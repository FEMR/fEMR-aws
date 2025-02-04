#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { PipelineStack } from "../lib/pipeline-stack";

const app = new cdk.App();
new PipelineStack(app, "FibulaPipelineStack", {
  env: { account: "177099735333", region: "us-east-2" },
});

app.synth();
