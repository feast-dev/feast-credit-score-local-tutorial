# Real-time Credit Scoring with Feast on Local Setup

## Overview
This tutorial is built from the original **[feast-aws-credit-scoring-tutorial](https://github.com/feast-dev/feast-aws-credit-scoring-tutorial)**.  

This tutorial demonstrates the use of Feast as part of a real-time credit scoring application.
* The primary training dataset is a loan table. This table contains historic loan data with accompanying features. The dataset also contains a target variable, namely whether a user has defaulted on their loan.
* Feast is used during training to enrich the loan table with zipcode and credit history features from the **data** folder.
* Feast is also used to serve the latest zipcode and credit history features for online credit scoring using Redis

To get a better feel of what this example entails, you can view the steps outlined below in notebook 
form in [demo_walkthrough.ipynb](demo_walkthrough.ipynb).

## Requirements

* Python 3.11
* Registry: Postgresql  
* Offline Storage: duckdb  
* Online Storage: Redis

## Setup

### Database Setup
 
You can setup the storages with Podman or Docker:  

1. Setup Postgresql and Redis by [Podman](https://podman.io/):  
```
podman pull docker://bitnami/postgresql  
podman run -d -p 5432:5432 --name postgresql -e "ALLOW_EMPTY_PASSWORD=yes" docker.io/bitnami/postgresql:latest  

podman pull docker://bitnami/redis:latest
podman run -d -p 6379:6379 --name redis -e "ALLOW_EMPTY_PASSWORD=yes"  docker.io/bitnami/redis:latest  
```

Please **create** a database named "feast" for Feast's SQL Registry service. It is required by the Registry setting in the **feature_store.yaml**. Feel free to use other names, but to make sure that they are the same and consistent.

This can be done via:
1. First login into the running container:
```
podman exec -it [your_container_id] /bin/bash
```
Then run:
```bash
% psql postgresql://postgres@localhost:5432
psql (13.4, server 16.3)
WARNING: psql major version 13, server major version 16.
         Some psql features might not work.
Type "help" for help.

postgres=# create database feast
postgres-# ;
CREATE DATABASE
```

### Setting up Feast

Install Feast using uv

```
uv sync  
```

We have already set up a feature repository in [feature_repo/](feature_repo/). As a result, all we have to do is configure the [feature_store.yaml/](feature_repo/feature_store.yaml) in the feature repository. Please set the connection string of the Postgresql and Redis according to your local infra setup.  

Deploy the feature store by running `apply` from within the `feature_repo/` folder
```
cd feature_repo/
feast apply
```
If you meet the following errors:
```
ImportError: no pq wrapper available.
Attempts made:
- couldn't import psycopg 'c' implementation: No module named 'psycopg_c'
- couldn't import psycopg 'binary' implementation: No module named 'psycopg_binary'
- couldn't import psycopg 'python' implementation: libpq library not found
```
You may need to install `libpq` library of PostgreSQL.
Linux (Debian):
```
sudo apt-get install libpq-dev
```
Linux (RHEL/CentOS/Fedora)
```
sudo yum install postgresql-devel
```
macOS(Homebrew)
```
brew install postgresql
```

Next we load features into the online store using the `materialize-incremental` command. This command will load the
latest feature values from a data source into the online store.

```
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME
```

Alternatively, you may have to run
```
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize 1990-01-00T00:00:00  $CURRENT_TIME
```

Return to the root of the repository
```
cd ..
```

## Train and test the model

Finally, we train the model using a combination of loan data from the parque file under the `./data` folder and our zipcode and credit history features from duckdb (with Filesource). And then we test online inference by reading those same features from Redis.

```
python run.py
```
The script should then output the result of a single loan application
```
loan rejected!
```

## Serving Demo and OpenAPI docs

You can run
```bash
python app.py
```
And you'll be able to see the endpoints by going to http://127.0.0.1:8888/docs#/.

