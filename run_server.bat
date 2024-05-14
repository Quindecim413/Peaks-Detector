echo activating virtual enviroment
call conda activate ./venv
echo starting server
call jupyter notebook --no-browser --config=jupyter_notebook_config.py
pause