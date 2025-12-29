"""
iam_audit.py
Audits all IAM users in your AWS account for MFA compliance.
Checks performed:
    1. Console Access - Does the user have a password to log into AWS Console?
    2. MFA Status - If they have console access, is MFA enabled?
Output:
    [PASS] - Console user with MFA enabled
    [FAIL] - Console user WITHOUT MFA (security risk!)
    [INFO] - No console access (programmatic only, MFA not required)
Usage:
    python iam_audit.py
Requirements:
    - boto3 installed (pip install boto3)
    - AWS credentials configured (aws configure)
"""

# Import associated AWS module for script.
import boto3

# Create IAM client to interact with AWS IAM service.
iam = boto3.client('iam')

# Get a list of all IAM users in the account.
iam_users = iam.list_users()  
users = iam_users['Users']

# Counters to track compliance stats.
total_users = len(users)
compliant_count = 0
no_console_count = 0

# Main loop to check each user for MFA compliance. 
for user in users:
    username = user['UserName']
    print(f"Checking: {username}")
    
    # Check returns a list of MFA devices. Empty list means no MFA.
    mfa_response = iam.list_mfa_devices(UserName=username)
    mfa_devices = mfa_response['MFADevices']

    # Check to see if user has console access. Throws except if no console access.
    try:
        iam.get_login_profile(UserName=username)
        has_console = True
    except:
        has_console = False

    # Evaluate compliance based on both checks.
    # Console user with MFA enabled.
    if has_console and mfa_devices:
        compliant_count += 1
        print("    [PASS] MFA enabled for console user.")

    # Console user without MFA enabled. 
    elif has_console and not mfa_devices:
        print("    [FAIL] Console access WITHOUT MFA!")

    # No console access does not require MFA> 
    else:
        no_console_count += 1
        print("    [INFO] No console access (MFA not required).")

# Compliance summary of results.
print("\n" + "=" * 40)
print(f"Total users: {total_users}")
print(f"Compliant (MFA enabled): {compliant_count}")
print(f"No console access: {no_console_count}")
print(f"Non-compliant: {total_users - compliant_count - no_console_count}")