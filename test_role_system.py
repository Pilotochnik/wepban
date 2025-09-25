#!/usr/bin/env python3
"""
Тест системы ролей и одобрений Project Manager Bot
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

class RoleSystemTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.creator_id = 434532312
        self.test_results = []

    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Логирование результатов теста"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status} {test_name}"
        if details:
            result += f" - {details}"
        print(result)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': timestamp
        })
        return success

    async def test_creator_access(self) -> bool:
        """Тест 1: Доступ создателя ко всем функциям"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/admin/users",
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("Creator Admin Access", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Creator Admin Access", False, str(e))

    async def test_user_creation_by_creator(self) -> bool:
        """Тест 2: Создание пользователей создателем"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/admin/users",
                    json={
                        "telegram_id": 999999999,
                        "username": "test_worker",
                        "role": "worker"
                    },
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("User Creation by Creator", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("User Creation by Creator", False, str(e))

    async def test_approval_system(self) -> bool:
        """Тест 3: Система одобрений"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/admin/approvals",
                    headers={"X-User-ID": str(self.creator_id)}
                )
                success = response.status_code == 200
                return self.log_test("Approval System", success, f"Status: {response.status_code}")
        except Exception as e:
            return self.log_test("Approval System", False, str(e))

    async def run_all_tests(self):
        """Запуск всех тестов системы ролей"""
        print("🔐 Запуск тестирования системы ролей Project Manager Bot")
        print("=" * 60)
        
        await self.test_creator_access()
        await self.test_user_creation_by_creator()
        await self.test_approval_system()
        
        # Итоги
        print("=" * 60)
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ СИСТЕМЫ РОЛЕЙ:")
        print(f"✅ Пройдено: {passed}/{total} ({success_rate:.1f}%)")
        print(f"❌ Провалено: {total - passed}")
        
        return success_rate >= 90

async def main():
    """Главная функция"""
    tester = RoleSystemTester()
    success = await tester.run_all_tests()
    
    if not success:
        print("\n🔧 Рекомендации по системе ролей:")
        print("1. Проверьте, что создатель (ID: 434532312) существует в базе данных")
        print("2. Убедитесь, что система одобрений работает корректно")
        sys.exit(1)
    else:
        print("\n🚀 Все тесты системы ролей пройдены!")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())