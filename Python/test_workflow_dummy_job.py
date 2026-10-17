import sys
import datetime
import boto3

job_name = "test_workflow_dummy_job"

print("--------------------------------------------------")
print(f"Starting test dummy job: {job_name}")
print(f"Execution timestamp: {datetime.datetime.now(datetime.timezone.utc)}")
print("--------------------------------------------------")

# Simple logic test: Check AWS connection using boto3
try:
    sts_client = boto3.client('sts')
    identity = sts_client.get_caller_identity()
    print(f"AWS Connection Verified. Running under Account: {identity['Account']}")
except Exception as e:
    print(f"Warning: Could not fetch STS identity: {str(e)}")

print("Simulating step 1: Validating workflow signals...")
print("Simulating step 2: Performing dummy assertions...")

print("--------------------------------------------------")
print("SUCCESS: Test workflow dummy job completed successfully!")
print("--------------------------------------------------")