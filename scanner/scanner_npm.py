import pandas as pd
import subprocess
import requests
import argparse
import logging
import os

from library.server import *


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--csv", type=str)
args = arg_parser.parse_args()


def get_npm_versions(alias: str):
    alias = alias.lower()
    NPM_BASE_URL = "https://registry.npmjs.org"
    res = requests.get(f"{NPM_BASE_URL}/{alias}")

    if res.status_code != 200:
        return []

    print("Status Code:", res.status_code)

    res_json = res.json()
    package_name = res_json["name"]
    package_versions = list(res_json["versions"].keys())
    package_ecosystem = "npm"

    for version in package_versions:
        print("In version:", version)

        package_version = version.lower()
        package_dist_shasum = res_json["versions"][version]["dist"]["shasum"]
        package_dist_artifact = res_json["versions"][version]["dist"]["tarball"]
        package_dist_artifact_name = package_dist_artifact.split("/")[-1]

        source_abs_path = os.path.join(os.getenv("DIR_SOURCE"), package_name, package_version)
        source_abs_path = os.path.abspath(source_abs_path)
        result_abs_path = os.path.join(os.getenv("DIR_RESULT"), package_name, package_version)
        result_abs_path = os.path.abspath(result_abs_path)

        subprocess.run(
            f"""
            mkdir -p {source_abs_path} &&\
            mkdir -p {result_abs_path} &&\
            cd {source_abs_path} &&\
            wget {package_dist_artifact} &&\
            tar -xvf {package_dist_artifact_name} &&\
            rm {package_dist_artifact_name}
            """,
            shell=True
        )

        docker_image = os.getenv("DOCKER_IMAGE")
        subprocess.run(
            f"""
            docker run --rm -v {source_abs_path}:/opt/source -v {result_abs_path}:/opt/result -t {docker_image} security-extended --language javascript-typescript
            """,
            shell=True
        )
        break


def main():
    csv_path = os.path.abspath(args.csv)
    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        alias = row["alias"]
        print("Using Alias:", alias)
        get_npm_versions(alias)


if __name__ == "__main__":

    from dotenv import load_dotenv
    load_dotenv()

    main()