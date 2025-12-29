# iam_audit.py

A Python tool that audits all IAM users in your AWS account for MFA compliance.

## Overview

This script checks each IAM user to determine:
1. **Console Access** — Does the user have a password to log into AWS Console?
2. **MFA Status** — If they have console access, is MFA enabled?

## Requirements

- Python 3.x
- `boto3` library
- AWS CLI configured with credentials (`aws configure`)

### Install dependencies
```bash
pip install boto3
```

## Usage

```bash
python iam_audit.py
```

**Sample output:**
```
Checking: admin-user
    [PASS] MFA enabled for console user.
Checking: developer
    [FAIL] Console access WITHOUT MFA!
Checking: lambda-role-user
    [INFO] No console access (MFA not required).

========================================
Total users: 3
Compliant (MFA enabled): 1
No console access: 1
Non-compliant: 1
```

## Output Legend

| Status | Meaning |
|--------|---------|
| `[PASS]` | Console user with MFA enabled |
| `[FAIL]` | Console user WITHOUT MFA |
| `[INFO]` | No console access (programmatic only) ℹ|

## Key Concepts Learned

| Concept | Description |
|---------|-------------|
| `iam.list_users()` | Get all IAM users |
| `iam.list_mfa_devices()` | Check MFA status |
| `iam.get_login_profile()` | Check console access |
| Exception handling | API throws error when config doesn't exist |

## GRC Application

This tool supports:
- **CIS AWS Benchmark** — 1.10 (MFA enabled for all IAM users with console password)
- **SOC 2** — CC6.1 (Logical Access Controls)
- **NIST 800-53** — IA-2 (Multi-Factor Authentication)

## Future Enhancements

- Check access key age
- Flag inactive users (90+ days)
- Export results to CSV/JSON
- Add timestamp to output
- Email alerts for non-compliant users
