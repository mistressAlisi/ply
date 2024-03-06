echo "**** Assuming the Virtual Environment was created in step1.sh! If not, ctrl-c now!...****"
read -p "Press enter if you have already created and activated the venv from step one. Otherwise, abort with ctrl-c now. " fpath

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


echo "*** Creating Initial Levels and Classes ***"
python3 ./manage.py init_experience
python3 ./manage.py init_stats


echo "*** Load Dashboard Type Data ***"
python3 ./manage.py load_dashboard_types DOCUMENTATION/dashboards/types.tsv


echo "*** Granting Permissions to all Dashboards.... ***"
python3 ./manage.py grant_dashboards __auto-during-setup__ __auto-during-setup__ _all_



echo "****** SETUP COMPLETE! Further parameters can be modified in 'config/settings.ini'! *****"
echo "You may (now hopefully) start the Ply/Django environment using runserver and continue setup :3!"
echo "Thank you for using Ply! :3 :3"


