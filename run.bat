@echo off
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Running the script...
python src/generate_datamatrix.py

echo.
echo Process completed!
echo.
pause 