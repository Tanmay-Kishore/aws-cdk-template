#! /bin/sh python
"""Script for installing the packages for lambda layers."""
import os
import shutil
from typing import AnyStr, List
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
print(ROOT_DIR)

def get_path_for_src(top_directory):
    for dirname, dirnames, filenames in os.walk(top_directory):
        for source_dir in dirnames:
            if source_dir == "src":
                return os.path.join(dirname, source_dir)

def get_layer_directories(top_level_dir: bytes) -> List[AnyStr]:
    """Get a list of all layers in layer folder."""
    dir_paths = []
    for subdir in os.scandir(top_level_dir):
        dir_paths.append(os.path.abspath(subdir))
    return dir_paths

def create_zip_for_layers(layer_dir: bytes) -> None:
    """Creates zip for layers."""
    filename = str(layer_dir)
    filename.rsplit("/", 1)[-1]
    install_requirements(layer_dir)
    # subprocess.run(f"zip --quiet -r9 ../{filename}.zip ./*", shell=True, check=True)
    shutil.make_archive(filename, 'zip')
    shutil.rmtree(layer_dir)


def install_requirements(path: bytes) -> None:
    """Install requirements for layers."""
    os.chdir(path + '/python')
    os.system('pip3 install -r requirements.txt -t .')
    os.remove("requirements.txt")
    remove_unnecessary_folders(path + '/python')
    os.chdir(path)


def remove_unnecessary_folders(path: bytes) -> None:
    """Removes unnecessary folders with extension .dist-info."""
    folders = os.listdir(path)
    for folder in folders:
        if folder.endswith(".dist-info"):
            shutil.rmtree(folder)

src_directory = get_path_for_src(ROOT_DIR)
layer_directories = get_layer_directories(src_directory + '/layer')
for layer in layer_directories:
    print("creating zip for:", layer)
    create_zip_for_layers(layer)
