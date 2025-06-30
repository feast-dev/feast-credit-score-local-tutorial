# Credit Scoring Feature Store - Complete Resource Guide

This document provides a comprehensive overview of all resource types and capabilities in our enhanced credit scoring feature store.

## 🎯 Overview

The feature store has been enhanced with multiple resource types to support comprehensive credit risk assessment, including:
- **3 Entities** with comprehensive metadata tags
- **3 Data Sources** with source system and quality tags
- **4 Feature Views** covering different data domains with detailed field tags
- **4 On-Demand Feature Views** for computed features
- **4 Feature Services** for different use cases
- **4 Saved Datasets** covering training, analysis, profiling, and comprehensive workflows
- **Data Validation Rules** for quality assurance
- **Advanced Transformations** for feature engineering
- **Comprehensive Tagging Strategy** across all resource types
- **Streaming capabilities** (ready to add when Kafka infrastructure is available)

## 📊 Resource Types Inventory

### 🔑 Entities

| Entity | Type | Description | Domain | PII | Sensitivity |
|--------|------|-------------|---------|-----|-------------|
| `zipcode` | INT64 | Geographic identifier | Geography | No | Stable |
| `dob_ssn` | STRING | Customer identifier | Customer | Yes | Critical |
| `loan_id` | STRING | Loan application identifier | Loan | No | Transactional |

### 📋 Data Sources

| Source | Type | Source System | Update Frequency | Quality | Cost/Sensitivity |
|--------|------|---------------|------------------|---------|------------------|
| `zipcode_source` | FileSource | Census Bureau | Annual | High | Public/Low |
| `credit_history_source` | FileSource | Credit Bureau | Daily | Critical | High/High |
| `loan_table_source` | FileSource | Loan Origination | Real-time | High | Internal/Critical |

### 🏗️ Feature Views

#### Core Feature Views

1. **`zipcode_features`** - Geographic Demographics
   - **Fields**: city, state, location_type, tax_returns_filed, population, total_wages
   - **TTL**: 3650 days
   - **Use Case**: Geographic risk assessment
   - **Tags**: demographics, census data

2. **`credit_history`** - Credit Bureau Data  
   - **Fields**: credit_card_due, mortgage_due, student_loan_due, vehicle_loan_due, hard_pulls, missed_payments_*
   - **TTL**: 90 days
   - **Use Case**: Payment behavior analysis
   - **Tags**: credit, PII, critical freshness

3. **`person_demographics`** - Personal Information
   - **Fields**: person_age, person_income, person_home_ownership, person_emp_length
   - **TTL**: 365 days
   - **Use Case**: Demographic risk factors
   - **Tags**: demographics, PII

4. **`loan_features`** - Loan Characteristics
   - **Fields**: loan_intent, loan_amnt, loan_int_rate, loan_status
   - **TTL**: 90 days
   - **Use Case**: Loan-specific risk assessment
   - **Tags**: loan, application data

#### Stream Feature View (Available for future enhancement)

*Streaming feature views can be added when Kafka infrastructure is configured*

### ⚡ On-Demand Feature Views

1. **`total_debt_calc`** - Debt Aggregation
   - **Output**: total_debt_due
   - **Logic**: Sum of all existing debts + new loan amount
   - **Use Case**: Debt burden analysis

2. **`financial_ratios`** - Key Financial Ratios
   - **Output**: debt_to_income_ratio, loan_to_income_ratio
   - **Logic**: Financial ratio calculations
   - **Use Case**: Creditworthiness assessment

3. **`risk_scores`** - Composite Risk Scoring
   - **Output**: risk_score, payment_stability_score
   - **Logic**: Multi-factor risk scoring algorithm
   - **Use Case**: ML model features

4. **`advanced_application_risk`** - Context-Aware Risk
   - **Output**: application_risk_score, channel_risk_multiplier, time_based_risk
   - **Logic**: Application context and timing analysis
   - **Use Case**: Fraud detection, behavioral analysis

### 💾 Saved Datasets

#### Training & Development Datasets

1. **`credit_score_training_v1`** - Zipcode Features Training Data
   - **Features**: 6 zipcode-based features (city, state, location_type, tax_returns_filed, population, total_wages)
   - **Purpose**: Model training with geographic and demographic data
   - **Author**: ML_Team
   - **Quality**: Production-grade

