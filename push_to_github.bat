@echo off
cls
echo ========================================================
echo   Gemini Voice Studio - Push to GitHub
echo ========================================================
echo.

echo [1/3] Logging in to GitHub...
echo Please copy the one-time code and paste it into your browser.
echo.
gh auth login --hostname github.com -p https -w
if errorlevel 1 goto error

echo.
echo [2/3] Setting up Git credentials...
gh auth setup-git
if errorlevel 1 goto error

echo.
echo [3/3] Pushing to GitHub (origin main)...
git push -u origin main
if errorlevel 1 goto error

echo.
echo ========================================================
echo   SUCCESS: Pushed to GitHub successfully!
echo ========================================================
echo.
pause
exit /b 0

:error
echo.
echo ========================================================
echo   ERROR: Process failed. Please check the message above.
echo ========================================================
echo.
pause
exit /b 1
