import os
import base64


def start_python_feature_transform_server(fs_file: str):
    os.environ["FEATURE_STORE_YAML_ENV_NAME"] = str(
        base64.b64encode(open(fs_file, "rb").read()), "utf-8"
    )
    
    


if __name__ == "__main__":
    fs_file = "./feature_repo/feature_store.yaml"
    start_python_feature_transform_server(fs_file=)