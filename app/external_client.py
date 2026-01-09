import httpx
import os
from typing import Dict

class ExternalAPIError(Exception):
    pass

BASE_URL = os.getenv("EXTERNAL_API_BASE_URL", "https://jsonplaceholder.typicode.com")

async def fetch_external_post(external_post_id: int) -> Dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/posts/{external_post_id}", timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise ExternalAPIError("External API timeout")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ExternalAPIError("Post not found on external API")
            raise ExternalAPIError(f"External API error: {e.response.status_code}")
        except Exception:
            raise ExternalAPIError("Failed to fetch from external API")
