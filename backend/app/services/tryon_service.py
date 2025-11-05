import requests
from typing import Optional
import base64
from pathlib import Path
from config.config import Config


class TryOnService:
    """Service for virtual try-on using Colab API (OOTDiffusion)"""

    def __init__(self):
        self.api_url = Config.COLAB_API_URL
        print(f"TryOn Service initialized with API URL: {self.api_url}")

    def generate_tryon(
        self,
        person_image_path: str,
        garment_image_path: str,
        output_path: Optional[str] = None
    ) -> dict:
        """
        Generate virtual try-on image

        Args:
            person_image_path: Path to user's photo
            garment_image_path: Path to garment image
            output_path: Where to save the result (optional)

        Returns:
            Dictionary with result info
        """
        if not self.api_url:
            return {
                "success": False,
                "error": "Colab API URL not configured. Please set COLAB_API_URL in .env"
            }

        try:
            # Read images and encode to base64
            with open(person_image_path, 'rb') as f:
                person_img_b64 = base64.b64encode(f.read()).decode('utf-8')

            with open(garment_image_path, 'rb') as f:
                garment_img_b64 = base64.b64encode(f.read()).decode('utf-8')

            # Prepare request payload
            payload = {
                "person_image": person_img_b64,
                "garment_image": garment_img_b64
            }

            # Call Colab API
            print(f"Calling virtual try-on API: {self.api_url}")
            response = requests.post(
                f"{self.api_url}/tryon",
                json=payload,
                timeout=120  # Virtual try-on can take time
            )

            response.raise_for_status()

            result = response.json()

            # Save generated image if output path provided
            if output_path and result.get('success') and result.get('image'):
                generated_img_b64 = result['image']
                generated_img_bytes = base64.b64decode(generated_img_b64)

                # Ensure output directory exists
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, 'wb') as f:
                    f.write(generated_img_bytes)

                result['output_path'] = output_path

            return result

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Virtual try-on request timed out. The API may be processing or unavailable."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}"
            }
        except Exception as e:
            print(f"Error in virtual try-on: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def check_api_health(self) -> bool:
        """Check if Colab API is available"""
        if not self.api_url:
            return False

        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False


# Singleton instance
_tryon_service = None


def get_tryon_service() -> TryOnService:
    """Get singleton instance of TryOnService"""
    global _tryon_service
    if _tryon_service is None:
        _tryon_service = TryOnService()
    return _tryon_service
