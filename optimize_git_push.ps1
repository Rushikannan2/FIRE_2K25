# =====================================================
# Git Push Optimization Script for CryptoQ Project
# Optimizes Git performance for large repositories
# PowerShell Version
# =====================================================

# Set console colors
$Host.UI.RawUI.ForegroundColor = "White"

Write-Host ""
Write-Host "🚀 Git Push Optimization Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Record start time
$startTime = Get-Date

Write-Host "📊 Analyzing Repository..." -ForegroundColor Cyan
Write-Host ""

# 1. Analyze Repository Size
Write-Host "1️⃣ Repository Analysis" -ForegroundColor Blue
Write-Host "------------------------" -ForegroundColor Blue

# Get repository size
$repoInfo = git count-objects -vH
$repoSize = ($repoInfo | Select-String "size:").ToString().Split(":")[1].Trim()
$fileCount = (git ls-files | Measure-Object).Count
$garbageSize = ($repoInfo | Select-String "size-garbage:").ToString().Split(":")[1].Trim()

Write-Host "Repository Size: " -NoNewline -ForegroundColor Yellow
Write-Host $repoSize -ForegroundColor White
Write-Host "Tracked Files: " -NoNewline -ForegroundColor Yellow
Write-Host $fileCount -ForegroundColor White
Write-Host "Garbage Size: " -NoNewline -ForegroundColor Yellow
Write-Host $garbageSize -ForegroundColor White

Write-Host ""

# 2. Configure Optimal Git Settings
Write-Host "2️⃣ Configuring Git Settings..." -ForegroundColor Blue
Write-Host "----------------------------" -ForegroundColor Blue

Write-Host "Setting optimal Git configuration..." -ForegroundColor Cyan

$gitConfigs = @(
    @{key="core.autocrlf"; value="true"; desc="core.autocrlf = true"},
    @{key="core.compression"; value="9"; desc="core.compression = 9"},
    @{key="pack.windowMemory"; value="100m"; desc="pack.windowMemory = 100m"},
    @{key="pack.packSizeLimit"; value="100m"; desc="pack.packSizeLimit = 100m"},
    @{key="http.postBuffer"; value="524288000"; desc="http.postBuffer = 500MB"},
    @{key="http.maxRequestBuffer"; value="100M"; desc="http.maxRequestBuffer = 100MB"}
)

foreach ($config in $gitConfigs) {
    $result = git config --global $config.key $config.value
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $($config.desc)" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to set $($config.desc)" -ForegroundColor Red
    }
}

Write-Host ""

# 3. Enable Git LFS for Large Files
Write-Host "3️⃣ Setting up Git LFS..." -ForegroundColor Blue
Write-Host "-------------------------" -ForegroundColor Blue

# Check if Git LFS is installed
try {
    git lfs version | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Git LFS is available. Setting up tracking..." -ForegroundColor Cyan
        
        git lfs install | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Git LFS installed" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to install Git LFS" -ForegroundColor Red
        }
        
        # Track large file types
        $lfsPatterns = @(
            "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff",
            "*.pth", "*.pt", "*.pkl", "*.joblib", "*.h5", "*.hdf5",
            "*.mp4", "*.avi", "*.mov", "*.wmv", "*.flv",
            "*.zip", "*.rar", "*.7z", "*.tar", "*.gz",
            "*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx"
        )
        
        foreach ($pattern in $lfsPatterns) {
            git lfs track $pattern | Out-Null
        }
        
        Write-Host "✓ Large file types tracked with Git LFS" -ForegroundColor Green
        
        # Add .gitattributes
        git add .gitattributes | Out-Null
        if ($LASTEXITCODE -eq 0) {
            git commit -m "Enable Git LFS tracking for large files" | Out-Null
            Write-Host "✓ Git LFS configuration committed" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "⚠ Git LFS not installed. Skipping LFS setup." -ForegroundColor Yellow
    Write-Host "To install Git LFS: https://git-lfs.github.io/" -ForegroundColor Cyan
}

Write-Host ""

# 4. Repository Cleanup
Write-Host "4️⃣ Cleaning Repository..." -ForegroundColor Blue
Write-Host "-------------------------" -ForegroundColor Blue

Write-Host "Running aggressive garbage collection..." -ForegroundColor Cyan
git gc --aggressive --prune=now | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Garbage collection completed" -ForegroundColor Green
} else {
    Write-Host "✗ Garbage collection failed" -ForegroundColor Red
}

