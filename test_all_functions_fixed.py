#!/usr/bin/env python3
"""
Тест всех функций Project Manager после исправлений
"""
import requests
import json
import sys
from datetime import datetime

# Конфигурация
BASE_URL = "https://projectmanager.chickenkiller.com/api"
TEST_TELEGRAM_ID = 434532312  # ID создателя

def log_test(test_name, success, message=""):
    """Логирование результатов тестов"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if message:
        print(f"    {message}")
    return success

def test_api_health():
    """Тест доступности API"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        success = response.status_code == 200
        return log_test("API Health Check", success, f"Status: {response.status_code}")
    except Exception as e:
        return log_test("API Health Check", False, str(e))

def test_user_check_access():
    """Тест проверки доступа пользователя"""
    try:
        response = requests.get(f"{BASE_URL}/v1/users/check-access/{TEST_TELEGRAM_ID}", timeout=10)
        success = response.status_code == 200
        if success:
            data = response.json()
            expected_fields = ['is_active', 'role', 'first_name', 'last_name', 'username']
            has_all_fields = all(field in data for field in expected_fields)
            success = has_all_fields and data['is_active'] and data['role'] == 'creator'
        
        return log_test("User Access Check", success, f"Status: {response.status_code}, Data: {response.json() if success else 'N/A'}")
    except Exception as e:
        return log_test("User Access Check", False, str(e))

def test_user_auth():
    """Тест авторизации пользователя"""
    try:
        auth_data = {"telegram_id": TEST_TELEGRAM_ID}
        response = requests.post(f"{BASE_URL}/v1/users/auth", json=auth_data, timeout=10)
        success = response.status_code == 200
        if success:
            data = response.json()
            has_token = 'access_token' in data and 'token_type' in data
            success = has_token
        
        return log_test("User Authentication", success, f"Status: {response.status_code}")
    except Exception as e:
        return log_test("User Authentication", False, str(e))

def test_projects_endpoint():
    """Тест endpoint проектов"""
    try:
        # Сначала получаем токен
        auth_data = {"telegram_id": TEST_TELEGRAM_ID}
        auth_response = requests.post(f"{BASE_URL}/v1/users/auth", json=auth_data, timeout=10)
        
        if auth_response.status_code != 200:
            return log_test("Projects Endpoint", False, "Failed to get auth token")
        
        token = auth_response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Тестируем получение проектов
        response = requests.get(f"{BASE_URL}/v1/projects/", headers=headers, timeout=10)
        success = response.status_code == 200
        return log_test("Projects Endpoint", success, f"Status: {response.status_code}")
    except Exception as e:
        return log_test("Projects Endpoint", False, str(e))

def test_frontend_access():
    """Тест доступности фронтенда"""
    try:
        response = requests.get("https://projectmanager.chickenkiller.com", timeout=10)
        success = response.status_code == 200
        return log_test("Frontend Access", success, f"Status: {response.status_code}")
    except Exception as e:
        return log_test("Frontend Access", False, str(e))

def test_cors_headers():
    """Тест CORS заголовков"""
    try:
        response = requests.options(f"{BASE_URL}/v1/users/check-access/{TEST_TELEGRAM_ID}", timeout=10)
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]
        has_cors = any(header in response.headers for header in cors_headers)
        return log_test("CORS Headers", has_cors, f"Headers: {list(response.headers.keys())}")
    except Exception as e:
        return log_test("CORS Headers", False, str(e))

def test_admin_endpoints():
    """Тест админских endpoint'ов"""
    try:
        # Получаем токен
        auth_data = {"telegram_id": TEST_TELEGRAM_ID}
        auth_response = requests.post(f"{BASE_URL}/v1/users/auth", json=auth_data, timeout=10)
        
        if auth_response.status_code != 200:
            return log_test("Admin Endpoints", False, "Failed to get auth token")
        
        token = auth_response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Тестируем админские endpoint'ы
        admin_endpoints = [
            "/v1/admin/stats",
            "/v1/admin/users",
            "/v1/admin/approvals/pending"
        ]
        
        results = []
        for endpoint in admin_endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            results.append(response.status_code == 200)
        
        success = all(results)
        return log_test("Admin Endpoints", success, f"Results: {results}")
    except Exception as e:
        return log_test("Admin Endpoints", False, str(e))

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование Project Manager API")
    print("=" * 50)
    print(f"📅 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Тестируемый Telegram ID: {TEST_TELEGRAM_ID}")
    print(f"🌐 Base URL: {BASE_URL}")
    print()
    
    tests = [
        test_api_health,
        test_user_check_access,
        test_user_auth,
        test_projects_endpoint,
        test_frontend_access,
        test_cors_headers,
        test_admin_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Результаты: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
        return 0
    else:
        print("⚠️  Некоторые тесты не прошли")
        return 1

if __name__ == "__main__":
    sys.exit(main())
