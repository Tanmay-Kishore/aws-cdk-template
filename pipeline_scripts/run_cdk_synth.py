"""Script to run cdk synth ."""
import argparse
import os
import subprocess
from pathlib import PurePath


def get_cdk_dir(top_dir):
    for _dir, _dirnames, _file in os.walk(top_dir):
        for _dirname in _dirnames:
            if _dirname == "cdk":
                return os.path.join(_dir, _dirname)


def run_synth(env):
    cdk_dir_path = get_cdk_dir(PurePath("../../.."))
    os.chdir(cdk_dir_path)
    subprocess.run(f"npx cdk synth --context env={env}", check=True, shell=True, stderr=subprocess.STDOUT)


PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    '--env', type=str, default='stag'
)
ARGS = PARSER.parse_args()
ENV = ARGS.env

run_synth(ENV)