2. **`credit_history_analysis_v1`** - Credit History Analysis
   - **Features**: 6 credit features (credit_card_due, mortgage_due, student_loan_due, vehicle_loan_due, hard_pulls, missed_payments_6m)
   - **Purpose**: Credit risk analysis and debt assessment
   - **Author**: Risk_Team
   - **Quality**: Production-grade

#### Demographics & Profiling Datasets

3. **`demographics_profile_v1`** - Demographics Profiling
   - **Features**: 4 demographic features (person_age, person_income, person_home_ownership, person_emp_length)
   - **Purpose**: Customer profiling and demographic analysis
   - **Author**: Data_Team
   - **Quality**: Production-grade

#### Comprehensive Analysis Datasets

4. **`comprehensive_credit_dataset_v1`** - Multi-Feature Analysis
   - **Features**: 6 mixed features (population, total_wages, credit_card_due, missed_payments_6m, person_income, person_age)
   - **Purpose**: Comprehensive credit scoring with multiple data sources
   - **Author**: ML_Team
   - **Model Type**: credit_scoring
   - **Quality**: Production-grade

### 🛠️ Feature Services

1. **`credit_assessment_v1`** - Core Credit Scoring
   - **Features**: credit_history, person_demographics, debt calculations, risk scores
   - **Use Case**: Primary loan approval decisions
   - **Team**: risk-team

2. **`geographic_analysis_v1`** - Location-Based Analysis
   - **Features**: zipcode_features, person_demographics
   - **Use Case**: Geographic risk patterns
   - **Team**: risk-team

3. **`realtime_scoring_v1`** - Low-Latency Scoring
   - **Features**: on-demand calculations, quick ratios
   - **Use Case**: Fast batch scoring (streaming ready)
   - **Team**: risk-team

4. **`portfolio_analysis_v1`** - Portfolio Management
   - **Features**: loan_features, credit_history, geographic data, risk scores
   - **Use Case**: Portfolio risk monitoring
   - **Team**: analytics-team

## 🔍 Data Quality & Validation

### Validation Rules by Domain

#### Credit History Validation
- Credit card debt: $0 - $500K
- Mortgage balance: $0 - $2M  
- Hard pulls: 0-20 reasonable range
- Missed payments: Non-negative, reasonable counts
- Bankruptcies: 0-10 range

#### Demographics Validation  
- Age: 18-100 years for loan applicants
- Income: $1K - $10M annual range
- Home ownership: Valid categories (RENT, OWN, MORTGAGE, OTHER)
- Employment length: 0-50 years

#### Loan Features Validation
- Loan amount: $500 - $500K
- Interest rate: 0.01% - 50%
- Loan intent: Valid categories
- Status: Binary (0/1)

#### Cross-Feature Validation
- Debt-to-income consistency
- Age-employment logical checks
- Loan-to-income reasonableness
- Payment history trends

## 🎨 Advanced Feature Engineering

### Transformation Categories

1. **Time-Based Features**
   - Day of week, month, quarter
   - Weekend indicators
   - Days since application
   - Recency features

2. **Statistical Features**
   - Rolling statistics (mean, std, min, max)
   - Percentile rankings
   - Z-scores within groups
   - Window-based calculations

3. **Categorical Features**
   - Frequency encoding
   - Target encoding
   - Rare category indicators
   - Interaction features

4. **Credit-Specific Features**
   - Credit utilization ratios
   - Payment behavior patterns
   - Demographic risk categories
   - Stability scores

## 💾 Saved Dataset Management

### Creating and Using Saved Datasets

```python
from feast import FeatureStore
from feast.data_format import ParquetFormat
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
import pandas as pd

# Initialize feature store
store = FeatureStore(repo_path=".")

# Create entity DataFrame
entity_df = pd.DataFrame([
    {"dob_ssn": "19790429_9552", "zipcode": 30721, "event_timestamp": pd.Timestamp("2023-03-15")},
    {"dob_ssn": "19971025_8002", "zipcode": 48893, "event_timestamp": pd.Timestamp("2023-06-20")},
])

# Get historical features
features = [
    "zipcode_features:population",
    "zipcode_features:total_wages",
    "credit_history:credit_card_due",
    "person_demographics:person_income",
]

historical_job = store.get_historical_features(
    entity_df=entity_df,
    features=features,
)

# Create saved dataset
store.create_saved_dataset(
    from_=historical_job,
    name="credit_score_training_v1",
    storage=SavedDatasetFileStorage(
        path="data/credit_score_training_v1", 
        file_format=ParquetFormat()
    ),
    tags={'author': 'ML_Team', 'purpose': 'training', 'version': 'v1'},
    allow_overwrite=True
)

# Verify creation
saved_dataset = store.get_saved_dataset("credit_score_training_v1")
print(f"Created dataset: {saved_dataset.name}")
```

