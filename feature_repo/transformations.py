# -*- coding: utf-8 -*-
"""
Advanced Feature Transformations for Credit Scoring

This module contains sophisticated feature engineering transformations
that can be applied to raw data to create more predictive features.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from feast.on_demand_feature_view import on_demand_feature_view
from feast.field import Field
from feast.types import Float64, Int64, String
from feast import RequestSource

# =============================================================================
# TIME-BASED TRANSFORMATIONS
# =============================================================================

def create_temporal_features(df: pd.DataFrame, timestamp_col: str = 'event_timestamp') -> pd.DataFrame:
    """
    Create time-based features from timestamp data.
    """
    df = df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    # Extract temporal components
    df['day_of_week'] = df[timestamp_col].dt.dayofweek
    df['day_of_month'] = df[timestamp_col].dt.day
    df['month'] = df[timestamp_col].dt.month
    df['quarter'] = df[timestamp_col].dt.quarter
    df['is_weekend'] = (df[timestamp_col].dt.dayofweek >= 5).astype(int)
    df['is_month_end'] = (df[timestamp_col].dt.day > 25).astype(int)
    
    # Time since features (assuming current time for demo)
    current_time = datetime.now()
    df['days_since_application'] = (current_time - df[timestamp_col]).dt.days
    df['is_recent_application'] = (df['days_since_application'] <= 30).astype(int)
    
    return df

def create_recency_features(df: pd.DataFrame, entity_col: str, event_col: str) -> pd.DataFrame:
    """
    Create features based on recency of events.
    """
    df = df.copy()
    df = df.sort_values([entity_col, event_col])
    
    # Days since last event
    df['days_since_last_event'] = df.groupby(entity_col)[event_col].diff().dt.days
    
    # Event frequency (events per month)
    df['event_frequency'] = df.groupby(entity_col).cumcount() + 1
    
    return df

# =============================================================================
# STATISTICAL TRANSFORMATIONS
# =============================================================================

def create_rolling_statistics(df: pd.DataFrame, 
                            value_cols: List[str], 
                            entity_col: str,
                            windows: List[int] = [30, 90, 180]) -> pd.DataFrame:
    """
    Create rolling window statistics for numerical features.
    """
    df = df.copy()
    
    for col in value_cols:
        for window in windows:
            # Rolling mean
            df[f'{col}_rolling_mean_{window}d'] = (
                df.groupby(entity_col)[col]
                .rolling(window=window, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
            )
            
            # Rolling standard deviation
            df[f'{col}_rolling_std_{window}d'] = (
                df.groupby(entity_col)[col]
                .rolling(window=window, min_periods=1)
                .std()
                .reset_index(level=0, drop=True)
            )
            
            # Rolling min/max
            df[f'{col}_rolling_min_{window}d'] = (
                df.groupby(entity_col)[col]
                .rolling(window=window, min_periods=1)
                .min()
                .reset_index(level=0, drop=True)
            )
            
            df[f'{col}_rolling_max_{window}d'] = (
                df.groupby(entity_col)[col]
                .rolling(window=window, min_periods=1)
                .max()
                .reset_index(level=0, drop=True)
            )
    
    return df

def create_percentile_features(df: pd.DataFrame, 
                             value_cols: List[str],
                             entity_col: str) -> pd.DataFrame:
    """
    Create percentile-based features within entity groups.
    """
    df = df.copy()
    
    for col in value_cols:
        # Percentile rank within entity
        df[f'{col}_percentile_rank'] = (
            df.groupby(entity_col)[col]
            .rank(pct=True)
        )
        
        # Z-score within entity
        entity_stats = df.groupby(entity_col)[col].agg(['mean', 'std'])
        df = df.merge(entity_stats, left_on=entity_col, right_index=True, suffixes=('', '_group'))
        df[f'{col}_zscore'] = (df[col] - df[f'{col}_mean']) / df[f'{col}_std'].fillna(1)
        
        # Drop temporary columns
        df = df.drop([f'{col}_mean', f'{col}_std'], axis=1)
    
    return df

# =============================================================================
# CATEGORICAL TRANSFORMATIONS
# =============================================================================

def create_categorical_features(df: pd.DataFrame, 
                               cat_cols: List[str],
                               target_col: Optional[str] = None) -> pd.DataFrame:
    """
    Create advanced categorical features including target encoding.
    """
    df = df.copy()
    
    for col in cat_cols:
        # Frequency encoding
        freq_map = df[col].value_counts().to_dict()
        df[f'{col}_frequency'] = df[col].map(freq_map)
        
        # Rare category indicator
        rare_threshold = 10
        df[f'{col}_is_rare'] = (df[f'{col}_frequency'] < rare_threshold).astype(int)
        
        # Target encoding (if target is provided)
        if target_col and target_col in df.columns:
            target_mean = df.groupby(col)[target_col].mean()
            df[f'{col}_target_encoded'] = df[col].map(target_mean)
    
    return df

def create_interaction_features(df: pd.DataFrame, 
                              cat_cols: List[str]) -> pd.DataFrame:
    """
    Create interaction features between categorical variables.
    """
    df = df.copy()
    
    # Create pairwise interactions
    for i, col1 in enumerate(cat_cols):
        for col2 in cat_cols[i+1:]:
            df[f'{col1}_{col2}_interaction'] = (
                df[col1].astype(str) + '_' + df[col2].astype(str)
            )
    
    return df

# =============================================================================
# FEATURE ENGINEERING PIPELINES
# =============================================================================

class FeatureEngineeringPipeline:
    """
    Pipeline for complex feature engineering operations.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.transformations = []
    
    def add_transformation(self, func, **kwargs):
        """Add a transformation function to the pipeline."""
        self.transformations.append((func, kwargs))
        return self
    
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all transformations in sequence."""
        result_df = df.copy()
        
        for func, kwargs in self.transformations:
            result_df = func(result_df, **kwargs)
        
        return result_df

# =============================================================================
# CREDIT-SPECIFIC FEATURE ENGINEERING
# =============================================================================

def create_credit_utilization_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features related to credit utilization patterns.
    """
    df = df.copy()
    
    # Assume we have credit limit information (would come from another source)
    # For demo purposes, estimate credit limits
    df['estimated_credit_limit'] = df['credit_card_due'] * 2.5  # Rough estimate
    
    # Credit utilization ratio
    df['credit_utilization_ratio'] = (
        df['credit_card_due'] / df['estimated_credit_limit'].clip(lower=1)
    ).clip(upper=1.0)
    
    # High utilization indicator
    df['high_credit_utilization'] = (df['credit_utilization_ratio'] > 0.8).astype(int)
    
    # Total debt burden
    debt_columns = ['credit_card_due', 'mortgage_due', 'student_loan_due', 'vehicle_loan_due']
    df['total_existing_debt'] = df[debt_columns].sum(axis=1)
    
    return df

