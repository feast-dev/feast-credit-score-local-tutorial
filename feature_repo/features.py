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
from feast import RequestSource, FeatureService

from typing import Any

# Note: Streaming features (KafkaSource, StreamFeatureView) are commented out
# for compatibility. Uncomment and configure when streaming infrastructure is ready.
# 
# from feast.stream_feature_view import StreamFeatureView
# from feast.data_format import JsonFormat
# from feast.data_source import KafkaSource

# =============================================================================
# ENTITIES
# =============================================================================

zipcode = Entity(
    name="zipcode", 
    value_type=ValueType.INT64,
    description="ZIP code identifier for geographic location-based features",
    tags={"domain": "geography", "pii": "false", "join_key": "true", "cardinality": "high", "stability": "stable", "standardized": "true"}
)

dob_ssn = Entity(
    name="dob_ssn",
    value_type=ValueType.STRING,
    description="Unique identifier combining date of birth and last four digits of SSN for customer identification",
    tags={"domain": "customer", "pii": "true", "join_key": "true", "cardinality": "high", "sensitive": "critical", "regulatory": "privacy_protected"}
)

loan_id = Entity(
    name="loan_id",
    value_type=ValueType.STRING,
    description="Unique identifier for each loan application",
    tags={"domain": "loan", "pii": "false", "join_key": "true", "cardinality": "high", "business_key": "true", "transactional": "true"}
)

# =============================================================================
# DATA SOURCES
# =============================================================================

zipcode_source = FileSource(
    name="Zipcode source",
    path="data/zipcode_table.parquet",
    file_format=ParquetFormat(),
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
    description="Geographic and demographic data aggregated by ZIP code",
    tags={"source_system": "census_bureau", "data_type": "reference", "update_frequency": "annual", "quality": "high", "external": "true", "public_data": "true"}
)

credit_history_source = FileSource(
    name="Credit history",
    path="data/credit_history.parquet",
    file_format=ParquetFormat(),
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
    description="Historical credit data including payment history and outstanding debts",
    tags={"source_system": "credit_bureau", "data_type": "transactional", "update_frequency": "daily", "quality": "critical", "external": "true", "sensitive": "high", "cost": "high"}
)

loan_table_source = FileSource(
    name="Loan table",
    path="data/loan_table.parquet",
    file_format=ParquetFormat(),
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
    description="Loan application data including personal and loan characteristics",
    tags={"source_system": "loan_origination", "data_type": "operational", "update_frequency": "real_time", "quality": "high", "internal": "true", "business_critical": "true", "latency": "low"}
)

# Streaming sources removed for compatibility
# Add back when streaming infrastructure is ready

# =============================================================================
# FEATURE VIEWS
# =============================================================================

zipcode_features = FeatureView(
    name="zipcode_features",
    entities=[zipcode],
    ttl=timedelta(days=3650),
    schema=[
        Field(name="city", dtype=String, description="City name for the ZIP code", 
              tags={"type": "categorical", "pii": "false", "geographic": "true", "enrichment": "location"}),
        Field(name="state", dtype=String, description="State abbreviation for the ZIP code",
              tags={"type": "categorical", "pii": "false", "geographic": "true", "standardized": "true"}),
        Field(name="location_type", dtype=String, description="Type of location (urban, suburban, rural)",
              tags={"type": "categorical", "pii": "false", "risk_factor": "geographic", "segmentation": "true"}),
        Field(name="tax_returns_filed", dtype=Int64, description="Number of tax returns filed in the ZIP code area",
              tags={"type": "numerical", "pii": "false", "economic_indicator": "true", "aggregated": "true"}),
        Field(name="population", dtype=Int64, description="Total population in the ZIP code area",
              tags={"type": "numerical", "pii": "false", "demographic": "true", "density_indicator": "true"}),
        Field(name="total_wages", dtype=Int64, description="Total wages earned in the ZIP code area",
              tags={"type": "numerical", "pii": "false", "economic_indicator": "true", "income_proxy": "true"}),
    ],
    source=zipcode_source,
    tags={"domain": "demographics", "team": "risk", "pii": "false", "source": "census"},
    description="Geographic and demographic features aggregated by ZIP code for credit risk assessment",
    owner="risk-team@company.com"
)

