import * as cdk from "aws-cdk-lib";
import { PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Function } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import { Runtime, Code } from "aws-cdk-lib/aws-lambda";
import { Topic } from "aws-cdk-lib/aws-sns";
import { Bucket } from "aws-cdk-lib/aws-s3";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

interface FibulaLambdasProps {
  requestTopic: Topic;
  responseTopic: Topic;
  installerBucket: Bucket;
  domainName: string;
  dbDumpBucket: Bucket;
}

export class FibulaLambdas extends Construct {
  readonly defaultLambda: Function;
  readonly sendRequestLambda: Function;
  readonly sendResponseLambda: Function;
  readonly loginLambda: Function;
  readonly getEnrollmentRequestsLambdas: Function;
  readonly getInstallerLambda: Function;
  readonly uploadDump: Function;

  constructor(scope: Construct, id: string, props: FibulaLambdasProps) {
    super(scope, id);

    this.defaultLambda = new Function(scope, "DefaultLambda", {
      runtime: Runtime.PYTHON_3_13,
      code: Code.fromAsset("lambda/public-api"),
      handler: "default_handler.lambda_handler",
    });

    this.sendRequestLambda = new Function(
      scope,
      "SendEnrollmentRequestLambda",
      {
        runtime: Runtime.PYTHON_3_13,
        code: Code.fromAsset("lambda/public-api", {
          bundling: {
            image: Runtime.PYTHON_3_13.bundlingImage,
            command: [
              "bash",
              "-c",
              "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
            ],
          },
        }),
        handler: "send_request_handler.lambda_handler",
        environment: {
          REQUEST_TOPIC_ARN: props.requestTopic.topicArn,
          RESPONSE_TOPIC_ARN: props.responseTopic.topicArn,
          DOMAIN_NAME: props.domainName,
        },
      }
    );

    this.sendResponseLambda = new Function(
      scope,
      "SendEnrollmentResponseLambda",
      {
        runtime: Runtime.PYTHON_3_13,
        code: Code.fromAsset("lambda/public-api", {
          bundling: {
            image: Runtime.PYTHON_3_13.bundlingImage,
            command: [
              "bash",
              "-c",
              "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
            ],
          },
        }),
        handler: "send_response_handler.lambda_handler",
        environment: {
          RESPONSE_TOPIC_ARN: props.responseTopic.topicArn,
          DOMAIN_NAME: props.domainName,
        },
      }
    );

    this.loginLambda = new Function(scope, "loginLambda", {
      runtime: Runtime.PYTHON_3_13,
      code: Code.fromAsset("lambda/public-api", {
        bundling: {
          image: Runtime.PYTHON_3_13.bundlingImage,
          command: [
            "bash",
            "-c",
            "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
          ],
        },
      }),
      handler: "login_handler.lambda_handler",
    });

    this.getEnrollmentRequestsLambdas = new Function(this, "Function", {
      code: Code.fromAsset("lambda/public-api", {
        bundling: {
          image: Runtime.PYTHON_3_13.bundlingImage,
          command: [
            "bash",
            "-c",
            "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
          ],
        },
      }),
      runtime: Runtime.PYTHON_3_13,
      handler: "get_enrollment_requests.lambda_handler",
    });

    this.getInstallerLambda = new Function(scope, "GetInstallerLambda", {
      runtime: Runtime.PYTHON_3_13,
      code: Code.fromAsset("lambda/public-api"),
      handler: "get_installer_handler.lambda_handler",
      environment: {
        BUCKET_NAME: props.installerBucket.bucketName,
      },
    });

    props.requestTopic.grantPublish(this.sendRequestLambda);
    props.responseTopic.grantPublish(this.sendResponseLambda);
    this.sendRequestLambda.addToRolePolicy(
      new PolicyStatement({
        actions: ["sns:Subscribe"],
        resources: [props.responseTopic.topicArn],
      })
    );
    props.installerBucket.grantRead(this.getInstallerLambda);

    this.uploadDump = new Function(scope, "UploadDumpLambda", {
      runtime: Runtime.PYTHON_3_13,
      code: Code.fromAsset("lambda/public-api"),
      handler: "upload_dump.lambda_handler",
      environment: {
        BUCKET_NAME: props.dbDumpBucket.bucketName,
      },
    });

    props.dbDumpBucket.grantPut(this.uploadDump);
  }
}
