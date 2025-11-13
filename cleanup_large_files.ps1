# Cleanup script: Remove large installer files from Git repository
# This script removes installers that should not be in the repository

Write-Host "Cleaning up large files from Git..." -ForegroundColor Cyan

# Remove files from Git (but keep them locally)
git rm --cached "Git-2.51.2-64-bit.exe" 2>$null
git rm --cached "node-v24.11.1-x64.msi" 2>$null

# Add .gitignore changes
git add .gitignore

# Create commit
git commit -m "Remove large installer files and update .gitignore"

Write-Host "Done! Now run: git push" -ForegroundColor Green
