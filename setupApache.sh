case $1 in
	-u)	echo "Purging previous Installations...."
		sudo apt-get -y purge apache2 libapache2-mod-php5 libapache2-mod-php5 libapache2-mod-wsgi libapache2-mod-php7.0
		echo "Done!";;
esac
echo "Installing Dependencies....."

sudo apt-get install -y apache2 libapache2-mod-wsgi python2.7 python-django
ubuntuVersion=$(lsb_release -r | awk '{print $2}'| sed 's/[.]//')
if [ "1604" == "$ubuntuVersion" ]; then
	sudo apt-get -y install libapache2-mod-php7.0
else
	sudo apt-get -y install libapache2-mod-php5
fi
echo "Done!"

echo "Deploying to Apache..."
path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
apachePath="/etc/apache2"
echo "

ServerName $(cat /etc/hostname)

Alias /static/ \"$path/static/\"


<Directory \"$path/static\">
Require all granted
</Directory>

WSGIScriptAlias / \"$path/vrc/wsgi.py\"
WSGIPythonPath \"$path\"

<Directory \"$path/vrc\">
<Files wsgi.py>
Require all granted
</Files>
</Directory>
" | sudo tee "$apachePath/conf-available/vrc.conf" > /dev/null

sudo a2enconf vrc
sudo service apache2 reload
echo "Done!"


echo "Setting Permissions..."
sudo addgroup webmasters
sudo adduser $USER webmasters
sudo chown -R www-data:webmasters "$path"
sudo chown -R www-data:webmasters ./db.sqlite3
sudo chmod g+x ./setupApache.sh
sudo find "$path" -type f -exec chmod 666 {} \;
sudo find "$path" -type d -exec chmod 775 {} \;
sudo find "$path" -type d -exec chmod g+s {} \;

echo "Finished Installing VRC Server"

