import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import {
  CodePipeline,
  CodePipelineSource,
  ShellStep,
} from "aws-cdk-lib/pipelines";
import { FemrStage, LogicalStage } from "./femr-prod-stage";

interface FibulaStackProps extends cdk.StackProps {
  logicalStage: LogicalStage;
}

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: FibulaStackProps) {
    super(scope, id, props);

    const pipeline = new CodePipeline(this, "FemrPipeline", {
      pipelineName: "FemrPipeline",
      synth: new ShellStep("Synth", {
        input: CodePipelineSource.connection("FEMR/fEMR-aws", "main", {
          connectionArn:
            "arn:aws:codeconnections:us-east-2:177099735333:connection/441b3a6c-57c1-48cd-ab0c-014953ce5618", // Created using the AWS console
        }),
        commands: [
          "cd resources/fibula-react-app",
          "npm install",
          "npm ci",
          "npm run build",
          "cd ../..",
          "npm install",
          "npm ci",
          "npm run build",
          "npx cdk synth",
        ],
      }),
      dockerEnabledForSynth: true,
    });

    /*
        pipeline.addStage(new FemrStage(this, "Dev", {
            env: { account: {DEV_ACCOUNT}, region: {DEV_REGION}},
            logicalStage: LogicalStage.DEV
        }))
        */

    pipeline.addStage(
      new FemrStage(this, "Prod", {
        env: { account: "177099735333", region: "us-east-2" },
        logicalStage: LogicalStage.PROD,
      })
    );
  }
}
