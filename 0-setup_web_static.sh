#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static.

if ! nginx -v; then
	sudo apt-get update;
	sudo apt-get -y install nginx;
fi

if sudo ufw --version; then
	sudo ufw allow 'Nginx HTTP'
	sufo ufw allow OpenSSH
fi

sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test

echo "
<html>
  <head>
  </head>
  <body>
    Holbermton School
  </body>
</html>
" | sudo tee data/web_static/releases/test/index.html

ls -sf /data/web_static/releases/test data/web_static/current

sudo chown -Rh ubuntu:ubuntu /data

sed -i '/server_name _;/ a \ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n}' /etc/nginx/sites-available/default

sudo service nginx restart