#!/usr/bin/env python3
"""Deploy Pingdizzle to the App Engine standard (Python 3) environment."""

import argparse
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ID = "pingmysites"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--promote",
    default=True,
    action="store_true",
    help="Set the newly deployed version to be the default version (serving traffic)",
)

PARSED_ARGS = parser.parse_args()
PROMOTE = PARSED_ARGS.promote


def deploy():
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
        ("--promote" if PROMOTE else "--no-promote"),
        "--quiet",
        "app.yaml",
    ]
    subprocess.check_call(command)
    print("Done")


def deploy_cron_yaml():
    print("Deploying cron jobs configuration (cron.yaml)...")
    subprocess.check_call(["gcloud", "app", "deploy", "--project", PROJECT_ID, "--quiet", "cron.yaml"])
    print("Done")


deploy()
deploy_cron_yaml()
