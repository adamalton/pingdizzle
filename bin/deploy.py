#!/usr/bin/env python
import argparse
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE_PATH = os.path.join(BASE_DIR, ".appengine-version")
PROJECT_ID = "pingmysites"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--promote",
    default=True,
    action="store_true",
    help="Set the newly deployed version to be the default version (serving traffic)",
)
parser.add_argument("--no-bump", default=False, action="store_true", help="Don't bump the App Engine version number")

PARSED_ARGS = parser.parse_args()
PROMOTE = PARSED_ARGS.promote
BUMP = not PARSED_ARGS.no_bump


def get_current_version_from_file():
    with open(VERSION_FILE_PATH) as f:
        return int(f.read().strip())


def write_new_version_to_file(version):
    print(f"Writing new version number ({version}) to file...")
    version = str(version)
    with open(VERSION_FILE_PATH, "w") as f:
        f.write(version)


def deploy():
    current_version = get_current_version_from_file()
    new_version = current_version
    if BUMP:
        new_version += 1
        print(f"Incrementing version number from {current_version} to {new_version}. (Pass --no-bump to prevent this.)")
    if not PROMOTE:
        print("Deploying new version as non-default... (Pass --promote to set it as default.)")
    else:
        print("Deploying new version which will be set to default...")

    command = [
        "gcloud",
        "app",
        "deploy",
        "--project",
        PROJECT_ID,
        "--version",
        str(new_version),
        ("--promote" if PROMOTE else "--no-promote"),
        "app.yaml",
    ]
    subprocess.check_call(command)
    if new_version != current_version:
        write_new_version_to_file(new_version)
    print("Done")


deploy()
