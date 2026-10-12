# Tech Boss - 100% Native Windows Chrome Medium Auto-Poster
param(
    [string]$ArticleId = "how-to-bypass-tpm-2-install-windows-11-unsupported-pc-2026"
)

$articleUrl = "https://imtechboss.com/post?id=$ArticleId"

Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "🚀 NATIVE MEDIUM AUTO-POST ENGINE (IN YOUR REAL CHROME)" -ForegroundColor Green
Write-Host "URL: $articleUrl" -ForegroundColor Yellow
Write-Host "==============================================================="

# 1. Copy URL to Clipboard
Set-Clipboard -Value $articleUrl
Write-Host "1. Copied article URL to clipboard..." -ForegroundColor Gray

# 2. Open Medium import in user's active, logged-in Chrome
Write-Host "2. Opening Medium in your logged-in Chrome..." -ForegroundColor Gray
Start-Process "chrome.exe" "https://medium.com/p/import"

# 3. Wait for Medium to load
Write-Host "3. Waiting 5 seconds for Medium page to load..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# 4. Activate Chrome Window
$wshell = New-Object -ComObject WScript.Shell
$wshell.AppActivate("Google Chrome")
$wshell.AppActivate("Chrome")
Start-Sleep -Milliseconds 800

# 5. Paste the URL into the input field
Write-Host "4. Pasting URL into import field..." -ForegroundColor Gray
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 600

# 6. Press Enter to trigger import
Write-Host "5. Submitting import request..." -ForegroundColor Gray
$wshell.SendKeys("{ENTER}")

# 7. Wait for Medium to finish fetching and create draft
Write-Host "6. Waiting 6 seconds for Medium to create the draft..." -ForegroundColor Gray
Start-Sleep -Seconds 6

# 8. Press Enter again to open "See your story"
$wshell.AppActivate("Google Chrome")
$wshell.AppActivate("Chrome")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{ENTER}")

Write-Host "`n🎉 SUCCESS! Story is imported in your real Chrome!" -ForegroundColor Green
Write-Host "Review your story and click 'Publish' to make it live!" -ForegroundColor Cyan
Write-Host "==============================================================="
