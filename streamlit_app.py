import datetime
import logging
import sys
from collections import OrderedDict

import pandas as pd
import shap
import streamlit as st
from matplotlib import pyplot as plt

from credit_model import CreditScoringModel

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logging.debug("Streamlit app started.")

st.set_page_config(layout="wide")
model = CreditScoringModel()
if not model.is_model_trained():
    raise Exception("The credit scoring model has not been trained. Please run run.py.")


def get_loan_request():
    zipcode = st.sidebar.text_input("Zip code", "94109")
    date_of_birth = st.sidebar.date_input(
        "Date of birth", value=datetime.date(year=1986, day=19, month=3)
    )
    ssn_last_four = st.sidebar.text_input(
        "Last four digits of social security number", "3643"
    )
    dob_ssn = f"{date_of_birth.strftime('%Y%m%d')}_{str(ssn_last_four)}"
    age = st.sidebar.slider("Age", 0, 130, 25)
    income = st.sidebar.slider("Yearly Income", 0, 1000000, 120000)
    person_home_ownership = st.sidebar.selectbox(
        "Do you own or rent your home?", ("RENT", "MORTGAGE", "OWN")
    )

    employment = st.sidebar.slider(
        "How long have you been employed (months)?", 0, 120, 12
    )

    loan_intent = st.sidebar.selectbox(
        "Why do you want to apply for a loan?",
        (
            "PERSONAL",
            "VENTURE",
            "HOMEIMPROVEMENT",
            "EDUCATION",
            "MEDICAL",
            "DEBTCONSOLIDATION",
        ),
    )

    amount = st.sidebar.slider("Loan amount", 0, 100000, 10000)
    interest = st.sidebar.slider("Preferred interest rate", 1.0, 25.0, 12.0, step=0.1)
    return OrderedDict(
        {
            "zipcode": [int(zipcode)],
            "dob_ssn": [dob_ssn],
            "person_age": [age],
            "person_income": [income],
            "person_home_ownership": [person_home_ownership],
            "person_emp_length": [float(employment)],
            "loan_intent": [loan_intent],
            "loan_amnt": [amount],
            "loan_int_rate": [interest],
        }
    )


# Application
st.title("Loan Application")

# Input Side Bar
st.header("User input:")
loan_request = get_loan_request()
df = pd.DataFrame.from_dict(loan_request)

logging.debug(f"User input: {loan_request}")
st.write(df)

# Full feature vector
st.header("Feature vector (user input + zipcode features + user features):")
vector = model._get_online_features_from_feast(loan_request)
ordered_vector = loan_request.copy()
key_list = vector.keys()
key_list = sorted(key_list)
for vector_key in key_list:
    if vector_key not in ordered_vector:
        ordered_vector[vector_key] = vector[vector_key]
df = pd.DataFrame.from_dict(ordered_vector)

logging.debug(f"Online features from Feast: {vector}")
st.write(df)

# Results of prediction
st.header("Application Status (model prediction):")
result = model.predict(loan_request)

if result == 0:
    st.success("Your loan has been approved!")
elif result == 1:
    st.error("Your loan has been rejected!")

logging.debug(f"Model prediction result: {result}")

# Feature importance
st.header("Feature Importance")
# TODO: Load a sample dataset from feature store instead of a static file
X = pd.read_parquet("data/training_dataset_sample.parquet")
X['total_debt_due'] = (X['credit_card_due'] + X['mortgage_due'] + X['student_loan_due'] + X['vehicle_loan_due'] + X['loan_amnt']).astype(float)
explainer = shap.TreeExplainer(model.classifier)
shap_values = explainer.shap_values(X)
left, right = st.columns(2)
with left:
    fig, ax = plt.subplots()
    plt.title("Feature importance based on SHAP values")
    shap.summary_plot(shap_values[:,:,1], X)  # Select only the values for class 1
    st.pyplot(fig, bbox_inches="tight")
    st.write("---")

with right:
    fig, ax = plt.subplots()
    plt.title("Feature importance based on SHAP values (Bar)")
    shap.summary_plot(shap_values[:,:,1], X, plot_type="bar")  # Select only the values for class 1
    st.pyplot(fig, bbox_inches="tight")

logging.debug("Streamlit app finished.")
