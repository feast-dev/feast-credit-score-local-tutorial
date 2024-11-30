# -*- coding: utf-8 -*-

from datetime import timedelta

import pandas as pd
from feast.value_type import ValueType
from feast.entity import Entity
from feast.types import String, Int64, Float64
from feast.feature_view import FeatureView
from feast.on_demand_feature_view import on_demand_feature_view
from feast.field import Field
from feast.infra.offline_stores.file_source import FileSource
from feast.data_format import ParquetFormat
from feast import RequestSource
from typing import Any

zipcode = Entity(name="zipcode", value_type=ValueType.INT64)

zipcode_source = FileSource(
    name="Zipcode source",
    path="data/zipcode_table.parquet",
    file_format=ParquetFormat(),
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

zipcode_features = FeatureView(
    name="zipcode_features",
    entities=[zipcode],
    ttl=timedelta(days=3650),
    schema=[
        Field(name="city", dtype=String),
        Field(name="state", dtype=String),
        Field(name="location_type", dtype=String),
        Field(name="tax_returns_filed", dtype=Int64),
        Field(name="population", dtype=Int64),
        Field(name="total_wages", dtype=Int64),
    ],
    source=zipcode_source,
)

dob_ssn = Entity(
    name="dob_ssn",
    value_type=ValueType.STRING,
    description="Date of birth and last four digits of social security number",
)

credit_history_source = FileSource(
    name="Credit history",
    path="data/credit_history.parquet",
    file_format=ParquetFormat(),
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

credit_history = FeatureView(
    name="credit_history",
    entities=[dob_ssn],
    ttl=timedelta(days=90),
    schema=[
        Field(name="credit_card_due", dtype=Int64),
        Field(name="mortgage_due", dtype=Int64),
        Field(name="student_loan_due", dtype=Int64),
        Field(name="vehicle_loan_due", dtype=Int64),
        Field(name="hard_pulls", dtype=Int64),
        Field(name="missed_payments_2y", dtype=Int64),
        Field(name="missed_payments_1y", dtype=Int64),
        Field(name="missed_payments_6m", dtype=Int64),
        Field(name="bankruptcies", dtype=Int64),
    ],
    source=credit_history_source,
)

input_request = RequestSource(
    name="application_data",
    schema=[
        Field(name='loan_amnt', dtype=Int64),
    ]
)

@on_demand_feature_view(
   sources=[
       credit_history,
       input_request,
   ],
   schema=[
     Field(name='total_debt_due', dtype=Float64),
   ],
   mode="pandas",
)
def total_debt_calc(features_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df['total_debt_due'] = (
        features_df['credit_card_due'] + features_df['mortgage_due'] + 
        features_df['student_loan_due'] + features_df['vehicle_loan_due'] + 
        features_df['loan_amnt']
    ).astype(float)
    return df 

