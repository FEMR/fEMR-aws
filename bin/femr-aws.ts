#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { FemrAwsStack } from "../lib/femr-aws-stack";
import { PipelineStack } from "../lib/pipeline-stack";

const app = new cdk.App();
new PipelineStack(app, "FemrAwsStack", {
  env: {
    account: "177099735333",
    region: "us-east-2",
  },
});
