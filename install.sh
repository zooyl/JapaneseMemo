#!/usr/bin/env bash

echo "---------------------------------------------------"
echo "This script will install virtual environment,"
echo "Set it up and install packages to run this project"
echo "One key note:"
echo "It will not install Python or Postgresql"
echo "---------------------------------------------------"
read -p "Click ""ENTER"" continue."
echo "Installing virtual environment..."
sudo apt install virtualenv
echo "---------------------------------------------------"
echo "Creating virtual environment in current directory"
echo "---------------------------------------------------"
virtualenv -p python3 venv
# pip install -r requirements.txt
venv/bin/pip install -r requirements.txt
source ./venv/bin/activate
echo "---------------------------------------------------"
echo "Installation completed"
echo "---------------------------------------------------"
echo "Make sure 'local_settings.py' is configured!"
echo "---------------------------------------------------"
read -r -p "Do you want to start server? [Y/n] " response
echo
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]] || [[ -z $response ]]; then
echo "---------------------------------------------------"
echo "Making migrations"
echo "---------------------------------------------------"
python manage.py migrate
echo "---------------------------------------------------"
echo "Collecting static files"
echo "---------------------------------------------------"
python manage.py collectstatic
echo "---------------------------------------------------"
echo "Running Tests"
echo "---------------------------------------------------"
python manage.py test
echo "---------------------------------------------------"
echo "Populating database"
echo "---------------------------------------------------"
python manage.py loaddata HiraganaData.json
echo "---------------------------------------------------"
echo "Please configure e-mail service in settings.py"
echo "otherwise you wont be able to register new users"
echo "---------------------------------------------------"
echo "Running Server"
echo "By default there is only one user:"
echo "'super-user' with password 'mkonjibhu'"
python manage.py runserver
fi
if [[ $response =~ ^(no|n| ) ]] || [[ -z $response ]]; then
exit
fi