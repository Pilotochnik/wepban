import asyncio
import httpx

async def test_api():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Тест 1: Проверка доступности API
        try:
            response = await client.get("http://127.0.0.1:8000/health")
            print(f"Health check: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Health check failed: {e}")
        
        # Тест 2: Проверка auth
        try:
            response = await client.post("http://127.0.0.1:8000/api/v1/users/auth", json={"telegram_id": 434532312})
            print(f"Auth: {response.status_code} - {response.json()}")
        except httpx.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {e.response.text if hasattr(e, 'response') else 'No response'}")
        except Exception as e:
            print(f"Auth failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
