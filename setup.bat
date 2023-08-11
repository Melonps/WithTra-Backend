@echo off

REM Update and install dependencies
REM For Windows, we will assume the user has installed Git and has Python in the system path
REM If not, please install them before running this script
python -m pip install --upgrade pip

REM Create and activate a virtual environment
python -m venv develop
call develop\Scripts\activate

pip install fastapi "uvicorn[standard]" firebase_admin