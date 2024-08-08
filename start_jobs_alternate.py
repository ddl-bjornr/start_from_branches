import requests
import json
import os
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Start a Domino job.')
parser.add_argument('--project', default='quick-start', help='Domino project name (default: quick-start)')
args = parser.parse_args()

# Collect data
API_KEY = os.getenv("DOMINO_USER_API_KEY")

AUTH_HEADER = {"X-Domino-Api-Key": API_KEY, "accept": "application/json"}
domino_host = os.environ.get("DOMINO_API_HOST")

# Pull the userName from the self object
def get_user_name(BASE_API_URL, AUTH_HEADER):
    response = requests.get(f"{BASE_API_URL}/v4/users/self", headers=AUTH_HEADER).json()
    return response["userName"]

# Pull the userId from the self object
def get_user_id(BASE_API_URL, AUTH_HEADER):
    response = requests.get(f"{BASE_API_URL}/v4/users/self", headers=AUTH_HEADER).json()
    print(response)
    return response["id"]

# Use the project name provided as a command-line argument or default to 'quick-start'
DOMINO_PROJECT = args.project

project_id = os.environ["DOMINO_PROJECT_ID"]

# Map the userName your API KEY has listed into UID to use against the job_run / job/start API
DOMINO_USER_ID = get_user_id(BASE_API_URL=domino_host, AUTH_HEADER=AUTH_HEADER)
DOMINO_USER_NAME = get_user_name(BASE_API_URL=domino_host, AUTH_HEADER=AUTH_HEADER)

# Get the project details
project = requests.get(
    f"{domino_host}/v4/gateway/projects/findProjectByOwnerAndName?ownerName={DOMINO_USER_NAME}&projectName={DOMINO_PROJECT}",
    headers=AUTH_HEADER
)

DOMINO_PROJECT_ID = project.json()['id']

# To separate the function, Python 3.10 and later don't like from domino import job_start:
def job_start_overloaded(file_path_and_name, app_id=None, project_id=None, job_name=None, branch=None):
    api_key = os.environ.get("DOMINO_USER_API_KEY")
    domino_host = os.environ.get("DOMINO_API_HOST")
    
    if branch:
        url = f"{domino_host}/api/jobs/v1/jobs"
        headers = {
            "X-Domino-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        mainRepoGitRef = {
            "refType": "branches",
            "value": branch
        }
        data = {
            "projectId": project_id,
            "runCommand": file_path_and_name,
            "mainRepoGitRef": mainRepoGitRef
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(url, headers, json.dumps(data))    
        if response.status_code == 201:
            print("Job started successfully.")
        else:
            print(f"Failed to start job. Status code: {response.status_code}, Response: {response.text}")
        return response.status_code
    else:
        from domino import Domino
        domino = Domino(f"{DOMINO_USER_NAME}/{DOMINO_PROJECT}", api_key=api_key)
        domino.runs_start([file_path_and_name])
        return domino

# Example usage

# Runs against 'live' branch
job_start_overloaded(project_id=project_id, job_name="live", file_path_and_name="/mnt/code/job.sh", branch="live")

# Runs against the head/default/main branch:
job_start_overloaded(project_id=project_id, job_name="main", file_path_and_name="/mnt/code/job.sh")
