@echo off
echo Creating virtual environment (if not exists)...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies from requirements/base.txt...
pip install -r requirements\base.txt

echo Running Django migrations...
python manage.py makemigrations
python manage.py migrate

echo Starting Django server...
python manage.py runserver

pause
