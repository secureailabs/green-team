#!/bin/bash

# Start the local mongodb database
mongod --port 27017 --dbpath /srv/mongodb/db0 --bind_ip localhost --fork --logpath /var/log/mongod.log

# Start the Public API Server
cd /
ls apiservice
. /.venv/bin/activate
cd apiservice
uvicorn main:server --host 0.0.0.0 --port 8000 --reload
