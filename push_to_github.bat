@echo off
title Push to GitHub - College Student Management System
echo ================================================================
echo  Pushing project to GitHub:
echo  https://github.com/251ca029-hash/College_Student_management_system.git
echo ================================================================
echo.

git init
git remote remove origin 2>nul
git remote add origin https://github.com/251ca029-hash/College_Student_management_system.git
git branch -M main
git add .
git commit -m "Initial commit: College Student Management System with Flask, Supabase, ML & Chatbot"
echo.
echo Pushing to GitHub (main branch)...
git push -u origin main

echo.
echo ================================================================
echo Done! Check your repository on GitHub.
echo ================================================================
pause
