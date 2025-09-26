#!/usr/bin/env python3
"""
Скрипт для проверки портов и конфигурации
"""
import socket
import requests
import subprocess
import sys

def check_port(host, port):
    """Проверяет доступность порта"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Ошибка при проверке порта {host}:{port}: {e}")
        return False

def check_http_endpoint(url):
    """Проверяет HTTP endpoint"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code, response.text[:200]
    except Exception as e:
        return None, str(e)

def main():
    print("=== Проверка портов и конфигурации ===\n")
    
    # Локальная проверка
    print("1. Локальная проверка:")
    local_ports = [
        ("Backend (8000)", "localhost", 8000),
        ("Frontend dev (3000)", "localhost", 3000),
    ]
    
    for name, host, port in local_ports:
        status = "✅ Доступен" if check_port(host, port) else "❌ Недоступен"
        print(f"   {name}: {host}:{port} - {status}")
    
    # Проверка сервера
    print("\n2. Проверка сервера:")
    server_ports = [
        ("HTTP (80)", "projectmanager.chickenkiller.com", 80),
        ("HTTPS (443)", "projectmanager.chickenkiller.com", 443),
    ]
    
    for name, host, port in server_ports:
        status = "✅ Доступен" if check_port(host, port) else "❌ Недоступен"
        print(f"   {name}: {host}:{port} - {status}")
    
    # Проверка HTTP endpoints
    print("\n3. Проверка HTTP endpoints:")
    endpoints = [
        ("Главная страница", "https://projectmanager.chickenkiller.com"),
        ("API health", "https://projectmanager.chickenkiller.com/api/v1/health"),
        ("API docs", "https://projectmanager.chickenkiller.com/docs"),
    ]
    
    for name, url in endpoints:
        status_code, response = check_http_endpoint(url)
        if status_code:
            print(f"   {name}: ✅ {status_code}")
        else:
            print(f"   {name}: ❌ {response}")
    
    # Проверка локальных процессов
    print("\n4. Локальные процессы:")
    try:
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        relevant_ports = ['3000', '8000']
        
        for line in lines:
            for port in relevant_ports:
                if f':{port}' in line and 'LISTEN' in line:
                    print(f"   Порт {port}: {line.strip()}")
    except Exception as e:
        print(f"   Ошибка при проверке процессов: {e}")

if __name__ == "__main__":
    main()
