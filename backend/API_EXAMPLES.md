# Wardrobe AI - API Examples

Comprehensive examples for using the Wardrobe AI Backend API.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API uses simple user_id based identification. In production, implement proper authentication (JWT, OAuth, etc.).

---

## Garments API

### 1. Upload a Garment with Auto-Analysis

The LLM will automatically analyze the garment and enhance metadata.

```bash
curl -X POST http://localhost:5000/api/garments/ \
  -F "image=@/path/to/shirt.jpg" \
  -F "name=Blue Denim Shirt" \
  -F "category=top" \
  -F "user_id=user123"
```

**Response:**
```json
{
  "success": true,
  "garment": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123",
    "name": "Blue Denim Shirt",
    "category": "top",
    "color": "blue",
    "style": "casual",
    "season": ["spring", "fall"],
    "image_path": "backend/app/static/uploads/resized_550e8400_shirt.jpg",
    "description": "A classic blue denim shirt with button-down collar...",
    "tags": ["casual", "work", "weekend"],
    "created_at": "2025-11-05T10:30:00.000000"
  }
}
```

### 2. Get All Garments for User

```bash
curl -X GET "http://localhost:5000/api/garments/?user_id=user123"
```

**Response:**
```json
{
  "success": true,
  "count": 15,
  "garments": [...]
}
```

### 3. Semantic Search for Garments

```bash
curl -X POST http://localhost:5000/api/garments/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "formal black pants for winter",
    "user_id": "user123",
    "n_results": 5,
    "filters": {
      "category": "bottom"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "results": [
    {
      "id": "garment-id-1",
      "name": "Black Dress Pants",
      "category": "bottom",
      "similarity_score": 0.89,
      ...
    },
    ...
  ]
}
```

### 4. Update Garment

```bash
curl -X PUT http://localhost:5000/api/garments/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Light Blue Denim Shirt",
    "tags": ["casual", "work", "weekend", "summer"]
  }'
```

### 5. Delete Garment

```bash
curl -X DELETE http://localhost:5000/api/garments/550e8400-e29b-41d4-a716-446655440000
```

---

## Outfits API

### 1. Create an Outfit

```bash
curl -X POST http://localhost:5000/api/outfits/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "name": "Business Casual Meeting",
    "garment_ids": [
      "garment-id-1",
      "garment-id-2",
      "garment-id-3"
    ],
    "occasion": "work",
    "season": "spring",
    "style": "business",
    "description": "Perfect for client meetings",
    "tags": ["professional", "comfortable"]
  }'
```

**Response:**
```json
{
  "success": true,
  "outfit": {
    "id": "outfit-id-1",
    "user_id": "user123",
    "name": "Business Casual Meeting",
    "garment_ids": [...],
    "occasion": "work",
    ...
  }
}
```

### 2. Get AI Outfit Suggestions

This is the most powerful feature - the LLM analyzes your wardrobe and suggests combinations.

```bash
curl -X POST http://localhost:5000/api/outfits/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I need a casual outfit for a weekend brunch in spring",
    "user_id": "user123",
    "context": {
      "weather": "sunny",
      "temperature": 22,
      "formality": "casual",
      "preferences": ["comfortable", "stylish"]
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "suggestions": [
    {
      "garment_ids": ["id-1", "id-2", "id-3"],
      "name": "Fresh Spring Brunch Look",
      "description": "This combination pairs your light blue denim shirt with khaki chinos and white sneakers. The relaxed fit and breathable fabrics are perfect for a sunny spring day...",
      "styling_tips": [
        "Roll up the shirt sleeves for a more casual vibe",
        "Add a watch or simple bracelet as an accent",
        "Consider bringing a light jacket in case it gets cooler"
      ]
    },
    {
      "garment_ids": ["id-4", "id-5", "id-6"],
      "name": "Smart Casual Alternative",
      "description": "For a slightly more polished look, try your white polo with dark jeans and brown loafers...",
      "styling_tips": [...]
    }
  ]
}
```

### 3. Get Outfit with Full Garment Details

```bash
curl -X GET http://localhost:5000/api/outfits/outfit-id-1
```

**Response:**
```json
{
  "success": true,
  "outfit": {
    "id": "outfit-id-1",
    "name": "Business Casual Meeting",
    "garments": [
      {
        "id": "garment-id-1",
        "name": "Blue Denim Shirt",
        "image_path": "...",
        ...
      },
      ...
    ],
    ...
  }
}
```

### 4. Rate an Outfit

```bash
curl -X POST http://localhost:5000/api/outfits/outfit-id-1/rate \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5
  }'
```

---

## Chat API

### 1. Start a Conversation

```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi! I need help choosing an outfit for a job interview.",
    "user_id": "user123",
    "session_id": "session1"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Hello! I'd be happy to help you prepare for your job interview. A great interview outfit should be professional, well-fitted, and make you feel confident. Could you tell me:\n\n1. What industry is the job in? (tech, finance, creative, etc.)\n2. What's the company culture like? (formal, business casual, startup casual)\n3. What type of role are you interviewing for?\n\nThis will help me give you more specific recommendations from your wardrobe!",
  "session_id": "session1"
}
```

### 2. Continue Conversation

```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "It is a tech startup, software engineer role",
    "user_id": "user123",
    "session_id": "session1",
    "context": {
      "wardrobe_size": 25,
      "favorite_style": "smart casual"
    }
  }'
```

### 3. Get Conversation History