credit_history = FeatureView(
    name="credit_history",
    entities=[dob_ssn],
    ttl=timedelta(days=90),
    schema=[
        Field(name="credit_card_due", dtype=Int64, description="Outstanding credit card balance",
              tags={"type": "numerical", "pii": "true", "debt_type": "revolving", "risk_factor": "high", "currency": "USD"}),
        Field(name="mortgage_due", dtype=Int64, description="Outstanding mortgage balance",
              tags={"type": "numerical", "pii": "true", "debt_type": "secured", "risk_factor": "medium", "currency": "USD"}),
        Field(name="student_loan_due", dtype=Int64, description="Outstanding student loan balance",
              tags={"type": "numerical", "pii": "true", "debt_type": "installment", "risk_factor": "medium", "currency": "USD"}),
        Field(name="vehicle_loan_due", dtype=Int64, description="Outstanding vehicle loan balance",
              tags={"type": "numerical", "pii": "true", "debt_type": "secured", "risk_factor": "medium", "currency": "USD"}),
        Field(name="hard_pulls", dtype=Int64, description="Number of hard credit inquiries in recent period",
              tags={"type": "count", "pii": "true", "risk_factor": "high", "time_sensitive": "true", "inquiry_type": "hard"}),
        Field(name="missed_payments_2y", dtype=Int64, description="Number of missed payments in the last 2 years",
              tags={"type": "count", "pii": "true", "risk_factor": "critical", "time_window": "2y", "payment_behavior": "negative"}),
        Field(name="missed_payments_1y", dtype=Int64, description="Number of missed payments in the last 1 year",
              tags={"type": "count", "pii": "true", "risk_factor": "critical", "time_window": "1y", "payment_behavior": "negative"}),
        Field(name="missed_payments_6m", dtype=Int64, description="Number of missed payments in the last 6 months",
              tags={"type": "count", "pii": "true", "risk_factor": "critical", "time_window": "6m", "payment_behavior": "negative"}),
        Field(name="bankruptcies", dtype=Int64, description="Number of bankruptcy filings on record",
              tags={"type": "count", "pii": "true", "risk_factor": "critical", "legal_status": "true", "credit_event": "major"}),
    ],
    source=credit_history_source,
    tags={"domain": "credit", "team": "risk", "pii": "true", "source": "credit_bureau", "freshness": "critical"},
    description="Credit history features including payment behavior, outstanding debts, and credit inquiries for risk assessment",
    owner="risk-team@company.com"
)

# New: Person Demographics Features
person_demographics = FeatureView(
    name="person_demographics",
    entities=[dob_ssn],
    ttl=timedelta(days=365),
    schema=[
        Field(name="person_age", dtype=Int64, description="Age of the loan applicant",
              tags={"type": "numerical", "pii": "true", "demographic": "true", "risk_factor": "medium", "regulatory": "age_verification"}),
        Field(name="person_income", dtype=Int64, description="Annual income of the applicant",
              tags={"type": "numerical", "pii": "true", "financial": "true", "risk_factor": "high", "currency": "USD", "verification": "required"}),
        Field(name="person_home_ownership", dtype=String, description="Home ownership status (RENT, OWN, MORTGAGE, OTHER)",
              tags={"type": "categorical", "pii": "true", "stability_indicator": "true", "risk_factor": "medium", "asset_type": "real_estate"}),
        Field(name="person_emp_length", dtype=Float64, description="Employment length in years",
              tags={"type": "numerical", "pii": "true", "stability_indicator": "true", "risk_factor": "medium", "employment": "true"}),
    ],
    source=loan_table_source,
    tags={"domain": "demographics", "team": "risk", "pii": "true", "source": "application", "update_frequency": "monthly"},
    description="Personal demographic and employment information for creditworthiness assessment",
    owner="risk-team@company.com"
)

