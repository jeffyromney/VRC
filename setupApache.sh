
sudo apt-get install apache2
sudo apt-get install libapache2-mod-php5
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install python2.7
pip install django


path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
apachePath="/etc/apache2"
echo "

ServerName VRC

Alias /static/ $path/static/


<Directory $path/static>
Require all granted
</Directory>

WSGIScriptAlias / $path/vrc/wsgi.py
WSGIPythonPath $path

<Directory $path/vrc>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
" | sudo tee $apachePath/conf-available/vrc.conf > /dev/null

a2enconf vrc
