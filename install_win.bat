@echo off
REM Edit the following variables according to python installation
set PYTHONARCH=64

REM ask user for version of python
set /P version64="Is your python installation Python 2.7.* 64-bit? (Y/N): "
IF NOT "%version64%"=="Y" IF NOT "%version64%"=="y" (
set PYTHONARCH=32
echo *************************************************************************************************
echo Sorry, this version of Python is currently not supported. Please install Python 2.7 64-bit.
echo *************************************************************************************************
pause
exit
)

REM set directory to place Gtk files
set PYTHONPACKAGES_PATH=Lib\site-packages\

REM name the container that will be created
set VENV_NAME=app-container

REM install and start the venv container
pip install virtualenv
virtualenv "%VENV_NAME%"

IF %PYTHONARCH%==64 (
echo Processing using a 64-bit python27 installation
%VENV_NAME%\Scripts\activate & pip install lxml & xcopy python27-64bit-gtk3\* "%VENV_NAME%" /E /Y & %VENV_NAME%\Scripts\deactivate
REM Now create the file that will start the gui
echo REM the name of the container used during installation > start.bat
echo set VENV_NAME=app-container >> start.bat
echo. >> start.bat
echo REM activate the container and invoke the gui >> start.bat
echo %VENV_NAME%\Scripts\activate ^& cd src ^& python main.py ^& deactivate ^& cd .. >> start.bat
echo Type: start.bat to start the application
)

