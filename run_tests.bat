@echo off

REM Activating the virtual environment
call .\.venv\Scripts\activate.bat

REM Checking the availability of the coverage library
pip show coverage >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo The coverage library is not installed in active virtual environment. Please, install it uses next command: pip install coverage
    exit /b
)

cd .\project_code

coverage run -m unittest discover .\tests\ "test*.py"
coverage report
