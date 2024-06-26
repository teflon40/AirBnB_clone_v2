#!/usr/bin/env bash
# sets up my web servers for the deployment of web_static.

# installs nginx if it is not already installed
if [[ ! -x ${/usr/sbin/nginx} ]];
then
    sudo apt-get -y update
    sudo apt-get install -y nginx
fi

# create directories if they doesnt exist
if [[ ! -d ${/data/web_static/releases/test/} ]];
then
    sudo mkdir -p /data/web_static/releases/test/
fi

if [[ ! -d ${/data/web_static/} ]];
then
    sudo mkdir -p /data/web_static/shared/
fi

# fake html content to test nginx config
echo "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# sym-link to html content directory (test). if exists, replace with new one
ln -nsf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to the host user and group
chown -R ubuntu:ubuntu /data/

# serve the content of /data/web_static/current/ to hbnb_static

echo "
server {
        listen 80;
        listen [::]:80;

        location /hbnb_static {
          alias /data/web_static/current/;
        }
        add_header X-Served-By $HOSTNAME;

}" | sudo tee /etc/nginx/sites-enabled/default > /dev/null

sudo service nginx start
