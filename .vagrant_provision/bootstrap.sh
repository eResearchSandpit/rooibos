#!/usr/bin/env bash

# export DEBIAN_FRONTEND=noninteractive
# set -e # Exit script immediately on first error.
set -x # Print commands and their arguments as they are executed.

echo "I am" `whoami`

echo -e "################# Provisioning vagrant box via ./vagrant_provision/bootstrap.sh #################"

# vagrant dirs
export HOME_DIR=/home/vagrant
export VAGRANT_DIR=/vagrant
export PROVISION_DIR=$VAGRANT_DIR/.vagrant_provision
export PRO_LOG=$HOME_DIR/bootstrap_logs
# MDID dirs
export MDID_DIR=$HOME_DIR/mdid
export MDID_DATA_DIR=$HOME_DIR/mdid-data
export CONFIG_DIR=$MDID_DIR/config
export ROOIBOS_DIR=$MDID_DIR/rooibos

# SQL password for root - obviously this would be stupid in a non-local non-dev context
# (the vagrant vm is set to be private network)
# do we need to say DO NOT DO THIS ON AN EXTERNALLY ACCESSIBLE DEVICE?
export SQL_PASSWORD=rooibos

##############################################################################
# A Vagrant provisioning shell script to setup an MDID Development VM
##############################################################################


##############################################################################
# Setup files and directories
##############################################################################

echo -e "################# Setting up files & directories as vagrant user #################"


# create a logs dir so verbose output of the script can be saved for review if something is not correct
mkdir -p $PRO_LOG
mkdir -p $MDID_DATA_DIR
mkdir -p $MDID_DATA_DIR/logs

# create a ln from /vagrant to our $MDID_DIR
ln -s $VAGRANT_DIR $MDID_DIR

# explicitly create the log directory, because when the workers service fires
# up later in the provisioning, if they're not there then they will get
# created by root and permissions will be all jacked up

mkdir -p $MDID_DATA_DIR/scratch/logs

# touch the log files so they work later

touch $MDID_DATA_DIR/logs/rooibos.log
touch $MDID_DATA_DIR/logs/request.log
touch $MDID_DATA_DIR/logs/sql_etc.log

echo -e "################# Making sure system & apt-get are up to date #################"

# Update our apt sources
sudo apt-get update 1>> $PRO_LOG/install.txt 2>> $PRO_LOG/install_errors.txt

# Make sure we are starting from an up-to-date system
sudo apt-get upgrade -y 1>> $PRO_LOG/install.txt 2>> $PRO_LOG/install_errors.txt
sudo apt-get dist-upgrade -y 1>> $PRO_LOG/install.txt 2>> $PRO_LOG/install_errors.txt

echo -e "################# Installing MySQL, Solr, RabbitMQ, memcached #################"

# The mysql-server package interactively prompts for the root pasword to the
# MySQL server.  These commands will cache the password settings, and they
# will be used by the mysql-server package on installation.  Since this is
# pretty insecure anyway, no attempt is made at using a secure password :)
#
# Sets the MySQL root password to '$SQL_PASSWORD' to conform to existing docs, etc.

echo -e "\n\n                  PSSST:  the mysql root password is: $SQL_PASSWORD\n\n"
echo -e "============== SQL_PASSWORD = $SQL_PASSWORD ==============" >> $PRO_LOG/db_install.txt

sudo echo mysql-server mysql-server/root_password password $SQL_PASSWORD | debconf-set-selections  1>> $PRO_LOG/db_install.txt 2>> $PRO_LOG/db_install_errors.txt
sudo echo mysql-server mysql-server/root_password_again password $SQL_PASSWORD | debconf-set-selections 1>> $PRO_LOG/db_install.txt 2>> $PRO_LOG/db_install_errors.txt

# Now we can install the packages
# mysql-server: The MySQL server
# mysql-client: The MySQL client utilities
# libmysqlclient-dev: MySQL developmental libraries, needed to build the python
#   MySQL module
sudo apt-get install -y mysql-server mysql-client libmysqlclient-dev 1>> $PRO_LOG/db_install.txt 2>> $PRO_LOG/db_install_errors.txt

