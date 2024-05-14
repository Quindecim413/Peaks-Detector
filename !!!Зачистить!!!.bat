call conda env remove -p venv -y
call conda remove -p venv --all -y
call RD /s /q venv
call RD /s /q app
call xcopy /e /k /h /i .app app
@echo off
pause