import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.conf import settings
import requests
import json


def test_credentials():
    print("=== ТЕСТ ДАННЫХ ЮKASSA ===")
    print(f"Shop ID: {settings.YOOKASSA_SHOP_ID}")
    print(f"Secret Key: {settings.YOOKASSA_SECRET_KEY}")
    print(f"Key length: {len(settings.YOOKASSA_SECRET_KEY)}")
    print(f"Key starts with: {settings.YOOKASSA_SECRET_KEY[:5]}")

    # Тест 1: Basic Auth
    print("\n--- Тест Basic Auth ---")
    try:
        response = requests.get(
            'https://api.yookassa.ru/v3/me',
            auth=(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY),
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Тест 2: Bearer Token
    print("\n--- Тест Bearer Token ---")
    headers = {
        'Authorization': f'Bearer {settings.YOOKASSA_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(
            'https://api.yookassa.ru/v3/me',
            headers=headers,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_credentials()