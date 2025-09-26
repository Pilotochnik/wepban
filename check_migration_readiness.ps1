# 🔍 Проверка готовности к миграции (PowerShell версия)

Write-Host "🔍 Проверка готовности к миграции" -ForegroundColor Blue
Write-Host ""

$OLD_SERVER = "194.87.76.75"
$NEW_SERVER = "88.218.122.213"
$OLD_DOMAIN = "projectmanager.chickenkiller.com"
$NEW_DOMAIN = "webpan.chickenkiller.com"

# Функция для проверки
function Test-Connection {
    param($Name, $Command, $Expected)
    
    Write-Host "Проверяем $Name... " -NoNewline
    
    try {
        $result = Invoke-Expression $Command
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ OK" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ FAIL" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ FAIL" -ForegroundColor Red
        return $false
    }
}

Write-Host "1. Проверка текущего сервера ($OLD_SERVER)" -ForegroundColor Blue

# Проверка доступности старого сервера
Test-Connection "Доступность старого сервера" "Test-NetConnection -ComputerName $OLD_SERVER -Port 22 -InformationLevel Quiet"

# Проверка сервисов на старом сервере
Write-Host "Проверяем сервисы на старом сервере:"
try {
    $backend = Invoke-WebRequest -Uri "http://$OLD_SERVER`:8000/docs" -UseBasicParsing -TimeoutSec 10
    Write-Host "  Backend: ✅ OK" -ForegroundColor Green
} catch {
    Write-Host "  Backend: ❌ FAIL" -ForegroundColor Red
}

try {
    $frontend = Invoke-WebRequest -Uri "https://$OLD_DOMAIN" -UseBasicParsing -TimeoutSec 10
    Write-Host "  Frontend: ✅ OK" -ForegroundColor Green
} catch {
    Write-Host "  Frontend: ❌ FAIL" -ForegroundColor Red
}

Write-Host ""
Write-Host "2. Проверка нового сервера ($NEW_SERVER)" -ForegroundColor Blue

# Проверка доступности нового сервера
Test-Connection "Доступность нового сервера" "Test-NetConnection -ComputerName $NEW_SERVER -Port 22 -InformationLevel Quiet"

# Проверка SSH доступности
Write-Host "Проверяем SSH доступность нового сервера:"
try {
    $sshTest = ssh -o ConnectTimeout=10 root@$NEW_SERVER "echo test" 2>$null
    if ($sshTest -eq "test") {
        Write-Host "  SSH: ✅ OK" -ForegroundColor Green
    } else {
        Write-Host "  SSH: ❌ FAIL" -ForegroundColor Red
    }
} catch {
    Write-Host "  SSH: ❌ FAIL" -ForegroundColor Red
}

Write-Host ""
Write-Host "3. Проверка DNS" -ForegroundColor Blue

# Проверка DNS записи
Write-Host "Проверяем DNS запись для $NEW_DOMAIN:"
try {
    $dns = Resolve-DnsName -Name $NEW_DOMAIN -Type A
    if ($dns.IPAddress -contains $NEW_SERVER) {
        Write-Host "  DNS: ✅ OK ($NEW_DOMAIN -> $NEW_SERVER)" -ForegroundColor Green
    } else {
        Write-Host "  DNS: ⚠️  WARNING (запись не указывает на $NEW_SERVER)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  DNS: ❌ FAIL (запись не найдена)" -ForegroundColor Red
}

Write-Host ""
Write-Host "4. Проверка файлов проекта" -ForegroundColor Blue

# Проверка наличия ключевых файлов
$files = @(
    "backend/app/core/config.py",
    "bot/app/core/config.py", 
    "frontend/vite.config.ts",
    "nginx-config.txt",
    "migrate_to_new_server.sh"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  $file: ✅ OK" -ForegroundColor Green
    } else {
        Write-Host "  $file: ❌ FAIL" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "5. Проверка .env файлов на старом сервере" -ForegroundColor Blue

try {
    $envFiles = ssh root@$OLD_SERVER "ls -la /var/www/project-manager/backend/.env /var/www/project-manager/bot/.env" 2>$null
    Write-Host "  .env файлы: ✅ OK" -ForegroundColor Green
} catch {
    Write-Host "  .env файлы: ❌ FAIL" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Проверка завершена!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Рекомендации перед миграцией:" -ForegroundColor Yellow
Write-Host "1. Убедитесь, что DNS запись $NEW_DOMAIN указывает на $NEW_SERVER"
Write-Host "2. Создайте полный бэкап базы данных"
Write-Host "3. Уведомите пользователей о плановом обслуживании"
Write-Host "4. Подготовьте план отката на случай проблем"
Write-Host ""
Write-Host "🚀 Готово к миграции! Запустите: .\quick_migration.ps1" -ForegroundColor Green
