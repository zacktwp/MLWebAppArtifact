### Log into ec2 and run the below commands:

`sudo apt-get update`

`sudo apt-get upgrade`

`sudo timedatectl set-timezone UTC`

`sudo apt-get install apache2`

`sudo apt-get install libapache2-mod-wsgi`

`sudo apt-get install postgresql postgresql-contrib`

create catalog db and set password to password

`sudo -u postgres createuser -P catalog`

`sudo -u postgres createdb -O catalog catalog`

`sudo apt-get install python-sqlalchemy python-pip`

`sudo apt-get install python-psycopg2 python-flask`

`sudo apt-get install python-pandas`

`sudo apt-get install python-boto3`

`sudo apt-get install git`

`cd /var/www/`

`sudo mkdir mlwebapp`

`sudo chown www-data:www-data mlwebapp/`

`sudo -u www-data git clone https://github.com/zacktwp/MLWebAppArtifact.git mlwebapp`

`cd mlwebapp`

`python database.py`

`python populatedb.py`

`sudo mv webapp.py __init__.py`

Make sure you change the SageMaker endpoint to the one you created within the __init__.py file

`cd /var/www/`

### Create wsgi file under the /var/www/ directory

`sudo nano flaskapp.wsgi`

### Copy and past the code below in the wsgi file

```python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/")

from mlwebapp import app as application
```

### Create the conf file

`sudo nano /etc/apache2/sites-available/FlaskApp.conf`

### copy code below and past in the conf file. Also be sure to past in the ip address of the ec2 instance in place of mywbsite.com

```
<VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/www/flaskapp.wsgi
		<Directory /var/www/mlwebapp/>
			Require all granted
		</Directory>
		Alias /static /var/www/mlwebapp/static
		<Directory /var/www/mlwebapp/static/>
			Require all granted
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### Run the below commands

`sudo a2dissite 000-default.conf`

`sudo a2ensite FlaskApp`

`sudo service apache2 restart`

`sudo pip install awscli --upgrade`

`sudo pip install boto3 --upgrade`

### go to the ip address in the browser and begin interacting with your website

### error logs if something goes wrong within ec2

`sudo nano /var/log/apache2/error.log`

`sudo service apache2 restart`