### Quick Start: Create All Datasets

To create all saved datasets that will be visible in the Feast UI:

```bash
# Navigate to feature repo directory
cd feature_repo

# Run the dataset creation script
python create_ui_visible_datasets.py

# Start Feast UI to view datasets
feast ui
```

The script will create 4 SavedDatasets:
- `credit_score_training_v1` - Training data with zipcode features
- `credit_history_analysis_v1` - Credit history analysis
- `demographics_profile_v1` - Demographics profiling
- `comprehensive_credit_dataset_v1` - Multi-feature comprehensive analysis

All datasets will be properly registered with Feast and visible in the UI at `http://localhost:8888`.

### Dataset Usage Patterns

#### 1. Model Training Workflow
```python
# Load training dataset
training_ds = store.get_saved_dataset("credit_score_training_v1")
training_df = training_ds.to_df()

# Prepare for ML training
features = [col for col in training_df.columns if col not in ['dob_ssn', 'zipcode', 'event_timestamp']]
X = training_df[features]
y = training_df['loan_status']  # Add target from your data warehouse

# Train model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)
```

#### 2. Batch Scoring Pipeline
```python
# Load credit history dataset for scoring
scoring_ds = store.get_saved_dataset("credit_history_analysis_v1")
scoring_df = scoring_ds.to_df()

# Apply model predictions
predictions = model.predict_proba(scoring_df)[:, 1]
scoring_df['credit_score'] = predictions

# Store results back to data warehouse
scoring_df.to_sql('loan_scores', connection, if_exists='append')
```

#### 3. Feature Quality Monitoring
```python
# Load comprehensive dataset for quality monitoring
quality_ds = store.get_saved_dataset("comprehensive_credit_dataset_v1")
quality_df = quality_ds.to_df()

# Check for data drift
from scipy import stats
baseline_income = quality_df['person_demographics__person_income'].iloc[:10]
recent_income = quality_df['person_demographics__person_income'].iloc[-10:]

# Statistical test for drift
statistic, p_value = stats.ks_2samp(baseline_income, recent_income)
drift_detected = p_value < 0.05

if drift_detected:
    print("⚠️ Data drift detected in person_income feature")
```

#### 4. Demographics Analysis
```python
# Load demographics dataset
demographics_ds = store.get_saved_dataset("demographics_profile_v1")
demographics_df = demographics_ds.to_df()

# Generate demographic report
demographic_features = ['person_age', 'person_income', 'person_home_ownership', 'person_emp_length']
demographic_report = {
    'total_profiles': len(demographics_df),
    'avg_age': demographics_df['person_demographics__person_age'].mean(),
    'avg_income': demographics_df['person_demographics__person_income'].mean(),
    'feature_distributions': {
        feature: demographics_df[f'person_demographics__{feature}'].describe().to_dict()
        for feature in demographic_features if f'person_demographics__{feature}' in demographics_df.columns
    }
}
```

#### 5. Multi-Dataset Analysis
```python
# Load multiple datasets for comprehensive analysis
datasets = [
    "credit_score_training_v1",
    "credit_history_analysis_v1", 
    "demographics_profile_v1",
    "comprehensive_credit_dataset_v1"
]

dataset_info = {}
for dataset_name in datasets:
    try:
        ds = store.get_saved_dataset(dataset_name)
        df = ds.to_df()
        dataset_info[dataset_name] = {
            'rows': len(df),
            'columns': len(df.columns),
            'features': [col for col in df.columns if col not in ['dob_ssn', 'zipcode', 'event_timestamp']]
        }
        print(f"✅ {dataset_name}: {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        print(f"❌ {dataset_name}: {e}")
```

### Dataset Tagging and Discovery

