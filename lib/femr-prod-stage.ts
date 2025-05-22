import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { FemrAwsStack } from "./femr-aws-stack";

export enum LogicalStage {
  DEV = "dev",
  PROD = "prod",
}

export interface FemrStageProps extends cdk.StageProps {
  logicalStage: LogicalStage;
}

export class FemrStage extends cdk.Stage {
  readonly fibulaStack: FemrAwsStack;

  constructor(scope: Construct, id: string, props: FemrStageProps) {
    super(scope, id, props);

    this.fibulaStack = new FemrAwsStack(this, "FemrStack", {
      env: props.env,
      logicalStage: props.logicalStage,
    });
  }
}
