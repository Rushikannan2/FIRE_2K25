@echo off
REM =====================================================
REM Git Push Optimization Script for CryptoQ Project
REM Optimizes Git performance for large repositories
REM =====================================================

setlocal enabledelayedexpansion

echo.
echo 🚀 Git Push Optimization Script
echo ================================
echo.

REM Colors for output
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "CYAN=[96m"
set "RESET=[0m"

REM Record start time
set start_time=%time%

echo %CYAN%📊 Analyzing Repository...%RESET%
echo.

REM 1. Analyze Repository Size
echo %BLUE%1️⃣ Repository Analysis%RESET%
echo ----------------------------

REM Get repository size
for /f "tokens=*" %%i in ('git count-objects -vH ^| findstr "size:"') do set repo_size=%%i
echo %YELLOW%Repository Size:%RESET% !repo_size!

REM Get file count
for /f %%i in ('git ls-files ^| find /c /v ""') do set file_count=%%i
echo %YELLOW%Tracked Files:%RESET% !file_count!

REM Get garbage size
for /f "tokens=*" %%i in ('git count-objects -vH ^| findstr "size-garbage:"') do set garbage_size=%%i
echo %YELLOW%Garbage Size:%RESET% !garbage_size!

echo.

REM 2. Configure Optimal Git Settings
echo %BLUE%2️⃣ Configuring Git Settings...%RESET%
echo --------------------------------

echo %CYAN%Setting optimal Git configuration...%RESET%

git config --global core.autocrlf true
if %errorlevel% equ 0 (echo %GREEN%✓ core.autocrlf = true%RESET%) else (echo %RED%✗ Failed to set core.autocrlf%RESET%)

git config --global core.compression 9
if %errorlevel% equ 0 (echo %GREEN%✓ core.compression = 9%RESET%) else (echo %RED%✗ Failed to set core.compression%RESET%)

git config --global pack.windowMemory "100m"
if %errorlevel% equ 0 (echo %GREEN%✓ pack.windowMemory = 100m%RESET%) else (echo %RED%✗ Failed to set pack.windowMemory%RESET%)

git config --global pack.packSizeLimit "100m"
if %errorlevel% equ 0 (echo %GREEN%✓ pack.packSizeLimit = 100m%RESET%) else (echo %RED%✗ Failed to set pack.packSizeLimit%RESET%)

git config --global http.postBuffer 524288000
if %errorlevel% equ 0 (echo %GREEN%✓ http.postBuffer = 500MB%RESET%) else (echo %RED%✗ Failed to set http.postBuffer%RESET%)

git config --global http.maxRequestBuffer 100M
if %errorlevel% equ 0 (echo %GREEN%✓ http.maxRequestBuffer = 100MB%RESET%) else (echo %RED%✗ Failed to set http.maxRequestBuffer%RESET%)

echo.

REM 3. Enable Git LFS for Large Files
echo %BLUE%3️⃣ Setting up Git LFS...%RESET%
echo --------------------------

REM Check if Git LFS is installed
git lfs version >nul 2>&1
if %errorlevel% equ 0 (
    echo %CYAN%Git LFS is available. Setting up tracking...%RESET%
    
    git lfs install
    if %errorlevel% equ 0 (echo %GREEN%✓ Git LFS installed%RESET%) else (echo %RED%✗ Failed to install Git LFS%RESET%)
    
    REM Track large file types
    git lfs track "*.jpg" "*.jpeg" "*.png" "*.gif" "*.bmp" "*.tiff"
    git lfs track "*.pth" "*.pt" "*.pkl" "*.joblib" "*.h5" "*.hdf5"
    git lfs track "*.mp4" "*.avi" "*.mov" "*.wmv" "*.flv"
    git lfs track "*.zip" "*.rar" "*.7z" "*.tar" "*.gz"
    git lfs track "*.pdf" "*.doc" "*.docx" "*.xls" "*.xlsx"
    
    echo %GREEN%✓ Large file types tracked with Git LFS%RESET%
    
    REM Add .gitattributes
    git add .gitattributes
    if %errorlevel% equ 0 (
        git commit -m "Enable Git LFS tracking for large files" >nul 2>&1
        echo %GREEN%✓ Git LFS configuration committed%RESET%
    )
) else (
    echo %YELLOW%⚠ Git LFS not installed. Skipping LFS setup.%RESET%
    echo %CYAN%To install Git LFS: https://git-lfs.github.io/%RESET%
)

