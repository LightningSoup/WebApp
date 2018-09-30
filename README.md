# Lightning Soup

Lightning Soup is a content management and collaboration for the decentralized web. This repository implements a simple web server that allows for the uploading, management, and tracking of content on IPFS.

## Use Cases
Lightning Soup is meant to be an easy-to-use frontend for IPFS. If you don't want to host your own instance, you may feel free to use mine at https://lightning-soup.herokuapp.com/.

## Requirements
In order to run your own Lightning Soup frontend, you will need:
 - An IPFS Daemon
 - A web server for running this code

You will need to install Python3.6 to host a Lightning Soup instance, along with several packages. Installation instructions are below:

### Installation on Ubuntu 14.04

First, install Python and Pip:

`sudo apt-get install python3 python3-pip`

Next, install relevant Python packages:

`sudo pip3 install Django==2.0.7`
Django version 2.0.7 is necessary, since version 2.1 does not work with the default installation of Python3.

`sudo pip3 install gunicorn whitenoise ipfsapi dj-database-url psycopg2-binary django-heroku`

After this succeeds, installation should be complete.

## Testing
To run the Lightning Soup instance, first make sure that you have an IPFS daemon running. You can do this by executing the command `ipfs daemon` in another terminal window. This will start the IPFS backend, which needs to be running constantly while your Lightning Soup instance is up.

You can then start the Lightning Soup server with the command:
`python3 manage.py runserver 0.0.0.0:8000`
This will run the server on port 8000, and allow connections from other machines as long as your IP has been added to `ALLOWED_HOSTS` in `settings.py`.

## Deployment
Lightning Soup is made to be run as a [Heroku](https://heroku.com/apps) application, but other means of deployment should also work. Instructions for deployment coming soon!

# Contributing
Lightning Soup is currently an alpha project under heavy development, and desperately needs your help!

If you find anything wrong with the code in this repository or would like to recommend features, please create an issue on this Github page.

If you have fixed an issue, please commit your code to a separate branch and submit a merge request into master.

Thank you for any help!
