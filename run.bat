@echo off
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Running the script...
python src/process_codes.py

echo.
echo Process completed!
echo.
pause 