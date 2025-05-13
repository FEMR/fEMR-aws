import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as lambda from "aws-cdk-lib/aws-lambda";
import { FibulaApi } from "./public-api";
import { FibulaLambdas } from "../lambda/public-api/public-api-lambdas";
import { Topic } from "aws-cdk-lib/aws-sns";
import { EmailSubscription } from "aws-cdk-lib/aws-sns-subscriptions";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { FibulaReactApp } from "./frontend";

export class FemrAwsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // SNS Topic
    const sendEnrollmentRequestTopic = new Topic(
      this,
      "SendEnrollmentRequestTopic",
      {
        displayName: "Send enrollment request email",
      }
    );

    sendEnrollmentRequestTopic.addSubscription(
      new EmailSubscription("bklingen@calpoly.edu")
    );

    const sendEnrollmentResponseTopic = new Topic(
      this,
      "SendEnrollmentResponseTopic",
      {
        displayName: "Send enrollment response email",
      }
    );

    // React App
    const reactApp = new FibulaReactApp(this, "ReactApp");

    // S3 Bucket - update to avoid collision
    const installerBucket = new Bucket(this, "InstallerBucket", {
      bucketName: "femr-installer",
    });

    const dbDumpBucket = new Bucket(this, "DBDumpBucket", {
      bucketName: "femr-kit-db-dumps",
    });

    // Lambdas
    const fibulaLambdas = new FibulaLambdas(this, "Lambdas", {
      requestTopic: sendEnrollmentRequestTopic,
      responseTopic: sendEnrollmentResponseTopic,
      installerBucket: installerBucket,
      dbDumpBucket: dbDumpBucket,
      domainName: reactApp.distribution.distributionDomainName,
    });

    // API
    const api = new FibulaApi(this, "FibulaApi", {
      fibulaLambdas: fibulaLambdas,
    });
  }
}
