@echo off
chcp 65001 >nul
echo Cleaning up large files from Git...

git rm --cached "Git-2.51.2-64-bit.exe" 2>nul
git rm --cached "node-v24.11.1-x64.msi" 2>nul

git add .gitignore

git commit -m "Remove large installer files and update .gitignore"

echo Done! Now run: git push
pause

