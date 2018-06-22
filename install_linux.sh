#!/usr/bin/env bash

#environment variables have default values, but should be set before calling the installer
if [ -z "$VENV_NAME" ]; then
    echo "Warning: VENV_NAME was not set, using: creator-container" 
    VENV_NAME=pptp-monitor-container
fi

pip install virtualenv
virtualenv $VENV_NAME

source ./$VENV_NAME/bin/activate
#creator dependencies
apt-get install python-gi
apt-get install python-pip
apt-get install libgirepository1.0-dev

pip install virtualenv
virtualenv $VENV_NAME

source ./$VENV_NAME/bin/activate
#creator dependencies
pip install pygobject
pip install vext
pip install vext.gi


#Generate the script 
echo "#!/usr/bin/env bash" > start_pptp_monitor.sh
echo "#The name of the container used during installation" >> start_pptp_monitor.sh
echo VENV_NAME=$VENV_NAME >> start_pptp_monitor.sh
echo >> start_pptp_monitor.sh
echo "#Activate the container and invoke the gui" >> start_pptp_monitor.sh
echo source ./$VENV_NAME/bin/activate >> start_pptp_monitor.sh
echo "#These variables are set based on their values when the install script is executed. Re-set values as needed." >> start_pptp_monitor.sh
echo cd src >> start_pptp_monitor.sh
echo python main.py >> start_pptp_monitor.sh

chmod 755 start_pptp_monitor.sh
echo
echo
echo Type: ./start_pptp_monitor.sh to start the GUI

