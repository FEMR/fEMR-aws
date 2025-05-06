#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { FemrAwsStack } from "../lib/femr-aws-stack";

const app = new cdk.App();
new FemrAwsStack(app, "FemrAwsStack", {
  env: {
    account: "177099735333",
    region: "us-east-2",
  },
});
