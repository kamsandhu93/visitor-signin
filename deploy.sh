#!/bin/bash
sudo mkdir /opt/visitor-db
sudo cp visitor_db.db /opt/visitor-db/
sudo docker-compose up --build
