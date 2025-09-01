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

1. Setup an online store with Redis by [Podman](https://podman.io/):  
```
podman pull docker://bitnami/redis:latest
podman run -d -p 6379:6379 --name redis -e "ALLOW_EMPTY_PASSWORD=yes"  docker.io/bitnami/redis:latest  
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

Next we load features into the online store using the `materialize-incremental` command. This command will load the
latest feature values from a data source into the online store.

```
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME
```

Alternatively, you may have to run
```
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize 1990-01-01T00:00:00  $CURRENT_TIME
```

Return to the root of the repository
```
cd ..
```

### Train and test the model

Finally, we train the model using a combination of loan data from the parque file under the `./data` folder and our zipcode and credit history features from duckdb (with Filesource). And then we test online inference by reading those same features from Redis.

```
python run.py
```
The script should then output the result of a single loan application
```
loan rejected!
```

### Serving Demo and OpenAPI docs
You can run
```bash
python app.py
```
And you'll be able to see the endpoints by going to http://127.0.0.1:8888/docs#/.


### Go Feature Server Demo
Current the Go Feature Server only supports "file", AWS "s3" and GCP "gs" storage. In this demo, we choose "file".
Steps:
1. terminate the previous running `app.py` if it is still running.  
2. start the Feast feature transformation server:
    `python app_with_transformation_server.py`  
3. start the Go feature server, assume you have built the Go binary and named it as 'feast':  
    `./feast -chdir ./feature_repo`
4. test the URI "http://localhost:8080/health". We suppose to see 'Healthy' word be displayed.   
5. test the following post for testing get-online-features. Make sure the `feast materialize` command have executed.
```
curl -X POST \
"http://localhost:8080/get-online-features" \
-d '{
    "features": [
        "zipcode_features:city",
        "zipcode_features:state",
        "zipcode_features:location_type",
        "zipcode_features:tax_returns_filed",
        "zipcode_features:population",
        "zipcode_features:total_wages",
        "credit_history:credit_card_due",
        "credit_history:mortgage_due",
        "credit_history:student_loan_due",
        "credit_history:vehicle_loan_due",
        "credit_history:hard_pulls",
        "credit_history:missed_payments_2y",
        "credit_history:missed_payments_1y",
        "credit_history:missed_payments_6m",
        "credit_history:bankruptcies",
        "total_debt_calc:total_debt_due"
    ],
    "entities": {
        "dob_ssn": [
            "19630621_4278"
        ],
        "zipcode": [
            76104
        ],
        "loan_amnt": [
            35000
        ]
    }
}' | jq
```