# New: Loan Characteristics Features
loan_features = FeatureView(
    name="loan_features",
    entities=[loan_id],
    ttl=timedelta(days=90),
    schema=[
        Field(name="loan_intent", dtype=String, description="Purpose of the loan (EDUCATION, MEDICAL, VENTURE, etc.)",
              tags={"type": "categorical", "pii": "false", "risk_factor": "medium", "business_logic": "true", "segmentation": "true"}),
        Field(name="loan_amnt", dtype=Int64, description="Requested loan amount",
              tags={"type": "numerical", "pii": "false", "risk_factor": "high", "currency": "USD", "core_feature": "true"}),
        Field(name="loan_int_rate", dtype=Float64, description="Interest rate for the loan",
              tags={"type": "numerical", "pii": "false", "risk_indicator": "true", "percentage": "true", "pricing": "true"}),
        Field(name="loan_status", dtype=Int64, description="Loan approval status (0=rejected, 1=approved)",
              tags={"type": "binary", "pii": "false", "target": "true", "outcome": "true", "decision": "final"}),
    ],
    source=loan_table_source,
    tags={"domain": "loan", "team": "risk", "pii": "false", "source": "application"},
    description="Loan application characteristics and terms for risk evaluation",
    owner="risk-team@company.com"
)

# =============================================================================
# REQUEST SOURCES
# =============================================================================

input_request = RequestSource(
    name="application_data",
    schema=[
        Field(name='loan_amnt', dtype=Int64, description="Requested loan amount from the application",
              tags={"type": "numerical", "pii": "false", "request_time": "true", "currency": "USD", "core_feature": "true"}),
        Field(name='person_income', dtype=Int64, description="Applicant's annual income",
              tags={"type": "numerical", "pii": "true", "request_time": "true", "currency": "USD", "verification": "required"}),
    ],
    description="Real-time loan application data provided at inference time"
)

# =============================================================================
# ON-DEMAND FEATURE VIEWS
# =============================================================================

