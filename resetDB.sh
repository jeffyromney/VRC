python manage.py dumpdata >> allBackup.json
rm db.sqlite3
python manage.py syncdb --noinput
python manage.py loaddata allBackup.json
rm allBackup.json