Write-Host "Repacking objects for optimal compression..." -ForegroundColor Cyan
git repack -a -d --depth=250 --window=250 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Object repacking completed" -ForegroundColor Green
} else {
    Write-Host "✗ Object repacking failed" -ForegroundColor Red
}

Write-Host ""

# 5. Analyze Results
Write-Host "5️⃣ Optimization Results" -ForegroundColor Blue
Write-Host "-------------------------" -ForegroundColor Blue

# Get new repository size
$newRepoInfo = git count-objects -vH
$newRepoSize = ($newRepoInfo | Select-String "size:").ToString().Split(":")[1].Trim()
$newGarbageSize = ($newRepoInfo | Select-String "size-garbage:").ToString().Split(":")[1].Trim()

Write-Host "New Repository Size: " -NoNewline -ForegroundColor Yellow
Write-Host $newRepoSize -ForegroundColor White
Write-Host "New Garbage Size: " -NoNewline -ForegroundColor Yellow
Write-Host $newGarbageSize -ForegroundColor White

Write-Host ""

# 6. Test Push Speed
Write-Host "6️⃣ Testing Push Performance..." -ForegroundColor Blue
Write-Host "-------------------------------" -ForegroundColor Blue

Write-Host "Testing push to origin..." -ForegroundColor Cyan
Write-Host "Note: This will attempt to push to your remote repository" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to skip the push test" -ForegroundColor Yellow
Write-Host ""

# Record push start time
$pushStartTime = Get-Date

# Attempt push
Write-Host "Executing git push..." -ForegroundColor Cyan
git push -u origin main

$pushExitCode = $LASTEXITCODE
$pushEndTime = Get-Date
$pushDuration = $pushEndTime - $pushStartTime

if ($pushExitCode -eq 0) {
    Write-Host "✓ Push completed successfully!" -ForegroundColor Green
    Write-Host "Push duration: $($pushDuration.TotalSeconds.ToString('F2')) seconds" -ForegroundColor Cyan
} else {
    Write-Host "✗ Push failed or was cancelled" -ForegroundColor Red
}

Write-Host ""

# 7. Summary Report
Write-Host "📊 OPTIMIZATION SUMMARY" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue
Write-Host ""

Write-Host "Repository Statistics:" -ForegroundColor Cyan
Write-Host "• Total Tracked Files: " -NoNewline -ForegroundColor Yellow
Write-Host $fileCount -ForegroundColor White
Write-Host "• Original Size: " -NoNewline -ForegroundColor Yellow
Write-Host $repoSize -ForegroundColor White
Write-Host "• Optimized Size: " -NoNewline -ForegroundColor Yellow
Write-Host $newRepoSize -ForegroundColor White
Write-Host "• Garbage Cleaned: " -NoNewline -ForegroundColor Yellow
Write-Host "$garbageSize → $newGarbageSize" -ForegroundColor White

Write-Host ""
Write-Host "Git Configuration Applied:" -ForegroundColor Cyan
Write-Host "• Compression Level: 9 (maximum)" -ForegroundColor Yellow
Write-Host "• Pack Memory: 100MB" -ForegroundColor Yellow
Write-Host "• Pack Size Limit: 100MB" -ForegroundColor Yellow
Write-Host "• HTTP Buffer: 500MB" -ForegroundColor Yellow
Write-Host "• HTTP Max Request: 100MB" -ForegroundColor Yellow

Write-Host ""
Write-Host "Performance Improvements:" -ForegroundColor Cyan
Write-Host "• Repository cleaned and repacked" -ForegroundColor Yellow
Write-Host "• Large files tracked with Git LFS" -ForegroundColor Yellow
Write-Host "• Optimal compression settings applied" -ForegroundColor Yellow
Write-Host "• Increased upload buffer size" -ForegroundColor Yellow

Write-Host ""
Write-Host "✅ Git push optimization completed!" -ForegroundColor Green
Write-Host "Future pushes should be significantly faster." -ForegroundColor Cyan

Write-Host ""
Write-Host "💡 Additional Recommendations:" -ForegroundColor Blue
Write-Host "• Consider adding large model files to .gitignore" -ForegroundColor Yellow
Write-Host "• Use Git LFS for files larger than 100MB" -ForegroundColor Yellow
Write-Host "• Regularly run 'git gc --aggressive' for maintenance" -ForegroundColor Yellow
Write-Host "• Monitor repository size with 'git count-objects -vH'" -ForegroundColor Yellow

Write-Host ""
Write-Host "Script completed at: $(Get-Date)" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to continue"