
# AWS deployment framework for serverless applications

aws-syndicate is an Amazon Web Services deployment framework written in Python, which allows to easily deploy serverless applications using resource descriptions. The framework allows to work with applications that engage the following AWS services:

* API Gateway

* CloudWatch Events

* Cognito

* DynamoDB

* Elastic Beanstalk

* Elastic Compute Cloud

* Identity and Access Management

* Kinesis

* Lambda

* Simple Notification Service

* Simple Queue Service

* Simple Storage Service

* Step Functions

Quick Start
-----------
To successfully setup and use the Syndicate, you need the following software to be installed:

* Python 3.7+
* pip 9.0+
* Apache Maven 3.3.9+

First, install the framework:

    $ pip install .

Next, set up a Syndicate Java **[plugin](https://github.com/epam/aws-syndicate/tree/master/plugin)**:

    $ mvn install

Next, set up a configuration file **[sdct.conf](https://github.com/epam/aws-syndicate/blob/master/examples/demo-config/sdct.conf)**:

	# absolute path to the examples/demo-project folder
	project_path=FOLDER_PATH

	resources_suffix=
	resources_prefix=sdct-
	# region name, example - eu-central-1
	region=REGION_NAME
	# bucket name to upload deployment artifacts, must be unique across all AWS accounts
	deploy_target_bucket=BUCKET_NAME
	# your account id
	account_id=ACCOUNT_ID
	access_role=

	aws_access_key_id=ACCESS_KEY_ID
	aws_secret_access_key=SECRET_ACCESS_KEY

	# build configuration
	build_projects_mapping=mvn:/demo-java;python:/demo-python

FOLDER_PATH - replace with absolute path to the folder **examples/demo-project** <br/> ACCOUNT_ID - replace with your AWS account id <br/> REGION_NAME - replace with region name where infrastructure will be deployed <br/> BUCKET_NAME - replace with an S3 bucket name which will be used as a storage for framework artifacts (bucket name must be unique across all AWS accounts) <br/> ACCESS_KEY_ID and SECRET_ACCESS_KEY - replace with AWS credentials for user with admin permissions

Then, set up an aliases file **[sdct_aliases.conf](https://github.com/epam/aws-syndicate/blob/master/examples/demo-config/sdct_aliases.conf)**:

    region=REGION_NAME
	notification_bucket=BUCKET_NAME
	account_id=ACCOUNT_ID

ACCOUNT_ID - replace with your AWS account id <br/> BUCKET_NAME - replace with an S3 bucket name which will be used in demo application (bucket name must be unique across all AWS accounts) <br/> REGION_NAME - replace with region name where infrastructure will be deployed

Then, set up an environment variable **SDCT_CONF**:

    export SDCT_CONF=FOLDER_PATH

FOLDER_PATH - absolute path to the folder where are located files **sdct.conf** and **sdct_aliases.conf**

Deployment
------------
The demo application consists of the following infrastructure:
*  2 IAM roles
* 3 IAM policies
* 1 DynamoDB table
* 1 S3 bucket
* 2 lambdas
* 1 API Gateway

Create an S3 bucket for aws-syndicate artifacts:

    $ syndicate create_deploy_target_bucket

Next, build aws-syndicate bundle with artifacts to be deployed:

    $ syndicate build_bundle --bundle_name demo-deploy

Then, deploy AWS resources:

    $ syndicate deploy --bundle_name demo-deploy --deploy_name sdct-example

We have done it!

The demo serverless application is ready to be used.

If you need to clean AWS resources:

    $ syndicate clean --bundle_name demo-deploy --deploy_name sdct-example

Documentation
------------
You can find a detailed documentation [here](https://github.com/epam/aws-syndicate/blob/master/docs/01_sdct_quick_start.pdf)

Getting Help
------------

We use GitHub issues for tracking bugs and feature requests. If it turns out that you may have found a bug, please [open an issue](https://github.com/epam/aws-syndicate/issues/new)