@on_demand_feature_view(
   sources=[
       credit_history,
       input_request,
   ],
   schema=[
     Field(name='total_debt_due', dtype=Float64),
   ],
   mode="pandas",
   tags={"domain": "credit", "team": "risk", "computation": "derived", "category": "debt_ratio"},
   description="Calculated total debt burden including existing debts and new loan amount for debt-to-income analysis",
   owner="risk-team@company.com"
)
def total_debt_calc(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total debt burden by combining existing debt obligations with new loan amount.
    
    This feature is critical for debt-to-income ratio calculations and overall creditworthiness assessment.
    """
    df = pd.DataFrame()
    df['total_debt_due'] = (
        features_df['credit_card_due'] + features_df['mortgage_due'] + 
        features_df['student_loan_due'] + features_df['vehicle_loan_due'] + 
        features_df['loan_amnt']
    ).astype(float)
    return df 

@on_demand_feature_view(
    sources=[
        credit_history,
        person_demographics,
        input_request,
    ],
         schema=[
        Field(name='debt_to_income_ratio', dtype=Float64),
        Field(name='loan_to_income_ratio', dtype=Float64),
     ],
    mode="pandas",
    tags={"domain": "risk", "team": "risk", "computation": "derived", "category": "ratios"},
    description="Financial ratios for assessing borrower's ability to repay",
    owner="risk-team@company.com"
)
def financial_ratios(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate key financial ratios for credit risk assessment.
    """
    df = pd.DataFrame()
    
    # Calculate total debt including existing debts and new loan
    total_existing_debt = (
        features_df['credit_card_due'] + features_df['mortgage_due'] + 
        features_df['student_loan_due'] + features_df['vehicle_loan_due']
    )
    total_debt_with_loan = total_existing_debt + features_df['loan_amnt']
    
    df['debt_to_income_ratio'] = (
        total_debt_with_loan / features_df['person_income']
    ).astype(float)
    df['loan_to_income_ratio'] = (
        features_df['loan_amnt'] / features_df['person_income']
    ).astype(float)
    return df

@on_demand_feature_view(
    sources=[
        credit_history,
        person_demographics,
    ],
         schema=[
        Field(name='risk_score', dtype=Float64),
        Field(name='payment_stability_score', dtype=Float64),
     ],
    mode="pandas",
    tags={"domain": "ml", "team": "risk", "computation": "derived", "category": "scores"},
    description="Derived risk scores for credit decision making",
    owner="risk-team@company.com"
)
def risk_scores(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate composite risk scores based on multiple factors.
    """
    df = pd.DataFrame()
    
    # Simple risk scoring logic (in practice, this would be more sophisticated)
    payment_risk = (
        features_df['missed_payments_6m'] * 3 +
        features_df['missed_payments_1y'] * 2 +
        features_df['missed_payments_2y'] * 1 +
        features_df['bankruptcies'] * 10
    )
    
    income_stability = features_df['person_emp_length'] / (features_df['person_age'] - 18)
    
    df['payment_stability_score'] = (100 - payment_risk).clip(0, 100).astype(float)
    df['risk_score'] = (
        df['payment_stability_score'] * 0.6 +
        income_stability * 40
    ).clip(0, 100).astype(float)
    
    return df

# =============================================================================
# FEATURE SERVICES
# =============================================================================

# Core credit assessment service
credit_assessment_service = FeatureService(
    name="credit_assessment_v1",
    features=[
        credit_history,
        person_demographics,
        total_debt_calc,
        financial_ratios,
        risk_scores,
    ],
    tags={"team": "risk", "version": "v1", "use_case": "credit_scoring"},
    description="Complete feature set for credit risk assessment and loan approval decisions",
    owner="risk-team@company.com"
)

# Geographic analysis service
geographic_analysis_service = FeatureService(
    name="geographic_analysis_v1",
    features=[
        zipcode_features,
        person_demographics,
    ],
    tags={"team": "risk", "version": "v1", "use_case": "geographic_risk"},
    description="Features for analyzing geographic and demographic risk patterns",
    owner="risk-team@company.com"
)

# Real-time scoring service (using batch features for now)
# Add streaming features when available
realtime_scoring_service = FeatureService(
    name="realtime_scoring_v1",
    features=[
        total_debt_calc,
        financial_ratios,
        # loan_applications_realtime,  # Uncomment when streaming is ready
    ],
    tags={"team": "risk", "version": "v1", "use_case": "real_time_scoring", "latency": "low"},
    description="Low-latency feature set for real-time credit scoring decisions (currently using batch features)",
    owner="risk-team@company.com"
)

# Loan portfolio analysis service
portfolio_analysis_service = FeatureService(
    name="portfolio_analysis_v1",
    features=[
        loan_features,
        credit_history,
        zipcode_features,
        risk_scores,
    ],
    tags={"team": "analytics", "version": "v1", "use_case": "portfolio_management"},
    description="Feature set for loan portfolio analysis and risk monitoring",
    owner="analytics-team@company.com"
)

# =============================================================================
# SIMPLE FEATURE SERVICES (No On-Demand Features - For Saved Datasets)
# =============================================================================

# Simple credit history service (batch features only)
credit_history_service = FeatureService(
    name="credit_history_v1",
    features=[
        credit_history,
    ],
    tags={"team": "risk", "version": "v1", "use_case": "credit_analysis", "complexity": "simple"},
    description="Simple credit history feature set for historical analysis and model training",
    owner="risk-team@company.com"
)

# Demographics analysis service (batch features only)
demographics_service = FeatureService(
    name="demographics_v1", 
    features=[
        person_demographics,
    ],
    tags={"team": "analytics", "version": "v1", "use_case": "demographic_analysis", "complexity": "simple"},
    description="Demographic feature set for customer profiling and segmentation",
    owner="analytics-team@company.com"
)

# Location intelligence service (batch features only)
location_intelligence_service = FeatureService(
    name="location_intelligence_v1",
    features=[
        zipcode_features,
    ],
    tags={"team": "risk", "version": "v1", "use_case": "location_analysis", "complexity": "simple"},
    description="Geographic feature set for location-based risk assessment and market analysis",
    owner="risk-team@company.com"
)

# Combined demographic and location service (batch features only)
customer_profile_service = FeatureService(
    name="customer_profile_v1",
    features=[
        person_demographics,
        zipcode_features,
    ],
    tags={"team": "marketing", "version": "v1", "use_case": "customer_profiling", "complexity": "simple"},
    description="Combined demographic and geographic features for comprehensive customer profiling",
    owner="marketing-team@company.com"
)

# Credit and demographics combined service (batch features only)
basic_underwriting_service = FeatureService(
    name="basic_underwriting_v1", 
    features=[
        credit_history,
        person_demographics,
    ],
    tags={"team": "underwriting", "version": "v1", "use_case": "basic_underwriting", "complexity": "simple"},
    description="Basic underwriting feature set combining credit history and demographics",
    owner="underwriting-team@company.com"
)

