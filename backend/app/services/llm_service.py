from openai import OpenAI
from typing import List, Dict, Optional
import json
from config.config import Config


class LLMService:
    """Service for interacting with OpenRouter LLM API"""

    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.model = Config.OPENROUTER_MODEL
        self.base_url = Config.OPENROUTER_BASE_URL

        # Initialize OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        print(f"LLM Service initialized with model: {self.model}")

    def analyze_garment_image(self, garment_data: Dict) -> Dict:
        """
        Analyze a garment and extract metadata using LLM

        Args:
            garment_data: Dictionary with garment info (name, category, etc.)

        Returns:
            Enhanced garment metadata
        """
        try:
            prompt = self._create_garment_analysis_prompt(garment_data)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a fashion expert AI. Analyze clothing items and provide detailed, structured information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            result = response.choices[0].message.content

            # Parse the response
            enhanced_data = self._parse_garment_analysis(result, garment_data)

            return enhanced_data

        except Exception as e:
            print(f"Error analyzing garment: {e}")
            # Return original data if analysis fails
            return garment_data

    def suggest_outfits(
        self,
        user_query: str,
        available_garments: List[Dict],
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Suggest outfit combinations based on user query and available garments

        Args:
            user_query: User's request (e.g., "casual outfit for spring")
            available_garments: List of garment dictionaries from wardrobe
            context: Additional context (weather, occasion, preferences)

        Returns:
            Outfit suggestions with explanations
        """
        try:
            prompt = self._create_outfit_suggestion_prompt(
                user_query,
                available_garments,
                context
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a personal fashion stylist AI. Create stylish, practical outfit combinations based on the user's wardrobe."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=1000
            )

            result = response.choices[0].message.content

            # Parse outfit suggestions
            suggestions = self._parse_outfit_suggestions(result, available_garments)

            return suggestions

        except Exception as e:
            print(f"Error suggesting outfits: {e}")
            return {
                "success": False,
                "error": str(e),
                "suggestions": []
            }

    def chat_about_fashion(
        self,
        user_message: str,
        conversation_history: List[Dict],
        user_context: Optional[Dict] = None
    ) -> str:
        """
        General fashion chat conversation

        Args:
            user_message: User's message
            conversation_history: Previous messages in conversation
            user_context: User preferences and wardrobe info

        Returns:
            AI response
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": self._create_fashion_assistant_system_prompt(user_context)
                }
            ]

            # Add conversation history
            messages.extend(conversation_history)

            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=800
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error in fashion chat: {e}")
            return "I apologize, but I'm having trouble responding right now. Please try again."

    def _create_garment_analysis_prompt(self, garment_data: Dict) -> str:
        """Create prompt for garment analysis"""
        prompt = f"""Analyze this clothing item and provide detailed information:

Item: {garment_data.get('name', 'Unknown')}
Category: {garment_data.get('category', 'Unknown')}
Color: {garment_data.get('color', 'Unknown')}

Please provide:
1. A brief description of the item
2. Suggested style tags (e.g., casual, formal, sporty)
3. Suitable seasons (spring, summer, fall, winter)
4. Occasions where this would be appropriate
5. Complementary colors and styles that would pair well

Format your response as JSON with these fields:
{{
    "description": "...",
    "style": "...",
    "seasons": ["..."],
    "occasions": ["..."],
    "pairs_well_with": ["..."]
}}"""

        return prompt

    def _parse_garment_analysis(self, llm_response: str, original_data: Dict) -> Dict:
        """Parse LLM response for garment analysis"""
        try:
            # Try to extract JSON from response
            start = llm_response.find('{')
            end = llm_response.rfind('}') + 1

            if start != -1 and end > start:
                json_str = llm_response[start:end]
                parsed = json.loads(json_str)

                # Merge with original data
                enhanced = original_data.copy()
                enhanced['description'] = parsed.get('description', enhanced.get('description', ''))
                enhanced['style'] = parsed.get('style', enhanced.get('style', ''))
                enhanced['season'] = parsed.get('seasons', enhanced.get('season', []))
                enhanced['tags'] = parsed.get('occasions', enhanced.get('tags', []))

                if 'pairs_well_with' in parsed:
                    enhanced['metadata']['pairs_well_with'] = parsed['pairs_well_with']

                return enhanced

        except Exception as e:
            print(f"Error parsing garment analysis: {e}")

        return original_data

    def _create_outfit_suggestion_prompt(
        self,
        user_query: str,
        garments: List[Dict],
        context: Optional[Dict]
    ) -> str:
        """Create prompt for outfit suggestions"""

        garment_list = "\n".join([
            f"- ID: {g['id']}, Name: {g.get('name', 'N/A')}, Category: {g.get('category', 'N/A')}, "
            f"Color: {g.get('color', 'N/A')}, Style: {g.get('style', 'N/A')}"
            for g in garments[:20]  # Limit to avoid token overflow
        ])

        context_str = ""
        if context:
            context_str = f"\nAdditional context: {json.dumps(context)}"

        prompt = f"""The user wants: {user_query}
{context_str}

Available garments in wardrobe:
{garment_list}

Please suggest 2-3 outfit combinations using these garments. For each outfit:
1. List the garment IDs to combine
2. Explain why this combination works
3. Provide styling tips

Format as JSON:
{{
    "suggestions": [
        {{
            "garment_ids": ["id1", "id2", "id3"],
            "name": "Outfit name",
            "description": "Why this works...",
            "styling_tips": ["tip1", "tip2"]
        }}
    ]
}}"""

        return prompt

    def _parse_outfit_suggestions(self, llm_response: str, garments: List[Dict]) -> Dict:
        """Parse LLM outfit suggestions"""
        try:
            # Extract JSON
            start = llm_response.find('{')
            end = llm_response.rfind('}') + 1

            if start != -1 and end > start:
                json_str = llm_response[start:end]
                parsed = json.loads(json_str)

                return {
                    "success": True,
                    "suggestions": parsed.get('suggestions', []),
                    "raw_response": llm_response
                }

        except Exception as e:
            print(f"Error parsing outfit suggestions: {e}")

        return {
            "success": False,
            "suggestions": [],
            "raw_response": llm_response
        }

    def _create_fashion_assistant_system_prompt(self, user_context: Optional[Dict]) -> str:
        """Create system prompt for fashion chat"""
        base_prompt = """You are a knowledgeable and friendly personal fashion stylist AI assistant.
You help users with:
- Outfit suggestions and styling advice
- Fashion trends and tips
- Color coordination
- Wardrobe organization
- Occasion-appropriate dressing

Be conversational, encouraging, and provide practical advice."""

        if user_context:
            base_prompt += f"\n\nUser context: {json.dumps(user_context)}"

        return base_prompt


# Singleton instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get singleton instance of LLMService"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
