"""Script to deploy CDK."""
import argparse
import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
import subprocess

def get_config(top_directory):
    for path, dirs, files in os.walk(top_directory):
        for name in files:
            if name == "config.ini":
                return os.path.join(path, name)


def get_cdk_path(top_directory):
    for dirname, dirnames, filenames in os.walk(top_directory):
        for source_dir in dirnames:
            if source_dir == "cdk":
                return os.path.join(dirname, source_dir)


ROOT_DIR = Path(__file__).parent.parent.parent.parent


CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.read(f"{get_config(ROOT_DIR)}")

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    '--env', type=str, default='stag'
)

ARGS = PARSER.parse_args()
ENV = ARGS.env

os.chdir(get_cdk_path(ROOT_DIR))
os.system(f"npx cdk bootstrap --context env={ENV}")
subprocess.run(f"npx cdk deploy '*' --context env={ENV} -v --require-approval never", check=True, shell=True, stderr=subprocess.STDOUT)