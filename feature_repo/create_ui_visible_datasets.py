"""
Create Feast SavedDatasets that are visible in the UI using the proven approach.
Only includes working datasets - problematic feature services with on-demand features removed.

This script demonstrates multiple approaches to creating SavedDatasets:

INDIVIDUAL FEATURE DATASETS (4 examples):
- credit_score_training_v1: Zipcode features for training
- credit_history_analysis_v1: Credit history features for analysis
- demographics_profile_v1: Demographics features for profiling
- comprehensive_credit_dataset_v1: Mixed features from multiple views

FEATURE SERVICE DATASETS (5 examples):
- credit_history_service_v1: Simple credit history analysis (credit_history_v1 service)
- demographics_service_v1: Demographic analysis (demographics_v1 service)
- location_intelligence_service_v1: Geographic analysis (location_intelligence_v1 service)
- customer_profile_service_v1: Combined demo + geo (customer_profile_v1 service)
- basic_underwriting_service_v1: Credit + demo combo (basic_underwriting_v1 service)

KEY FIX: Uses feature_service parameter in create_saved_dataset() to preserve
feature service relationships in the UI instead of showing individual features.
"""

from feast import FeatureStore
from datetime import datetime, timezone
import pandas as pd
from feast.data_format import ParquetFormat
from feast.saved_dataset import SavedDataset
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage

