#once logged in to the ec2 instance run these commands

sudo apt-get update

sudo apt-get upgrade

sudo timedatectl set-timezone UTC

sudo apt-get install apache2

sudo apt-get install libapache2-mod-wsgi

sudo apt-get install postgresql postgresql-contrib

sudo -u postgres createuser -P catalog

sudo -u postgres createdb -O catalog catalog

sudo apt-get install python-sqlalchemy python-pip

sudo apt-get install python-psycopg2 python-flask

sudo apt-get install python-pandas

sudo apt-get install python-boto3

sudo apt-get install git

cd /var/www/

sudo mkdir mlwebapp

sudo chown www-data:www-data mlwebapp/

sudo -u www-data git clone https://github.com/zacktwp/MLWebApp.git mlwebapp

#replace files with
engine = create_engine('postgresql://catalog:password@localhost/catalog')

sudo mv webapp.py __init__.py


cd /var/www/

sudo nano flaskapp.wsgi

# in the flaskapp.wsgi file copy and past the below code

#start code
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/")

from mlwebapp import app as application
application.secret_key = 'Add your secret key'
#end code

#create host conf file
sudo nano /etc/apache2/sites-available/FlaskApp.conf

#copy VirtualHost block below and replace ServerName and ServerAdmin with your ec2 ip address past in the FlaskApp.conf file
<VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/www/flaskapp.wsgi
		<Directory /var/www/mlwebapp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/mlwebapp/static
		<Directory /var/www/mlwebapp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>


# run the below commands

sudo a2dissite 000-default.conf

sudo a2ensite FlaskApp

sudo service apache2 restart

sudo pip install awscli --upgrade

sudo pip install boto3 --upgrade

#error logs
cd /var/log/apache2/
sudo nano error.log

sudo nano /var/log/apache2/error.log

sudo service apache2 restart
