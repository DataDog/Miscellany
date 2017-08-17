# S3 Permissions
This script will check S3 bucket ACL permissions for read/write access for
`AllUser` and report a metric to Datadog that uses a custom value to alert on.
This script uses `0` when no read or write ACLs are in place, `1` when read or
write is given to all users, and `2` when read and write are given to all users.

This script is just for POC and demostration purposes and should not be used for
production. It may be the basis for production monitoring scripts of your own.


# Run Code
- Setup a python virtualenv: `virtualenv s3_permissions`
- Activate the virtualenv: `source s3_permissions/bin/activate`
- Run `pip install -r requirements.txt`
- Setup [AWS Credentials](http://boto3.readthedocs.io/en/latest/guide/configuration.html)
  in your environment
- Run `python s3_permissions.py -k <your-api-key> -a <your-app-key>`
  - Alternatively set `DATADOG_API_KEY` or `DD_API_KEY` and `DATADOG_APP_KEY` or
    `DD_APP_KEY` as environment variables
