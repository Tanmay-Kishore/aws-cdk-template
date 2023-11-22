"""Script to run CFN Lint."""
import os
from pathlib import Path
import subprocess
ROOT_DIR = Path(__file__).parent.parent.parent.parent

def get_cfts(top_directory):
    for dirname, dirnames, filenames in os.walk(top_directory):
        for source_dir in dirnames:
            if source_dir == "cdk.out":
                return os.path.join(dirname, source_dir)


PATH_TO_CFT = get_cfts(ROOT_DIR)

subprocess.run(
    f"cfn-lint --verbose {PATH_TO_CFT}/*template.json -i W",
    shell=True,
    check=True,
    stderr=subprocess.STDOUT
)