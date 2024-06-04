# Real-time Credit Scoring with Feast on Local Setup

## Overview
This tutorial is built from the original **[feast-aws-credit-scoring-tutorial](https://github.com/feast-dev/feast-aws-credit-scoring-tutorial)**.  

This tutorial demonstrates the use of Feast as part of a real-time credit scoring application.
* The primary training dataset is a loan table. This table contains historic loan data with accompanying features. The dataset also contains a target variable, namely whether a user has defaulted on their loan.
* Feast is used during training to enrich the loan table with zipcode and credit history features from the **data** folder.
* Feast is also used to serve the latest zipcode and credit history features for online credit scoring using Redis

## Requirements

* Python 3.11
* Registry: Postgresql  
* Offline Storage: duckdb  
* Online Storage: Redis

## Setup
 
Setup Postgresql and Redis by docker:  

```
docker run -d -p 5432:5432 --name postgresql -e "ALLOW_EMPTY_PASSWORD=yes" bitnami/postgresql:latest
docker run -d -p 6379:6379 --name redis  bitnami/redis:latest
```

### Setting up Feast

Install Feast using pip

```
pip install -r requirements.txt
```

We have already set up a feature repository in [feature_repo/](feature_repo/). As a result, all we have to do is configure the [feature_store.yaml/](feature_repo/feature_store.yaml) in the feature repository. Please set the connection string of the Postgresql and Redis according to your local infra setup.  

Deploy the feature store by running `apply` from within the `feature_repo/` folder
```
cd feature_repo/
feast apply
```
```
Deploying infrastructure for credit_history
Deploying infrastructure for zipcode_features
```

Next we load features into the online store using the `materialize-incremental` command. This command will load the
latest feature values from a data source into the online store.

```
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME
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

## Interactive demo (using Streamlit)

Once the credit scoring model has been trained it can be used for interactive loan applications using Streamlit:

Simply start the Streamlit application
```
streamlit run streamlit_app.py
```
Then navigate to the URL on which Streamlit is being served. You should see a user interface through which loan applications can be made:

![Streamlit Loan Application](streamlit.png)