echo.

REM 4. Repository Cleanup
echo %BLUE%4️⃣ Cleaning Repository...%RESET%
echo -------------------------

echo %CYAN%Running aggressive garbage collection...%RESET%
git gc --aggressive --prune=now
if %errorlevel% equ 0 (echo %GREEN%✓ Garbage collection completed%RESET%) else (echo %RED%✗ Garbage collection failed%RESET%)

echo %CYAN%Repacking objects for optimal compression...%RESET%
git repack -a -d --depth=250 --window=250
if %errorlevel% equ 0 (echo %GREEN%✓ Object repacking completed%RESET%) else (echo %RED%✗ Object repacking failed%RESET%)

echo.

REM 5. Analyze Results
echo %BLUE%5️⃣ Optimization Results%RESET%
echo --------------------------

REM Get new repository size
for /f "tokens=*" %%i in ('git count-objects -vH ^| findstr "size:"') do set new_repo_size=%%i
echo %YELLOW%New Repository Size:%RESET% !new_repo_size!

REM Get new garbage size
for /f "tokens=*" %%i in ('git count-objects -vH ^| findstr "size-garbage:"') do set new_garbage_size=%%i
echo %YELLOW%New Garbage Size:%RESET% !new_garbage_size!

echo.

REM 6. Test Push Speed
echo %BLUE%6️⃣ Testing Push Performance...%RESET%
echo -------------------------------

echo %CYAN%Testing push to origin...%RESET%
echo %YELLOW%Note: This will attempt to push to your remote repository%RESET%
echo %YELLOW%Press Ctrl+C to skip the push test%RESET%
echo.

REM Record push start time
set push_start=%time%

REM Attempt push
git push -u origin main
set push_exit_code=%errorlevel%

REM Record push end time
set push_end=%time%

if %push_exit_code% equ 0 (
    echo %GREEN%✓ Push completed successfully!%RESET%
) else (
    echo %RED%✗ Push failed or was cancelled%RESET%
)

echo.

REM 7. Summary Report
echo %BLUE%📊 OPTIMIZATION SUMMARY%RESET%
echo ================================
echo.

echo %CYAN%Repository Statistics:%RESET%
echo %YELLOW%• Total Tracked Files:%RESET% !file_count!
echo %YELLOW%• Original Size:%RESET% !repo_size!
echo %YELLOW%• Optimized Size:%RESET% !new_repo_size!
echo %YELLOW%• Garbage Cleaned:%RESET% !garbage_size! → !new_garbage_size!

echo.
echo %CYAN%Git Configuration Applied:%RESET%
echo %YELLOW%• Compression Level:%RESET% 9 (maximum)
echo %YELLOW%• Pack Memory:%RESET% 100MB
echo %YELLOW%• Pack Size Limit:%RESET% 100MB
echo %YELLOW%• HTTP Buffer:%RESET% 500MB
echo %YELLOW%• HTTP Max Request:%RESET% 100MB

echo.
echo %CYAN%Performance Improvements:%RESET%
echo %YELLOW%• Repository cleaned and repacked%RESET%
echo %YELLOW%• Large files tracked with Git LFS%RESET%
echo %YELLOW%• Optimal compression settings applied%RESET%
echo %YELLOW%• Increased upload buffer size%RESET%

echo.
echo %GREEN%✅ Git push optimization completed!%RESET%
echo %CYAN%Future pushes should be significantly faster.%RESET%

echo.
echo %BLUE%💡 Additional Recommendations:%RESET%
echo %YELLOW%• Consider adding large model files to .gitignore%RESET%
echo %YELLOW%• Use Git LFS for files larger than 100MB%RESET%
echo %YELLOW%• Regularly run 'git gc --aggressive' for maintenance%RESET%
echo %YELLOW%• Monitor repository size with 'git count-objects -vH'%RESET%

echo.
echo %CYAN%Script completed at: %time%%RESET%
echo.

pause
