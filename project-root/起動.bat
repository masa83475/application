@echo off
title scanmeter-app 起動

echo -----------------------------------------
echo  scanmeter-app 起動中...
echo -----------------------------------------
echo.

echo Docker Desktop を確認しています...

:: Docker が起動しているか確認
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Desktop が起動していません。起動します...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo 起動を待機しています...
    timeout /t 10 >nul

    docker info >nul 2>&1
    if %errorlevel% neq 0 (
        echo Docker Desktop が起動できませんでした。
        echo 手動で起動してから再度お試しください。
        pause
        exit /b
    )
)

echo Docker Desktop が起動しています。
echo.

echo scanmeter-app イメージを確認しています...

:: イメージ存在確認
docker images | findstr "scanmeter-app" >nul
if %errorlevel% neq 0 (
    echo scanmeter-app イメージが見つかりません。
    echo scanmeter-app.tar をロードしてください。
    echo 例: docker load -i scanmeter-app.tar
    pause
    exit /b
)

echo → OK: scanmeter-app イメージが見つかりました。
echo.

echo 既存コンテナを確認しています...

:: 既存コンテナ停止・削除
docker ps -a | findstr "scanmeter-app" >nul
if %errorlevel% eq 0 (
    echo 既存コンテナを停止しています...
    docker stop scanmeter-app >nul 2>&1

    echo 既存コンテナを削除しています...
    docker rm scanmeter-app >nul 2>&1
) else (
    echo → 既存コンテナなし
)

echo.
echo コンテナを起動します...
echo.

:: ログを表示し続けるモードで起動（-d を使わない）
docker run --name scanmeter-app -p 8000:8000 scanmeter-app:latest

echo.
echo -----------------------------------------
echo  scanmeter-app が起動しました
echo -----------------------------------------
echo.

echo ブラウザを開いています...
start http://localhost:8000

echo ログを表示しています。終了するには Ctrl + C を押してください。
pause
