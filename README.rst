rds-log
=======

A small utility to download/stream logs from Amazon AWS RDS to a local
directory. When started, all log files will be downloaded, and the latest file
will be watched for changes.

Installation
------------

Make sure you already have installed

* `Amazon RDS Command Line Toolkit
  <http://docs.aws.amazon.com/AmazonRDS/latest/CommandLineReference/StartCLI.html>`_
* Python 3.4 (Python 2 is not supported)


Install from PyPI::

    pip install rds-log


Usage
-----

rds-log-stream will find AWS credentials in ~/.aws/credentials or environment
variables. rds-log-stream uses boto3 and finds credentials/config in the same
locations.

Set up ~/.aws/credentials with AWS authentication details::

    [default]
    aws_access_key_id = <your access key id>
    aws_secret_access_key = <your secret key>

Set up ~/.aws/config to point to your region::

    [default]
    region = eu-central-1

An alternative is to set up environment variables::

    export AWS_ACCESS_KEY_ID="<your access key id>"
    export AWS_SECRET_ACCESS_KEY="<your secret key>"
    export AWS_DEFAULT_REGION="<your aws region>"


Run rds-log-stream with your database identifier and directory to store logs::

    rds-log-stream yourdbinstance /your/log/destination

/your/log/destination will be populated with all current RDS logs and
continously updated with new messages as they arrive.


Development
-----------

Creating a new release::

    git tag x.x.x
    python setup.py sdist bdist_wheel
    twine upload dist/*x.x.x*
