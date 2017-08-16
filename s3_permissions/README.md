# S3 Permissions
TODO!

# Run Code
- Setup a python virtualenv: `virtualenv s3_permissions`
- Activate the virtualenv: `source s3_permissions/bin/activate`
- Run `pip install -r requirements.txt`
- Setup [AWS Credentials](http://boto3.readthedocs.io/en/latest/guide/configuration.html)
  in your environment
- Run `python s3_permissions.py -k <your-api-key> -a <your-app-key>`
  - Alternatively set `DATADOG_API_KEY` or `DD_API_KEY` and `DATADOG_APP_KEY` or
    `DD_APP_KEY` as environment variables
