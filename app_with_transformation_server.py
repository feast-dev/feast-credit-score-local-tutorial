# -*- coding: utf-8 -*-
from feast.feature_store import FeatureStore


def main():
    # Init the Feature Store
    store = FeatureStore(repo_path="./feature_repo/")

    # Start the feature transformation server
    # default port is 6569
    store.serve_transformations(6569)

if __name__ == "__main__":
    main()