def create_payment_behavior_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features that capture payment behavior patterns.
    """
    df = df.copy()
    
    # Payment trend (recent vs historical)
    df['payment_trend_6m_to_1y'] = (
        df['missed_payments_6m'] - (df['missed_payments_1y'] - df['missed_payments_6m'])
    )
    
    df['payment_trend_1y_to_2y'] = (
        df['missed_payments_1y'] - (df['missed_payments_2y'] - df['missed_payments_1y'])
    )
    
    # Payment consistency score (lower is better)
    df['payment_inconsistency_score'] = (
        df['missed_payments_6m'] * 3 +
        df['missed_payments_1y'] * 2 +
        df['missed_payments_2y'] * 1
    )
    
    # Recent payment behavior flag
    df['recent_payment_issues'] = (df['missed_payments_6m'] > 0).astype(int)
    
    # Payment improvement indicator
    df['payment_improving'] = (
        (df['missed_payments_6m'] < df['missed_payments_1y'] - df['missed_payments_6m']) &
        (df['missed_payments_1y'] < df['missed_payments_2y'] - df['missed_payments_1y'])
    ).astype(int)
    
    return df

def create_demographic_risk_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create risk features based on demographic information.
    """
    df = df.copy()
    
    # Age-based risk categories
    df['age_risk_category'] = pd.cut(
        df['person_age'], 
        bins=[0, 25, 35, 50, 65, 100], 
        labels=['very_young', 'young', 'middle', 'mature', 'senior']
    )
    
    # Income stability score
    df['income_per_year_employed'] = (
        df['person_income'] / df['person_emp_length'].clip(lower=1)
    )
    
    # Employment stability
    df['employment_stability'] = pd.cut(
        df['person_emp_length'],
        bins=[0, 1, 3, 7, 50],
        labels=['unstable', 'short_term', 'stable', 'very_stable']
    )
    
    # Home ownership risk
    ownership_risk = {
        'OWN': 1, 'MORTGAGE': 2, 'RENT': 3, 'OTHER': 4
    }
    df['home_ownership_risk_score'] = df['person_home_ownership'].map(ownership_risk)
    
    return df

