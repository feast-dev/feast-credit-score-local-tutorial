# -*- coding: utf-8 -*-
from feast.feature_store import FeatureStore


def main():
    store = FeatureStore(repo_path="./feature_repo/")
    store.serve(
        host='localhost', 
        port=8888, 
        type_="http",
        no_access_log=False, 
        workers=2, 
        keep_alive_timeout=1,
        registry_ttl_sec=10,
    )    

if __name__ =="__main__":
    main()