##############################################################################
# Install other dependencies
##############################################################################

# Java is needed to run Solr
apt-get install -y openjdk-7-jre-headless 1>> $PRO_LOG/apt_install.txt 2>> $PRO_LOG/apt_install_errors.txt

sudo mkdir -p /usr/java
sudo ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/java/default

# Solr should probably installed, while we're at it...
sudo apt-get install -y solr-jetty 1>> apt_bootstrap_logs/install.txt 2>> $PRO_LOG/apt_install_errors.txt

# RabbitMQ is needed to manage the worker jobs
sudo apt-get install -y rabbitmq-server 1>> $PRO_LOG/apt_install.txt 2>> $PRO_LOG/apt_install_errors.txt

# Memcached is used for django's memory object cache
sudo apt-get install -y memcached 1>> $PRO_LOG/apt_install.txt 2>> $PRO_LOG/apt_install_errors.txt

# ffmpeg for video funage
# add repo for ffmpeg and install it
sudo add-apt-repository ppa:mc3man/trusty-media 1>> $PRO_LOG/apt_install.txt 2>> $PRO_LOG/apt_install_errors.txt
sudo apt-get install -y ffmpeg 1>> $PRO_LOG/install.txt 2>> $PRO_LOG/install_errors.txt

##############################################################################
# Python build dependencies
##############################################################################

echo -e "################# Installing python things that require apt-get #################"

sudo apt-get install -y python-dev 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt

# PyODBC needs the unixodbc libs
sudo apt-get install -y unixodbc unixodbc-dev 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt

# python-ldap needs ldap and sasl libraries
sudo apt-get install -y libldap2-dev libsasl2-dev 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt

# Pillow needs image libraries
sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt

##############################################################################
# Configure Python and setup a Virtual Environment
##############################################################################
# Use PIP for python package management

echo -e "################# Configuring Python and setting up Virtual Environment #################"

sudo apt-get install -y python-pip 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt

# in case the ubuntu repo lags behind pip, upgrade it!
sudo pip install -U pip 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt

echo -e "################# Installing virtualenv software #################"

# install virtualenv
# as per docs, virtualenv & vewrapper should only be installed in a system install of python
# http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation

mkdir -p $HOME_DIR/.virtualenvs

export WORKON_HOME=$HOME_DIR/.virtualenvs

sudo pip install --upgrade virtualenv 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt
sudo pip install --upgrade virtualenvwrapper 1>> $PRO_LOG/python_install.txt 2>> $PRO_LOG/python_install_errors.txt

## add git autocomplete, git prompt and a few other niceties to the cmd line
## and stick in a .bash-profile to autosource them

sudo apt-get install git bash-completion 1>> $PRO_LOG/install.txt 2>> $PRO_LOG/install_errors.txt
# cp $PROVISION_DIR/.bash-completion $HOME_DIR
cp $PROVISION_DIR/.git-prompt $HOME_DIR
cp $PROVISION_DIR/.mdid-funcs $HOME_DIR
cp $PROVISION_DIR/.bash_aliases $HOME_DIR/
cp $PROVISION_DIR/.my.cnf $HOME_DIR

# copy a little helper script for running the django dev server
cp $PROVISION_DIR/runserver $HOME_DIR/

source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv -a $MDID_DIR -r $MDID_DIR/requirements.txt mdid 1>> $PRO_LOG/venv_install.txt 2>> $PRO_LOG/venv_install_errors.txt
workon mdid

echo `which python`
# install our requirements in case the above one fails... ?
# deactivate; workon mdid; pip install --upgrade -r requirements.txt 1>> $PRO_LOG/install.txt 2>> $PRO_LOG/install_errors.txt

sudo chown -R vagrant:vagrant /home/vagrant/

