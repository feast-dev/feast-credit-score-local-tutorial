# -*- coding: utf-8 -*-
"""
Data Validation Rules for Credit Scoring Feature Store

This module defines validation rules and data quality expectations
for features used in credit risk assessment.
"""

from feast import FeatureView
from feast.dqm.profilers.ge_profiler import ge_profiler
from great_expectations.core import ExpectationSuite
from great_expectations.expectations import *
from typing import Dict, Any

# =============================================================================
# VALIDATION RULES FOR CREDIT HISTORY FEATURES
# =============================================================================

def credit_history_validation_suite() -> ExpectationSuite:
    """
    Validation rules for credit history features to ensure data quality.
    """
    suite = ExpectationSuite(expectation_suite_name="credit_history_validation")
    
    # Credit card due should be non-negative and reasonable
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="credit_card_due",
            min_value=0,
            max_value=500000,
            meta={"notes": "Credit card debt should be between $0 and $500K"}
        )
    )
    
    # Mortgage due should be non-negative
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="mortgage_due",
            min_value=0,
            max_value=2000000,
            meta={"notes": "Mortgage balance should be between $0 and $2M"}
        )
    )
    
    # Hard pulls should be reasonable (0-20 in recent period)
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="hard_pulls",
            min_value=0,
            max_value=20,
            meta={"notes": "Hard credit pulls should be reasonable"}
        )
    )
    
    # Missed payments should be non-negative
    for period in ['6m', '1y', '2y']:
        suite.add_expectation(
            ExpectColumnValuesToBeBetween(
                column=f"missed_payments_{period}",
                min_value=0,
                max_value=100,
                meta={"notes": f"Missed payments in {period} should be reasonable"}
            )
        )
    
    # Bankruptcies should be reasonable
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="bankruptcies",
            min_value=0,
            max_value=10,
            meta={"notes": "Number of bankruptcies should be reasonable"}
        )
    )
    
    return suite

# =============================================================================
# VALIDATION RULES FOR PERSON DEMOGRAPHICS
# =============================================================================

def person_demographics_validation_suite() -> ExpectationSuite:
    """
    Validation rules for person demographic features.
    """
    suite = ExpectationSuite(expectation_suite_name="person_demographics_validation")
    
    # Age should be reasonable for loan applicants
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="person_age",
            min_value=18,
            max_value=100,
            meta={"notes": "Applicant age should be between 18 and 100"}
        )
    )
    
    # Income should be positive and reasonable
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="person_income",
            min_value=1000,
            max_value=10000000,
            meta={"notes": "Annual income should be between $1K and $10M"}
        )
    )
    
    # Home ownership should be valid categories
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(
            column="person_home_ownership",
            value_set=["RENT", "OWN", "MORTGAGE", "OTHER"],
            meta={"notes": "Home ownership should be valid category"}
        )
    )
    
    # Employment length should be reasonable
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="person_emp_length",
            min_value=0,
            max_value=50,
            meta={"notes": "Employment length should be between 0 and 50 years"}
        )
    )
    
    return suite

# =============================================================================
# VALIDATION RULES FOR LOAN FEATURES
# =============================================================================

def loan_features_validation_suite() -> ExpectationSuite:
    """
    Validation rules for loan application features.
    """
    suite = ExpectationSuite(expectation_suite_name="loan_features_validation")
    
    # Loan amount should be positive and reasonable
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="loan_amnt",
            min_value=500,
            max_value=500000,
            meta={"notes": "Loan amount should be between $500 and $500K"}
        )
    )
    
    # Interest rate should be reasonable
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="loan_int_rate",
            min_value=0.01,
            max_value=50.0,
            meta={"notes": "Interest rate should be between 0.01% and 50%"}
        )
    )
    
    # Loan intent should be valid categories
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(
            column="loan_intent",
            value_set=["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", 
                      "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"],
            meta={"notes": "Loan intent should be valid category"}
        )
    )
    
    # Loan status should be 0 or 1
    suite.add_expectation(
        ExpectColumnValuesToBeInSet(
            column="loan_status",
            value_set=[0, 1],
            meta={"notes": "Loan status should be 0 (rejected) or 1 (approved)"}
        )
    )
    
    return suite

# =============================================================================
# VALIDATION RULES FOR ZIPCODE FEATURES
# =============================================================================

def zipcode_features_validation_suite() -> ExpectationSuite:
    """
    Validation rules for zipcode demographic features.
    """
    suite = ExpectationSuite(expectation_suite_name="zipcode_features_validation")
    
    # Population should be positive
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="population",
            min_value=1,
            max_value=10000000,
            meta={"notes": "Population should be positive and reasonable"}
        )
    )
    
    # Tax returns filed should be reasonable
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="tax_returns_filed",
            min_value=0,
            max_value=5000000,
            meta={"notes": "Tax returns filed should be reasonable"}
        )
    )
    
    # Total wages should be positive
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(
            column="total_wages",
            min_value=0,
            max_value=500000000000,
            meta={"notes": "Total wages should be non-negative"}
        )
    )
    
    # State should be valid US state abbreviations
    suite.add_expectation(
        ExpectColumnValuesToMatchRegex(
            column="state",
            regex="^[A-Z]{2}$",
            meta={"notes": "State should be 2-letter abbreviation"}
        )
    )
    
    return suite

# =============================================================================
# COMPOSITE VALIDATION RULES
# =============================================================================

def cross_feature_validation_rules() -> Dict[str, Any]:
    """
    Cross-feature validation rules that check relationships between features.
    """
    return {
        "debt_to_income_consistency": {
            "description": "Debt-to-income ratio should be consistent",
            "rule": "total_debt_due / person_income <= 10.0",
            "severity": "error",
            "tags": ["consistency", "financial_ratios"]
        },
        
        "age_employment_consistency": {
            "description": "Employment length should not exceed working age",
            "rule": "person_emp_length <= (person_age - 16)",
            "severity": "warning", 
            "tags": ["consistency", "demographics"]
        },
        
        "loan_income_ratio": {
            "description": "Loan amount should be reasonable relative to income",
            "rule": "loan_amnt <= (person_income * 5)",
            "severity": "warning",
            "tags": ["business_logic", "risk"]
        },
        
        "payment_history_trend": {
            "description": "Recent missed payments should not exceed historical",
            "rule": "missed_payments_6m <= missed_payments_1y <= missed_payments_2y",
            "severity": "warning",
            "tags": ["data_quality", "credit_history"]
        }
    }

# =============================================================================
# DATA PROFILING CONFIGURATION
# =============================================================================

def get_profiling_config() -> Dict[str, Any]:
    """
    Configuration for automatic data profiling and drift detection.
    """
    return {
        "profiling_schedule": "daily",
        "drift_detection": {
            "enabled": True,
            "threshold": 0.1,
            "features_to_monitor": [
                "person_income",
                "loan_amnt",
                "credit_card_due",
                "mortgage_due",
                "person_age"
            ]
        },
        "anomaly_detection": {
            "enabled": True,
            "method": "isolation_forest",
            "contamination": 0.05
        },
        "alerts": {
            "email": ["risk-team@company.com", "data-team@company.com"],
            "slack_channel": "#feature-store-alerts",
            "severity_threshold": "warning"
        }
    } 