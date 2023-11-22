"""Script to run CFN Nag scan."""
import os
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent

def get_cfts(top_directory):
    for _dirname, _dirnames, _filenames in os.walk(top_directory):
        for source_dir in _dirnames:
            if source_dir == "cdk.out":
                return os.path.join(_dirname, source_dir)


PATH_TO_STACKS = get_cfts(ROOT_DIR)

os.system(f"cfn_nag_scan --input-path {PATH_TO_STACKS}/*template.json")
subprocess.check_output(
    f"cfn_nag_scan --input-path {PATH_TO_STACKS}/*template.json",
    shell=True,
    stderr=subprocess.STDOUT
)