##############################################################################
# Configure MDID
##############################################################################
### alternative - run not in a script
#$MY_SQLS -e  "DROP DATABASE IF EXISTS rooibos;"
#$MY_SQLS -e  "CREATE DATABASE IF NOT EXISTS rooibos CHARACTER SET utf8;"
#$MY_SQLS -e  "GRANT ALL PRIVILEGES ON rooibos.* TO rooibos@localhost IDENTIFIED BY 'rooibos';"
#$MY_SQLS -e  "UPDATE mysql.user SET  Select_priv='Y', Insert_priv='Y',
#              Update_priv='Y', Delete_priv='Y', Create_priv='Y', Drop_priv='Y',
#              Index_priv='Y', Alter_priv='y'
#              WHERE Host='localhost' AND User='rooibos';"
#$MY_SQLS -e  "FLUSH PRIVILEGES;"

# you can load the schema to work around current weird migrations problems
# mysql -u root -p$SQL_PASSWORD < /vagrant/.vagrant_provision/mdid_schema.sql

## save settings_local.py from template if there is none
if [ ! -f $CONFIG_DIR/settings_local.py ]; then
#  # backup any existing local settings first
  echo "~~~ no settings_local.py so let's make a fresh one from settings_local_template.py ~~~"
  cp -n $CONFIG_DIR/settings_local_template.py $CONFIG_DIR/settings_local.py
else
  echo "~~~ settings_local.py exists so using it, \e[91m make sure your settings are correct \e[21m ~~~"
fi

### replaced this in settings_local_template.py so that we don't accidently mess up someone's settings_local.py
## Get the default gateway IP address so we can add it to INTERNAL_IPS
#GATEWAY_IP=`route -n | grep 'UG' | awk '{print $2}'`
### backup settings_local.py
#cp -n $CONFIG_DIR/settings_local.py $CONFIG_DIR/settings_loc.backup.py
### filter our local settings template, replacing necessary values
#cat $CONFIG_DIR/settings_local.py | sed -e "s/<<GATEWAY_IP>>/$GATEWAY_IP/" > $CONFIG_DIR/settings_local.py
echo "running /vagrant/.vagrant_provision/create_database.sql now" >> $PRO_LOG/db_install.txt
mysql --user=root --password=$SQL_PASSWORD -v < /vagrant/.vagrant_provision/create_database.sql 1>> $PRO_LOG/db_install.txt 2>> $PRO_LOG/db_install_errors.txt

echo "showing grants" >> $PRO_LOG/db_install.txt
mysql --user=rooibos --password=$SQL_PASSWORD -v -e "show grants; show tables;" rooibos 1>> $PRO_LOG/db_install.txt 2>> $PRO_LOG/db_install_errors.txt

# make manage.py executable like "./mangage.py syncdb"
chmod +x $MDID_DIR/manage.py

# setup the app using full paths to the correct python and correct manage.py
MDID_PY=$WORKON_HOME/mdid/bin/python

# create rooibos specific tables
$MDID_PY $MDID_DIR/manage.py migrate rooibos --noinput  1>> $PRO_LOG/mdid_install.txt 2>> $PRO_LOG/mdid_install_errors.txt
# make sure all apps (including unmigrated apps) are processed
$MDID_PY $MDID_DIR/manage.py migrate --noinput 1>> $PRO_LOG/mdid_install.txt 2>> $PRO_LOG/mdid_install_errors.txt
# copy static files from all the apps into settings.STATIC_DIR
$MDID_PY $MDID_DIR/manage.py collectstatic --noinput 1>> $PRO_LOG/mdid_install.txt 2>> $PRO_LOG/mdid_install_errors.txt

echo -e "################# Adding Upstart scripts for Solr and the Workers #################"
sudo cp $PROVISION_DIR/mdid3-*.conf /etc/init

sudo chown -R vagrant:vagrant /home/vagrant/

echo -e "################# Starting Up Services #################"
# start up the services
service mdid3-solr start
service mdid3-workers start

echo -e "### COMPLETED ###"
echo -e "You can start the mdid server from your desktop via"
echo -e "   vagrant ssh -c \"~/runserver\""
