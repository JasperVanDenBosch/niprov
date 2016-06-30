MongoDB setup
=============

This quickstart guide explains how to setup a MongoDB backend for niprov
on Ubuntu.

...incomplete..

Requires 2.6

Follow installation instructions at 

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

Configure mongodb:
::

    sudo nano /etc/mongod.conf


    # network interfaces
    net:
      port: 27017
      bindIp: 0.0.0.0


    sudo service mongod restart