```python
# Search datasets by tags
def find_datasets_by_tag(store: FeatureStore, tag_key: str, tag_value: str):
    """Find saved datasets by specific tag."""
    dataset_names = [
        "credit_score_training_v1",
        "credit_history_analysis_v1", 
        "demographics_profile_v1",
        "comprehensive_credit_dataset_v1"
    ]
    matching_datasets = []
    
    for dataset_name in dataset_names:
        try:
            dataset = store.get_saved_dataset(dataset_name)
            if hasattr(dataset, 'tags') and dataset.tags.get(tag_key) == tag_value:
                matching_datasets.append(dataset_name)
        except Exception as e:
            print(f"Could not access {dataset_name}: {e}")
    
    return matching_datasets

# Find datasets by purpose
training_datasets = find_datasets_by_tag(store, "purpose", "training")
print(f"Training datasets: {training_datasets}")

# Find datasets by author
ml_team_datasets = find_datasets_by_tag(store, "author", "ML_Team")
print(f"ML team datasets: {ml_team_datasets}")

# Find datasets by version
v1_datasets = find_datasets_by_tag(store, "version", "v1")
print(f"Version 1 datasets: {v1_datasets}")

# List all available datasets with their tags
print("\n📊 All Available Datasets:")
for dataset_name in ["credit_score_training_v1", "credit_history_analysis_v1", 
                     "demographics_profile_v1", "comprehensive_credit_dataset_v1"]:
    try:
        dataset = store.get_saved_dataset(dataset_name)
        print(f"✅ {dataset.name}")
        if hasattr(dataset, 'tags') and dataset.tags:
            print(f"   Tags: {dataset.tags}")
    except Exception as e:
        print(f"❌ {dataset_name}: {e}")
```

## 📈 Usage Examples

### Basic Feature Retrieval
```python
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# Get historical features for training
entity_df = pd.DataFrame({
    "dob_ssn": ["19790429_9552", "19971025_8002"],
    "event_timestamp": [datetime.now(), datetime.now()]
})

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "credit_history:credit_card_due",
        "credit_history:missed_payments_6m",
        "person_demographics:person_income",
        "total_debt_calc:total_debt_due"
    ]
).to_df()
```

### Feature Service Usage
```python
# Use pre-defined feature service
features = store.get_online_features(
    features=store.get_feature_service("credit_assessment_v1"),
    entity_rows=[{
        "dob_ssn": "19790429_9552",
        "loan_amnt": 5000,
        "person_income": 50000
    }]
).to_dict()
```

### Real-time Scoring
```python
# Real-time feature retrieval
realtime_features = store.get_online_features(
    features=store.get_feature_service("realtime_scoring_v1"),
    entity_rows=[{
        "loan_id": "loan_12345",
        "loan_amnt": 10000,
        "person_income": 75000
    }]
)
```

### Feature Discovery by Tags
```python
# Find all PII features for compliance review
pii_features = []
for fv in store.list_feature_views():
    for field in fv.schema:
        if field.tags.get("pii") == "true":
            pii_features.append(f"{fv.name}:{field.name}")

# Find high-risk features for model monitoring
high_risk_features = []
for fv in store.list_feature_views():
    for field in fv.schema:
        if field.tags.get("risk_factor") == "critical":
            high_risk_features.append(f"{fv.name}:{field.name}")

# Find on-demand computed features by feature view tags
computed_feature_views = []
for fv in store.list_on_demand_feature_views():
    if fv.tags.get("computation") == "derived":
        computed_feature_views.append(fv.name)

# Find PII entities for privacy compliance
pii_entities = []
for entity in store.list_entities():
    if entity.tags.get("pii") == "true":
        pii_entities.append(entity.name)

# Find external data sources for vendor management
external_sources = []
for ds in store.list_data_sources():
    if ds.tags.get("external") == "true":
        external_sources.append({"name": ds.name, "system": ds.tags.get("source_system")})

# Find high-cost data sources for budget planning
high_cost_sources = []
for ds in store.list_data_sources():
    if ds.tags.get("cost") == "high":
        high_cost_sources.append(ds.name)
```

## 🏷️ Comprehensive Tagging Strategy

**Note**: Tags are currently supported on Feature Views and Request Sources. On-Demand Feature View outputs use feature view-level tags for governance.

### Feature-Level Tags

