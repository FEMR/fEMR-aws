import { Construct } from "constructs";
import {
  Cors,
  LambdaIntegration,
  LambdaRestApi,
} from "aws-cdk-lib/aws-apigateway";
import { FibulaLambdas } from "../lambda/public-api/public-api-lambdas";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

interface FibulaApiProps {
  fibulaLambdas: FibulaLambdas;
}

export class FibulaApi extends Construct {
  readonly api: LambdaRestApi;

  constructor(scope: Construct, id: string, props: FibulaApiProps) {
    super(scope, id);

    this.api = new LambdaRestApi(this, "FibulaApi", {
      handler: props.fibulaLambdas.defaultLambda,
      proxy: false,
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["GET", "PUT"],
        allowHeaders: Cors.DEFAULT_HEADERS,
      },
    });

    const login = this.api.root.addResource("login", {
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["PUT"],
        allowHeaders: Cors.DEFAULT_HEADERS,
      },
    });
    login.addMethod(
      "PUT",
      new LambdaIntegration(props.fibulaLambdas.loginLambda)
    );

    const enroll = this.api.root.addResource("enroll", {
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["GET", "PUT"],
        allowHeaders: Cors.DEFAULT_HEADERS,
      },
    });
    enroll.addMethod(
      "PUT",
      new LambdaIntegration(props.fibulaLambdas.sendRequestLambda)
    );
    enroll.addMethod(
      "GET",
      new LambdaIntegration(props.fibulaLambdas.getEnrollmentRequestsLambdas)
    );

    const requestId = enroll.addResource("{requestId}", {
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["GET", "PUT"],
        allowHeaders: Cors.DEFAULT_HEADERS,
      },
    });
    requestId.addMethod(
      "PUT",
      new LambdaIntegration(props.fibulaLambdas.sendResponseLambda)
    );

    const installer = this.api.root.addResource("installer", {
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["GET"],
        allowHeaders: Cors.DEFAULT_HEADERS,
      },
    });
    const platform = installer.addResource("{platform}", {
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["GET"],
        allowHeaders: Cors.DEFAULT_HEADERS,
      },
    });
    platform.addMethod(
      "GET",
      new LambdaIntegration(props.fibulaLambdas.getInstallerLambda)
    );

    const uploadDumpApi = this.api.root.addResource("upload_dump");

    const idResource = uploadDumpApi.addResource("{id}");
    idResource.addMethod(
      "POST",
      new LambdaIntegration(props.fibulaLambdas.uploadDump)
    );
  }
}
