# Domino Job Starter

This Python script allows you to start a job in a Domino project. It can be configured to run against a specific branch and execute a specified command. The script takes the project name as a parameter, defaulting to `'quick-start'` if not provided.

## Requirements

- Python 3.6 or later
- The `requests` library: Install via pip with `pip install requests`
- Domino API Key: Set as an environment variable `DOMINO_USER_API_KEY`
- Domino API Host: Set as an environment variable `DOMINO_API_HOST`
- Domino Project ID: Set as an environment variable `DOMINO_PROJECT_ID`

## Usage

### Command-line Arguments

The script accepts the following command-line arguments:

- `--project`: The name of the Domino project. Defaults to `'quick-start'`.

### Example Usage

1. **Running the Script with the Default Project:**

    ```bash
    python domino_job_starter.py
    ```

    This will use `'quick-start'` as the project name.

2. **Running the Script with a Specific Project:**

    ```bash
    python domino_job_starter.py --project my-custom-project
    ```

    This will use `my-custom-project` as the project name.

### Environment Variables

Ensure the following environment variables are set before running the script:

- `DOMINO_USER_API_KEY`: Your Domino API key.
- `DOMINO_API_HOST`: The base URL of your Domino API host (e.g., `https://domino.example.com`).
- `DOMINO_PROJECT_ID`: The ID of the project in Domino.

### Example Workflow

1. **Runs against the `live` branch:**

    ```python
    job_start_overloaded(project_id=project_id, job_name="live", file_path_and_name="/mnt/code/job.sh", branch="live")
    ```

2. **Runs against the head/default/main branch:**

    ```python
    job_start_overloaded(project_id=project_id, job_name="main", file_path_and_name="/mnt/code/job.sh")
    ```

## Functions

### `get_user_name(BASE_API_URL, AUTH_HEADER)`

Fetches the `userName` from the Domino API.

### `get_user_id(BASE_API_URL, AUTH_HEADER)`

Fetches the `userId` from the Domino API.

### `job_start_overloaded(file_path_and_name, app_id=None, project_id=None, job_name=None, branch=None)`

Starts a job in the specified Domino project. The function can target a specific branch or the default branch if no branch is specified.

## Notes

- Ensure that your environment variables are set correctly for the script to interact with the Domino API.
- Modify the `file_path_and_name` and other parameters as needed for your specific use case.
- Use at your own risk - this does start jobs or runs in Domino which can incur fees.
- No guarantees, this is a combination of solutions provided to run from a branch, using the REST API

## License

This project is licensed under the MIT License. It is provided as an example only, please use at your own risk.