```bash
curl -X GET "http://localhost:5000/api/chat/history/session1?user_id=user123"
```

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "role": "user",
      "content": "Hi! I need help choosing an outfit..."
    },
    {
      "role": "assistant",
      "content": "Hello! I'd be happy to help..."
    },
    ...
  ]
}
```

### 4. Clear Conversation

```bash
curl -X DELETE "http://localhost:5000/api/chat/clear/session1?user_id=user123"
```

---

## Virtual Try-On API

### 1. Check API Health

```bash
curl -X GET http://localhost:5000/api/tryon/health
```

**Response:**
```json
{
  "success": true,
  "available": true,
  "api_url": "https://xxx.ngrok.io"
}
```

### 2. Generate Try-On with Uploaded Person Image

```bash
curl -X POST http://localhost:5000/api/tryon/generate \
  -F "person_image=@/path/to/person.jpg" \
  -F "garment_id=550e8400-e29b-41d4-a716-446655440000"
```

**Response:**
```json
{
  "success": true,
  "message": "Virtual try-on generated successfully",
  "image_url": "/api/tryon/images/tryon_123456.png",
  "image_path": "backend/app/static/generated/tryon_123456.png"
}
```

### 3. Generate Try-On with Existing Person Image

```bash
curl -X POST http://localhost:5000/api/tryon/generate \
  -F "person_image_path=/path/to/saved/person.jpg" \
  -F "garment_id=550e8400-e29b-41d4-a716-446655440000"
```

### 4. Access Generated Image

```bash
curl -X GET http://localhost:5000/api/tryon/images/tryon_123456.png --output result.png
```

Or directly in browser:
```
http://localhost:5000/api/tryon/images/tryon_123456.png
```

---

## Complete Workflow Example

Here's a complete workflow from uploading garments to getting outfit suggestions:

### Step 1: Upload Multiple Garments

```bash
# Upload shirt
curl -X POST http://localhost:5000/api/garments/ \
  -F "image=@shirt.jpg" \
  -F "name=White Oxford Shirt" \
  -F "category=top" \
  -F "user_id=john_doe"

# Upload pants
curl -X POST http://localhost:5000/api/garments/ \
  -F "image=@pants.jpg" \
  -F "name=Navy Chinos" \
  -F "category=bottom" \
  -F "user_id=john_doe"

# Upload shoes
curl -X POST http://localhost:5000/api/garments/ \
  -F "image=@shoes.jpg" \
  -F "name=Brown Leather Shoes" \
  -F "category=shoes" \
  -F "user_id=john_doe"
```

### Step 2: Search Your Wardrobe

```bash
curl -X POST http://localhost:5000/api/garments/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "business formal",
    "user_id": "john_doe"
  }'
```

### Step 3: Get Outfit Suggestions

```bash
curl -X POST http://localhost:5000/api/outfits/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "query": "professional outfit for an important business presentation",
    "user_id": "john_doe",
    "context": {
      "occasion": "presentation",
      "formality": "formal"
    }
  }'
```

### Step 4: Create and Save Outfit

```bash
curl -X POST http://localhost:5000/api/outfits/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john_doe",
    "name": "Big Presentation Outfit",
    "garment_ids": ["shirt-id", "pants-id", "shoes-id"],
    "occasion": "business"
  }'
```

### Step 5: Chat for Styling Tips

```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Should I wear a tie with my white oxford shirt and navy chinos?",
    "user_id": "john_doe"
  }'
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Description of what went wrong"
}
```

HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error

---

## Tips for Best Results

### For Garment Upload:
- Use clear, well-lit photos
- Photograph items on a plain background
- Ensure the entire garment is visible
- Image should be at least 512x512 pixels

### For Outfit Suggestions:
- Provide detailed context (occasion, weather, preferences)
- Maintain a diverse wardrobe in the system
- The more items you have, the better the suggestions

### For Chat:
- Be specific about your needs
- Provide context about the occasion
- Ask follow-up questions for refinement

### For Virtual Try-On:
- Use a full-body photo with clear visibility
- Stand in a neutral pose
- Good lighting is essential
- Person should be facing forward

---

## Python SDK Example

```python
import requests

class WardrobeAIClient:
    def __init__(self, base_url="http://localhost:5000", user_id="default_user"):
        self.base_url = base_url
        self.user_id = user_id

    def upload_garment(self, image_path, name, category):
        url = f"{self.base_url}/api/garments/"
        files = {"image": open(image_path, "rb")}
        data = {
            "name": name,
            "category": category,
            "user_id": self.user_id
        }
        response = requests.post(url, files=files, data=data)
        return response.json()

    def suggest_outfits(self, query, context=None):
        url = f"{self.base_url}/api/outfits/suggest"
        payload = {
            "query": query,
            "user_id": self.user_id,
            "context": context or {}
        }
        response = requests.post(url, json=payload)
        return response.json()

    def chat(self, message, session_id="default"):
        url = f"{self.base_url}/api/chat/message"
        payload = {
            "message": message,
            "user_id": self.user_id,
            "session_id": session_id
        }
        response = requests.post(url, json=payload)
        return response.json()

# Usage
client = WardrobeAIClient(user_id="john_doe")

# Upload
result = client.upload_garment("shirt.jpg", "Blue Shirt", "top")
print(result)

# Get suggestions
suggestions = client.suggest_outfits("casual summer outfit")
print(suggestions)

# Chat
response = client.chat("What should I wear to a wedding?")
print(response["message"])
```

---

For more information, see the main [README.md](README.md)
