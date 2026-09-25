@echo off
title Tech Boss - Auto Cross-Poster (Bluesky + Mastodon)
cd /d "%~dp0"
echo ======================================================================
echo   Tech Boss (imtechboss.com) - Auto Cross-Poster
echo   Platforms: Bluesky (@imtechboss.bsky.social) ^& Mastodon (@imtechboss)
echo ======================================================================
echo.
echo Running automated drip cross-poster...
echo   * Existing backlog articles: Shared every 20-25 minutes to BOTH platforms.
echo   * New published articles: Shared with 5-minute priority difference.
echo   * History tracking: Auto-saved to scripts\social-history.json
echo.
node scripts/social-auto-scheduler.js
pause
