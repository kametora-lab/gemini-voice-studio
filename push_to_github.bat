@echo off
chcp 65001 > nul
echo ========================================================
echo   Gemini Voice Studio - GitHub アップロード
echo ========================================================
echo.

set "GH_EXE=C:\Users\kaor\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\gh.exe"
set "GIT_EXE=C:\Users\kaor\AppData\Local\Programs\Git\cmd\git.exe"

echo 1. GitHub 認証を開始します...
echo    (ブラウザが開いたらコードを入力して認証してください)
echo.
"%GH_EXE%" auth login --hostname github.com -p https -w

echo.
echo 2. Git の認証を設定中...
"%GH_EXE%" auth setup-git

echo.
echo 3. GitHub (origin main) にプッシュ中...
"%GIT_EXE%" push -u origin main

echo.
echo ========================================================
echo   完了しました！ GitHub でリポジトリを確認してください。
echo ========================================================
pause