#### Data Type Classification
- `type`: "numerical", "categorical", "binary", "count", "ratio", "score", "multiplier"
- `currency`: "USD" for monetary values
- `percentage`: "true" for rate-based features

#### Privacy & Compliance
- `pii`: "true"/"false" - Personally identifiable information
- `regulatory`: "age_verification", "dti" (debt-to-income), compliance requirements
- `verification`: "required" for features needing validation

#### Risk Assessment
- `risk_factor`: "low", "medium", "high", "critical" - Risk impact level
- `risk_indicator`: "true" for direct risk signals
- `payment_behavior`: "negative", "positive" for payment-related features

#### Business Context
- `debt_type`: "revolving", "secured", "installment" - Type of debt
- `time_window`: "6m", "1y", "2y" - Time period for temporal features
- `stability_indicator`: "true" for features indicating stability
- `core_feature`: "true" for essential features

#### Technical Metadata
- `computed`: "true" for derived/calculated features
- `request_time`: "true" for real-time inputs
- `time_sensitive`: "true" for features with temporal importance
- `aggregated`: "true" for aggregated data

#### Feature Usage
- `target`: "true" for outcome variables
- `ml_feature`: "true" for machine learning inputs
- `fraud_detection`: "true" for fraud-related features
- `segmentation`: "true" for customer segmentation

#### Domain-Specific Tags
- `geographic`: "true" for location-based features
- `economic_indicator`: "true" for economic metrics
- `demographic`: "true" for population characteristics
- `financial`: "true" for financial metrics
- `employment`: "true" for employment-related data
- `contextual`: "true" for context-aware features
- `behavioral`: "true" for behavioral analysis
- `temporal`: "true" for time-based features

### Feature View-Level Tags
- `domain`: "demographics", "credit", "loan", "risk"
- `team`: "risk-team", "analytics-team" - Ownership
- `source`: "census", "credit_bureau", "application", "stream"
- `freshness`: "critical" for time-sensitive data
- `use_case`: "credit_scoring", "geographic_risk", "portfolio_management"

### Entity-Level Tags
- `domain`: "geography", "customer", "loan" - Business domain
- `pii`: "true"/"false" - Privacy classification
- `join_key`: "true" - Used for feature joins
- `cardinality`: "high", "medium", "low" - Number of unique values
- `stability`: "stable", "changing" - Rate of change
- `sensitive`: "critical", "high", "medium" - Sensitivity level
- `regulatory`: "privacy_protected" - Compliance requirements
- `business_key`: "true" - Core business identifier
- `transactional`: "true" - Transaction-level entity

### Data Source-Level Tags  
- `source_system`: "census_bureau", "credit_bureau", "loan_origination" - Origin system
- `data_type`: "reference", "transactional", "operational" - Data category
- `update_frequency`: "annual", "daily", "real_time" - Refresh rate
- `quality`: "critical", "high", "medium" - Data quality requirement
- `external`: "true"/"false" - External vs internal data
- `internal`: "true"/"false" - Internal system data
- `sensitive`: "high", "medium", "low" - Sensitivity classification
- `cost`: "high", "medium", "low" - Data acquisition cost
- `public_data`: "true" - Publicly available data
- `business_critical`: "true" - Critical for operations
- `latency`: "low", "medium", "high" - Access latency requirements

## 🔧 Configuration Management

All configurations are centralized in dedicated modules:
- `validations.py`: Data quality rules and expectations
- `transformations.py`: Feature engineering pipelines
- `features.py`: Core feature definitions

## 🚀 Next Steps

1. **Deploy the enhanced feature store**: Apply configurations to your Feast deployment
2. **Set up monitoring**: Implement data quality monitoring and alerting
3. **Feature discovery**: Use tags and metadata for team collaboration
4. **Model integration**: Connect ML models to feature services
5. **Performance optimization**: Monitor and tune feature retrieval performance

## 📞 Support & Ownership

| Component | Owner | Contact |
|-----------|-------|---------|
| Core Features | risk-team | risk-team@company.com |
| Portfolio Analysis | analytics-team | analytics-team@company.com |
| Infrastructure | data-team | data-team@company.com |
| Feature Engineering | ml-team | ml-team@company.com |

---

*This feature store implementation follows MLOps best practices and provides a comprehensive foundation for credit risk assessment and decision making.* 