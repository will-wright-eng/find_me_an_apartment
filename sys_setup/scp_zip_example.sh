#!/bin/bash

home_path="pi@0.0.0.0:/home/pi"
dag_path="pi@0.0.0.0:/home/pi/airflow/dags"

scp src.zip $home_path
scp dag_clist.py $dag_path