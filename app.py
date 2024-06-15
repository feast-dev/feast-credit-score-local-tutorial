from feast.feature_server import start_server 
from feast.feature_store import FeatureStore


def main():
    store = FeatureStore(repo_path="./feature_repo/")
    start_server(
        store=store, 
        host='localhost', 
        port=8080, 
        no_access_log=False, 
        workers=2, 
        keep_alive_timeout=1, 
        registry_ttl_sec=10,
    )    

if __name__ =="__main__":
    main()

