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

rds-log-stream will find AWS credentials in ~/.aws/credentials (just like
boto).

Set up ~/.aws/credentials with AWS authentication details::

    [default]
    aws_access_key_id = <your access key id>
    aws_secret_access_key = <your secret key>

Set up ~/.aws/config to point to your region::

    [default]
    region = eu-central-1

Run rds-log-stream with your database identifier and directory to store logs::

    rds-log-stream yourdbinstance /your/log/destination

/your/log/destination will be populated with all current RDS logs and
continously updated with new messages as they arrive.


Development
-----------

Creating a new release::

    # Modify setup.py with version
    git commit -am 'Version x.x.x'
    git tag x.x.x
    python setup.py sdist bdist_wheel
    twine upload dist/*
