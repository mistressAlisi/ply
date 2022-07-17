#!/bin/bash
echo "***Welcome to Ply!***"
echo "Step 1: Install Python3.9x: Virtualenv, Pip and toolchain..."
sudo apt-get install python3-venv python3-pip python3-dev libpq-dev pwgen
echo "Step 2: Create Virtual Environment... Please specify path:"
path="$HOME/venv"
read -p "Enter the path to create the 'ply' folder in, or enter for default: [~/venv/ply]: " npath
path=${npath:-$path}
fpath="$path/ply"
echo "Creating and activating venv: $fpath"
python3 -m venv "$fpath"
source $fpath'/bin/activate'
echo "Intalling Python dependencies (pip install -r requirements.txt)"
pip install -r requirements.txt
echo "***Setup Complete: Initialising Configuration...***"
echo "***Configuration will be generated as 'config/settings.ini': Please mkdir or mount ./config/ before continuing!)***"
read -p "***WARNING: Proceeding past this point WILL replace existing configuration settings (and secret keys). Ctrl-C now if you wish to abort, or press enter to continue...***" abort
read -n 1 -p "Do you wish to install PostgreSQL Locally? (y/n): " ipq
echo "\n"
if [ $ipq == 'y' ];
then
    echo "Installing PostgreSQL..."
    sudo apt-get install postgresql-13
    echo "Installation Complete: PSQL Must be configured!"
    read -p "*** Please configure 'pg_hba.conf' and 'postgresql.conf' and press Enter to continue when ready. ***" abort
fi
    read -p "*** To continue installation; you will require a PostgreSQL user and database set up. The user should be the owner of the database. Please create both objects and press enter to continue when ready. ***" abort
echo "***** Please enter the PostgreSQL Configuration parameters below: *****"
conf_valid=false
while [ $conf_valid == false ]
do
DB_HOST='127.0.0.1'
read  -p "Host name / IP? [127.0.0.1]: " nDB_HOST
DB_HOST=${nDB_HOST:-$DB_HOST}

DB_PORT='5432'
read  -p "Port? [5432]: " nDB_PORT
DB_PORT=${nDB_PORT:-$DB_PORT}

DB_NAME='ply'
read  -p "DB name? [ply]: " nDB_NAME
DB_NAME=${nDB_NAME:-$DB_NAME}

DB_USER='ply'
read  -p "User name? [ply]: " nDB_USER
DB_USER=${nDB_USER:-$DB_USER}

DB_PW='ply'
read -s -p "User Password? (will not be echoed) [ply]: " nDB_PW
echo "\n"
DB_PW=${nDB_PW:-$DB_PW}
echo "*** Connection String is: pgsql://$DB_USER@$DB_HOST:$DB_PORT/$DB_NAME ***"
read -n1 -p "Is this correct? (y/n): " correct
if [ $correct == 'y' ];
then
    conf_valid=true
fi
echo "\n"
done;
echo "Generating Config file 'config/settings.ini'..."
cp setup/INI_DEF config/settings.ini
sed -i "s/DBNAME/${DB_NAME}/" config/settings.ini
sed -i "s/DBUSER/${DB_USER}/" config/settings.ini
sed -i "s/DBPW/${DB_PW}/" config/settings.ini
sed -i "s/DBHOST/${DB_HOST}/" config/settings.ini
sed -i "s/DBPORT/${DB_PORT}/" config/settings.ini
SECRETS=`pwgen -s 230 1`
sed -i "s/SKEY/${SECRETS}/" config/settings.ini

echo "**** Starting Database Setup...****"
python3 ./manage.py migrate

echo "**** Installing SQL Files...****"
python3 ./manage.py install_sql_files _all_

echo "**** --> CREATING SUPERUSER / ADMINISTRATOR <--****"
python3 ./manage.py createsuperuser

echo "**** Initalizing Timezone Data...****"
python3 ./manage.py init_timezones

echo "**** Dynapages: Register Templates...****"
python3 ./manage.py registertemplate

echo "**** Dynapages: Register Widgets...****"
python3 ./manage.py registerwidgets

echo "**** Dynapages: Init Dynapages...****"
python3 ./manage.py init_dynapages

echo "*** Loading Disciplines and Categories (defaults): ***"
python3 ./manage.py load_disciplines DOCUMENTATION/Categories/disciplines.tsv
python3 ./manage.py load_categories DOCUMENTATION/Categories/categories.tsv


echo "*** Creating Initial Community ***"
python3 ./manage.py create_community


echo "****** SETUP COMPLETE! Further parameters can be modified in 'config/settings.ini'! *****"
echo "You may (now hopefully) start the Django environment using runserver! :3!"
echo "Thank you for using Ply! :3 :3"


