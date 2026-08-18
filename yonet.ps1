param(
    [ValidateSet("start", "stop")]
    [string]$Action = "start"
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$backendDir = Join-Path $root "backend"
$frontendDir = Join-Path $root "frontend"

function Stop-PortProcess {
    param([int]$Port)
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
        $procIds = $conns.OwningProcess | Sort-Object -Unique
        foreach ($procId in $procIds) {
            try {
                Stop-Process -Id $procId -Force -ErrorAction Stop
                Write-Host "  Port $Port kapatildi (PID $procId)"
            } catch {
                Write-Host "  Port $Port icin islem durdurulamadi: $_"
            }
        }
    } else {
        Write-Host "  Port $Port zaten bos."
    }
}

function Stop-StrayProjectProcess {
    # Onceki calistirmalardan kalan, port dinlemeyen ama hala calisan
    # (uvicorn/vite) surecleri de temizler - "hayalet" surec birikmesini onler.
    $candidates = Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='node.exe'" -ErrorAction SilentlyContinue
    foreach ($proc in $candidates) {
        if ($proc.CommandLine -and ($proc.CommandLine -like "*Summarize-AI*")) {
            try {
                Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
                Write-Host "  Artik surec temizlendi (PID $($proc.ProcessId))"
            } catch {
                # zaten kapanmis olabilir, sorun degil
            }
        }
    }
}

if ($Action -eq "start") {
    Write-Host "=== Summarize-AI baslatiliyor ===" -ForegroundColor Cyan

    # -NoExit KULLANILMIYOR: icindeki surec (uvicorn/npm) durdurulunca
    # pencere de otomatik kapansin, bos komut istemi olarak birikmesin.
    Write-Host "Backend baslatiliyor (port 8000)..."
    Start-Process powershell -ArgumentList @(
        "-ExecutionPolicy", "Bypass", "-Command",
        "cd '$backendDir'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"
    ) -WindowStyle Normal

    Write-Host "Frontend baslatiliyor (port 5173)..."
    Start-Process powershell -ArgumentList @(
        "-ExecutionPolicy", "Bypass", "-Command",
        "cd '$frontendDir'; npm run dev"
    ) -WindowStyle Normal

    Write-Host "Sunucularin ayaga kalkmasi bekleniyor..."
    Start-Sleep -Seconds 6

    Start-Process "http://localhost:5173"
    Write-Host "Tamamlandi. Tarayicida acildi: http://localhost:5173" -ForegroundColor Green
    Write-Host "Kapatmak icin kapat.bat dosyasini calistir."
}
elseif ($Action -eq "stop") {
    Write-Host "=== Summarize-AI durduruluyor ===" -ForegroundColor Cyan

    Write-Host "Backend (8000) durduruluyor..."
    Stop-PortProcess -Port 8000

    Write-Host "Frontend (5173) durduruluyor..."
    Stop-PortProcess -Port 5173

    Write-Host "Artik surecler kontrol ediliyor..."
    Stop-StrayProjectProcess

    Write-Host "Tamamlandi." -ForegroundColor Green
}