# =============================================================================
# ADVANCED ON-DEMAND FEATURE VIEWS
# =============================================================================

# Enhanced request source for advanced features
advanced_request = RequestSource(
    name="advanced_application_data",
    schema=[
        Field(name='loan_amnt', dtype=Int64,
              tags={"type": "numerical", "pii": "false", "request_time": "true", "currency": "USD", "core_feature": "true"}),
        Field(name='person_income', dtype=Int64,
              tags={"type": "numerical", "pii": "true", "request_time": "true", "currency": "USD", "verification": "required"}),
        Field(name='application_channel', dtype=String,
              tags={"type": "categorical", "pii": "false", "contextual": "true", "fraud_indicator": "true", "channel": "true"}),
        Field(name='time_of_day', dtype=Int64,
              tags={"type": "numerical", "pii": "false", "temporal": "true", "behavioral": "true", "fraud_indicator": "true"}),
    ]
)

@on_demand_feature_view(
    sources=[advanced_request],
    schema=[
        Field(name='application_risk_score', dtype=Float64),
        Field(name='channel_risk_multiplier', dtype=Float64),
        Field(name='time_based_risk', dtype=Float64),
    ],
    mode="pandas",
    tags={"domain": "advanced_risk", "team": "risk", "computation": "complex"},
    description="Advanced risk scoring based on application context and timing"
)
def advanced_application_risk(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate advanced risk scores based on application context.
    """
    df = pd.DataFrame()
    
    # Channel-based risk scoring
    channel_risk = {
        'online': 1.0,
        'mobile': 1.1,
        'branch': 0.9,
        'phone': 1.2,
        'broker': 1.3
    }
    df['channel_risk_multiplier'] = features_df['application_channel'].map(channel_risk).fillna(1.0)
    
    # Time-based risk (applications outside business hours are riskier)
    business_hours = (features_df['time_of_day'] >= 9) & (features_df['time_of_day'] <= 17)
    df['time_based_risk'] = (~business_hours).astype(float) * 0.1 + 1.0
    
    # Composite application risk score
    loan_income_ratio = features_df['loan_amnt'] / features_df['person_income'].clip(lower=1)
    df['application_risk_score'] = (
        loan_income_ratio * 
        df['channel_risk_multiplier'] * 
        df['time_based_risk']
    ).clip(0, 10)
    
    return df

# =============================================================================
# FEATURE ENGINEERING CONFIGURATION
# =============================================================================

def get_feature_engineering_config() -> Dict[str, Any]:
    """
    Configuration for feature engineering pipelines.
    """
    return {
        "transformations": {
            "temporal": {
                "enabled": True,
                "features": ["day_of_week", "month", "quarter", "is_weekend"],
                "lookback_days": [30, 90, 180, 365]
            },
            "statistical": {
                "enabled": True,
                "rolling_windows": [7, 30, 90],
                "percentiles": [0.25, 0.5, 0.75, 0.9, 0.95]
            },
            "categorical": {
                "enabled": True,
                "encoding_methods": ["frequency", "target", "rare_category"],
                "interaction_depth": 2
            }
        },
        "feature_selection": {
            "enabled": True,
            "methods": ["correlation", "mutual_info", "feature_importance"],
            "max_features": 100,
            "correlation_threshold": 0.95
        },
        "validation": {
            "train_test_split": 0.8,
            "cross_validation_folds": 5,
            "feature_stability_threshold": 0.1
        }
    } 