def create_ui_visible_datasets():
    """Create SavedDatasets that will be visible in the Feast UI."""
    print("🏦 Creating UI-Visible Feast SavedDatasets")
    print("=" * 60)

    # Initialize feature store
    store = FeatureStore(repo_path=".")

    # Dataset 1: Training Dataset with Zipcode Features
    print("\n1. Creating Training Dataset with Zipcode Features...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19790429_9552", "zipcode": 30721, "event_timestamp": pd.Timestamp("2023-03-15")},
            {"dob_ssn": "19971025_8002", "zipcode": 48893, "event_timestamp": pd.Timestamp("2023-06-20")},
            {"dob_ssn": "19670812_9247", "zipcode": 24092, "event_timestamp": pd.Timestamp("2023-09-10")},
        ])

        feature_refs = [
            "zipcode_features:city",
            "zipcode_features:state",
            "zipcode_features:location_type",
            "zipcode_features:tax_returns_filed",
            "zipcode_features:population",
            "zipcode_features:total_wages",
        ]

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Features: {feature_refs}")

        training_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs,
        )

        print("   Retrieved historical features successfully")
        print("   Sample data:")
        sample_data = training_df.to_df().head()
        print(sample_data.to_string())

        # Create the saved dataset
        store.create_saved_dataset(
            from_=training_df,
            name="credit_score_training_v1",
            storage=SavedDatasetFileStorage(
                path="data/credit_score_training_v1",
                file_format=ParquetFormat()
            ),
            tags={'author': 'ML_Team', 'purpose': 'training', 'version': 'v1'},
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: credit_score_training_v1")

        # Verify it was created
        saved_dataset = store.get_saved_dataset("credit_score_training_v1")
        print(f"   ✅ Verified: {saved_dataset.name}")

    except Exception as e:
        print(f"   ❌ Error creating training dataset: {e}")

    # Dataset 2: Credit History Dataset
    print("\n2. Creating Credit History Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19790429_9552", "zipcode": 30721, "event_timestamp": pd.Timestamp("2023-04-01")},
            {"dob_ssn": "19971025_8002", "zipcode": 48893, "event_timestamp": pd.Timestamp("2023-07-15")},
        ])

        feature_refs = [
            "credit_history:credit_card_due",
            "credit_history:student_loan_due",
            "credit_history:vehicle_loan_due",
            "credit_history:hard_pulls",
            "credit_history:missed_payments_6m",
        ]

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Features: {feature_refs}")

        credit_history_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs,
        )

        print("   Retrieved historical features successfully")
        sample_data = credit_history_df.to_df().head()
        print("   Sample data:")
        print(sample_data.to_string())

        store.create_saved_dataset(
            from_=credit_history_df,
            name="credit_history_analysis_v1",
            storage=SavedDatasetFileStorage(
                path="data/credit_history_analysis_v1",
                file_format=ParquetFormat()
            ),
            tags={'author': 'Risk_Team', 'purpose': 'analysis', 'version': 'v1'},
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: credit_history_analysis_v1")

        saved_dataset = store.get_saved_dataset("credit_history_analysis_v1")
        print(f"   ✅ Verified: {saved_dataset.name}")

    except Exception as e:
        print(f"   ❌ Error creating credit history dataset: {e}")

    # Dataset 3: Demographics Dataset
    print("\n3. Creating Demographics Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19790429_9552", "zipcode": 30721, "event_timestamp": pd.Timestamp("2023-05-10")},
            {"dob_ssn": "19971025_8002", "zipcode": 48893, "event_timestamp": pd.Timestamp("2023-08-25")},
            {"dob_ssn": "19670812_9247", "zipcode": 24092, "event_timestamp": pd.Timestamp("2023-11-05")},
        ])

        feature_refs = [
            "person_demographics:person_age",
            "person_demographics:person_income",
            "person_demographics:person_home_ownership",
            "person_demographics:person_emp_length",
        ]

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Features: {feature_refs}")

        demographics_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs,
        )

        print("   Retrieved historical features successfully")
        sample_data = demographics_df.to_df().head()
        print("   Sample data:")
        print(sample_data.to_string())

        store.create_saved_dataset(
            from_=demographics_df,
            name="demographics_profile_v1",
            storage=SavedDatasetFileStorage(
                path="data/demographics_profile_v1",
                file_format=ParquetFormat()
            ),
            tags={'author': 'Data_Team', 'purpose': 'profiling', 'version': 'v1'},
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: demographics_profile_v1")

        saved_dataset = store.get_saved_dataset("demographics_profile_v1")
        print(f"   ✅ Verified: {saved_dataset.name}")

    except Exception as e:
        print(f"   ❌ Error creating demographics dataset: {e}")

    # Dataset 4: Comprehensive Dataset
    print("\n4. Creating Comprehensive Feature Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19790429_9552", "zipcode": 30721, "event_timestamp": pd.Timestamp("2023-06-01")},
            {"dob_ssn": "19971025_8002", "zipcode": 48893, "event_timestamp": pd.Timestamp("2023-09-15")},
        ])

        # Mix of features from different feature views
        feature_refs = [
            "zipcode_features:population",
            "zipcode_features:total_wages",
            "credit_history:credit_card_due",
            "credit_history:missed_payments_6m",
            "person_demographics:person_income",
            "person_demographics:person_age",
        ]

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Features: {feature_refs}")

        comprehensive_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs,
        )

        print("   Retrieved historical features successfully")
        sample_data = comprehensive_df.to_df().head()
        print("   Sample data:")
        print(sample_data.to_string())

        store.create_saved_dataset(
            from_=comprehensive_df,
            name="comprehensive_credit_dataset_v1",
            storage=SavedDatasetFileStorage(
                path="data/comprehensive_credit_dataset_v1",
                file_format=ParquetFormat()
            ),
            tags={'author': 'ML_Team', 'purpose': 'comprehensive_analysis', 'version': 'v1'},
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: comprehensive_credit_dataset_v1")

        saved_dataset = store.get_saved_dataset("comprehensive_credit_dataset_v1")
        print(f"   ✅ Verified: {saved_dataset.name}")

    except Exception as e:
        print(f"   ❌ Error creating comprehensive dataset: {e}")

    # Summary
    print("\n5. Summary of Individual Feature Datasets...")
    individual_datasets = [
        "credit_score_training_v1",
        "credit_history_analysis_v1",
        "demographics_profile_v1",
        "comprehensive_credit_dataset_v1"
    ]

    print("   📊 Created Individual Feature Datasets:")
    successful_count = 0
    for dataset_name in individual_datasets:
        try:
            dataset = store.get_saved_dataset(dataset_name)
            print(f"   ✅ {dataset.name}")
            if hasattr(dataset, 'tags') and dataset.tags:
                author_tag = dataset.tags.get('author', 'N/A')
                purpose_tag = dataset.tags.get('purpose', 'N/A')
                print(f"      Author: {author_tag}, Purpose: {purpose_tag}")
            successful_count += 1
        except Exception as e:
            print(f"   ❌ {dataset_name}: {e}")

    print(f"\n🎉 Individual Dataset Creation Complete!")
    print(f"   Successfully created {successful_count}/{len(individual_datasets)} datasets")
    print(f"   All datasets use reliable batch features without on-demand dependencies")

def create_working_feature_service_datasets():
    """Create multiple working feature service datasets (no on-demand features)."""
    print("🚀 Creating Working Feature Service-Based Datasets")
    print("=" * 60)

    # Initialize feature store
    store = FeatureStore(repo_path=".")

    # Dataset 1: Credit History Service Dataset
    print("\n1. Creating Credit History Service Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19530219_5179", "event_timestamp": pd.Timestamp("2023-03-15")},
            {"dob_ssn": "19781116_7723", "event_timestamp": pd.Timestamp("2023-06-20")},
            {"dob_ssn": "19931128_5771", "event_timestamp": pd.Timestamp("2023-09-10")},
        ])

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Using feature service: credit_history_v1")

        feature_service = store.get_feature_service("credit_history_v1")

        credit_history_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_service,
        )

        print("   Retrieved historical features successfully")
        try:
            sample_data = credit_history_df.to_df().head()
            print("   Sample data:")
            print(sample_data.to_string() if not sample_data.empty else "   (No data returned)")
        except Exception as e:
            print(f"   Sample data display failed: {e}")

        store.create_saved_dataset(
            from_=credit_history_df,
            name="credit_history_service_v1",
            storage=SavedDatasetFileStorage(
                path="data/credit_history_service_v1",
                file_format=ParquetFormat()
            ),
            feature_service=feature_service,
            tags={
                'author': 'Risk_Team',
                'purpose': 'credit_analysis',
                'version': 'v1',
                'feature_service': 'credit_history_v1',
                'use_case': 'credit_analysis',
                'complexity': 'simple',
                'team': 'risk'
            },
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: credit_history_service_v1")

    except Exception as e:
        print(f"   ❌ Error creating credit history service dataset: {e}")

    # Dataset 2: Demographics Service Dataset
    print("\n2. Creating Demographics Service Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19530219_5179", "event_timestamp": pd.Timestamp("2023-04-01")},
            {"dob_ssn": "19781116_7723", "event_timestamp": pd.Timestamp("2023-07-15")},
            {"dob_ssn": "19931128_5771", "event_timestamp": pd.Timestamp("2023-10-20")},
        ])

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Using feature service: demographics_v1")

        feature_service = store.get_feature_service("demographics_v1")

        demographics_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_service,
        )

        print("   Retrieved historical features successfully")
        try:
            sample_data = demographics_df.to_df().head()
            print("   Sample data:")
            print(sample_data.to_string() if not sample_data.empty else "   (No data returned)")
        except Exception as e:
            print(f"   Sample data display failed: {e}")

        store.create_saved_dataset(
            from_=demographics_df,
            name="demographics_service_v1",
            storage=SavedDatasetFileStorage(
                path="data/demographics_service_v1",
                file_format=ParquetFormat()
            ),
            feature_service=feature_service,
            tags={
                'author': 'Analytics_Team',
                'purpose': 'demographic_analysis',
                'version': 'v1',
                'feature_service': 'demographics_v1',
                'use_case': 'demographic_analysis',
                'complexity': 'simple',
                'team': 'analytics'
            },
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: demographics_service_v1")

    except Exception as e:
        print(f"   ❌ Error creating demographics service dataset: {e}")

    # Dataset 3: Location Intelligence Service Dataset
    print("\n3. Creating Location Intelligence Service Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"zipcode": 30721, "event_timestamp": pd.Timestamp("2023-05-10")},
            {"zipcode": 48893, "event_timestamp": pd.Timestamp("2023-08-25")},
            {"zipcode": 24092, "event_timestamp": pd.Timestamp("2023-11-05")},
        ])

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Using feature service: location_intelligence_v1")

        feature_service = store.get_feature_service("location_intelligence_v1")

        location_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_service,
        )

        print("   Retrieved historical features successfully")
        try:
            sample_data = location_df.to_df().head()
            print("   Sample data:")
            print(sample_data.to_string() if not sample_data.empty else "   (No data returned)")
        except Exception as e:
            print(f"   Sample data display failed: {e}")

        store.create_saved_dataset(
            from_=location_df,
            name="location_intelligence_service_v1",
            storage=SavedDatasetFileStorage(
                path="data/location_intelligence_service_v1",
                file_format=ParquetFormat()
            ),
            feature_service=feature_service,
            tags={
                'author': 'Risk_Team',
                'purpose': 'location_analysis',
                'version': 'v1',
                'feature_service': 'location_intelligence_v1',
                'use_case': 'location_analysis',
                'complexity': 'simple',
                'team': 'risk'
            },
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: location_intelligence_service_v1")

    except Exception as e:
        print(f"   ❌ Error creating location intelligence service dataset: {e}")

    # Dataset 4: Customer Profile Service Dataset (Combined)
    print("\n4. Creating Customer Profile Service Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19530219_5179", "zipcode": 30721, "event_timestamp": pd.Timestamp("2023-06-01")},
            {"dob_ssn": "19781116_7723", "zipcode": 48893, "event_timestamp": pd.Timestamp("2023-09-15")},
            {"dob_ssn": "19931128_5771", "zipcode": 24092, "event_timestamp": pd.Timestamp("2023-12-01")},
        ])

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Using feature service: customer_profile_v1")

        feature_service = store.get_feature_service("customer_profile_v1")

        customer_profile_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_service,
        )

        print("   Retrieved historical features successfully")
        try:
            sample_data = customer_profile_df.to_df().head()
            print("   Sample data:")
            print(sample_data.to_string() if not sample_data.empty else "   (No data returned)")
        except Exception as e:
            print(f"   Sample data display failed: {e}")

        store.create_saved_dataset(
            from_=customer_profile_df,
            name="customer_profile_service_v1",
            storage=SavedDatasetFileStorage(
                path="data/customer_profile_service_v1",
                file_format=ParquetFormat()
            ),
            feature_service=feature_service,
            tags={
                'author': 'Marketing_Team',
                'purpose': 'customer_profiling',
                'version': 'v1',
                'feature_service': 'customer_profile_v1',
                'use_case': 'customer_profiling',
                'complexity': 'simple',
                'team': 'marketing'
            },
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: customer_profile_service_v1")

    except Exception as e:
        print(f"   ❌ Error creating customer profile service dataset: {e}")

    # Dataset 5: Basic Underwriting Service Dataset
    print("\n5. Creating Basic Underwriting Service Dataset...")
    try:
        entity_df = pd.DataFrame([
            {"dob_ssn": "19530219_5179", "event_timestamp": pd.Timestamp("2023-07-01")},
            {"dob_ssn": "19781116_7723", "event_timestamp": pd.Timestamp("2023-10-15")},
        ])

        print(f"   Entity DataFrame shape: {entity_df.shape}")
        print(f"   Using feature service: basic_underwriting_v1")

        feature_service = store.get_feature_service("basic_underwriting_v1")

        underwriting_df = store.get_historical_features(
            entity_df=entity_df,
            features=feature_service,
        )

        print("   Retrieved historical features successfully")
        try:
            sample_data = underwriting_df.to_df().head()
            print("   Sample data:")
            print(sample_data.to_string() if not sample_data.empty else "   (No data returned)")
        except Exception as e:
            print(f"   Sample data display failed: {e}")

        store.create_saved_dataset(
            from_=underwriting_df,
            name="basic_underwriting_service_v1",
            storage=SavedDatasetFileStorage(
                path="data/basic_underwriting_service_v1",
                file_format=ParquetFormat()
            ),
            feature_service=feature_service,
            tags={
                'author': 'Underwriting_Team',
                'purpose': 'basic_underwriting',
                'version': 'v1',
                'feature_service': 'basic_underwriting_v1',
                'use_case': 'basic_underwriting',
                'complexity': 'simple',
                'team': 'underwriting'
            },
            allow_overwrite=True
        )

        print("   ✅ Created saved dataset: basic_underwriting_service_v1")

    except Exception as e:
        print(f"   ❌ Error creating basic underwriting service dataset: {e}")

    # Summary of Working Feature Service Datasets
    print("\n6. Summary of Working Feature Service Datasets...")
    working_service_datasets = [
        "credit_history_service_v1",
        "demographics_service_v1",
        "location_intelligence_service_v1",
        "customer_profile_service_v1",
        "basic_underwriting_service_v1"
    ]

    print("   📊 Created Working Feature Service Datasets:")
    successful_count = 0
    for dataset_name in working_service_datasets:
        try:
            dataset = store.get_saved_dataset(dataset_name)
            print(f"   ✅ {dataset.name}")
            if hasattr(dataset, 'tags') and dataset.tags:
                feature_service_tag = dataset.tags.get('feature_service', 'N/A')
                purpose_tag = dataset.tags.get('purpose', 'N/A')
                team_tag = dataset.tags.get('team', 'N/A')
                print(f"      Service: {feature_service_tag}, Purpose: {purpose_tag}, Team: {team_tag}")
            successful_count += 1
        except Exception as e:
            print(f"   ❌ {dataset_name}: {e}")

    print(f"\n🎉 Working Feature Service Dataset Creation Complete!")
    print(f"   Successfully created {successful_count}/{len(working_service_datasets)} datasets")
    print(f"   ✅ Used feature_service parameter to preserve service relationship in UI")
    print(f"   📋 Datasets should now show as created from feature services, not individual features")
    print(f"   🏷️  Each dataset demonstrates different use cases and team ownership patterns")

def create_all_working_datasets():
    """Create both individual feature datasets and working feature service datasets."""
    print("🏦 Creating Working Dataset Suite")
    print("=" * 60)

    # Create individual feature datasets
    create_ui_visible_datasets()

    print("\n" + "="*60)

    # Create working feature service datasets
    create_working_feature_service_datasets()

    # Final summary
    print("\n" + "="*60)
    print("📊 WORKING DATASET SUMMARY")
    print("="*60)

    store = FeatureStore(repo_path=".")

    individual_datasets = [
        "credit_score_training_v1",
        "credit_history_analysis_v1",
        "demographics_profile_v1",
        "comprehensive_credit_dataset_v1"
    ]

    working_service_datasets = [
        "credit_history_service_v1",
        "demographics_service_v1",
        "location_intelligence_service_v1",
        "customer_profile_service_v1",
        "basic_underwriting_service_v1"
    ]

    print("\n📋 Individual Feature Datasets:")
    individual_success = 0
    for dataset_name in individual_datasets:
        try:
            dataset = store.get_saved_dataset(dataset_name)
            print(f"   ✅ {dataset.name}")
            individual_success += 1
        except Exception as e:
            print(f"   ❌ {dataset_name}: Not found")

    print("\n🚀 Working Feature Service Datasets:")
    service_success = 0
    for dataset_name in working_service_datasets:
        try:
            dataset = store.get_saved_dataset(dataset_name)
            print(f"   ✅ {dataset.name}")
            service_success += 1
        except Exception as e:
            print(f"   ❌ {dataset_name}: Not found")

    total_success = individual_success + service_success
    total_possible = len(individual_datasets) + len(working_service_datasets)
    print(f"\n🎯 Total: {total_success}/{total_possible} Working SavedDatasets created")
    print(f"💡 All datasets are now visible in the Feast UI at: http://localhost:8888")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "services":
            create_working_feature_service_datasets()
        elif sys.argv[1] == "individual":
            create_ui_visible_datasets()
        elif sys.argv[1] == "all":
            create_all_working_datasets()
        else:
            print("Usage: python create_ui_visible_datasets.py [individual|services|all]")
            print()
            print("Options:")
            print("  individual - Create 4 datasets using individual features")
            print("               (zipcode, credit history, demographics, comprehensive)")
            print()
            print("  services   - Create 5 datasets using feature services")
            print("               (credit_history_v1, demographics_v1, location_intelligence_v1,")
            print("                customer_profile_v1, basic_underwriting_v1)")
            print()
            print("  all        - Create both individual and feature service datasets (9 total)")
            print()
            print("Feature Service Examples:")
            print("  • credit_history_v1: Simple credit history analysis")
            print("  • demographics_v1: Demographic profiling and segmentation")
            print("  • location_intelligence_v1: Geographic risk assessment")
            print("  • customer_profile_v1: Combined demographics + geography")
            print("  • basic_underwriting_v1: Credit history + demographics")
            print()
            print("All feature services use batch features only (no on-demand) for reliability.")
    else:
        # Default behavior - create all working datasets
        create_all_working_datasets()