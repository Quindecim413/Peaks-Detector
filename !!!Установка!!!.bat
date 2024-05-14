@echo off
if exist venv/ (
    call RD /s /q venv
)
@echo off
if exist __pycache__/ (
    call RD /s /q __pycache__
)
call conda env create -f environment.yml -p venv
call conda install -p venv "nbconvert=5.6.1" -y
pause