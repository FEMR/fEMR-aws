import { CfnOutput, Duration } from "aws-cdk-lib";
import {
  AccessLevel,
  AllowedMethods,
  CachedMethods,
  CachePolicy,
  Distribution,
  OriginRequestPolicy,
  ViewerProtocolPolicy,
} from "aws-cdk-lib/aws-cloudfront";
import { S3BucketOrigin } from "aws-cdk-lib/aws-cloudfront-origins";
import { Bucket, CfnBucket, IBucket } from "aws-cdk-lib/aws-s3";
import { BucketDeployment, Source } from "aws-cdk-lib/aws-s3-deployment";
import { Construct } from "constructs";

export class FibulaReactApp extends Construct {
  readonly s3Site: Bucket;
  readonly distribution: Distribution;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Add S3 Bucket
    const s3Site = new Bucket(scope, "FibulaReactApp", {
      publicReadAccess: true,
      blockPublicAccess: {
        blockPublicAcls: false,
        ignorePublicAcls: false,
        restrictPublicBuckets: false,
        blockPublicPolicy: false,
      },
      websiteIndexDocument: "index.html",
      websiteErrorDocument: "index.html",
    });

    this.enableCorsOnBucket(s3Site);

    const s3Origin = S3BucketOrigin.withOriginAccessControl(s3Site, {
      originAccessLevels: [AccessLevel.READ, AccessLevel.LIST],
    });

    // Create a new CloudFront Distribution
    const distribution = new Distribution(
      scope,
      `femr-central-frontend-distribution`,
      {
        defaultRootObject: "index.html",
        defaultBehavior: {
          origin: s3Origin,
          compress: true,
          allowedMethods: AllowedMethods.ALLOW_ALL,
          cachedMethods: CachedMethods.CACHE_GET_HEAD_OPTIONS,
          cachePolicy: CachePolicy.CACHING_OPTIMIZED,
          originRequestPolicy: OriginRequestPolicy.CORS_S3_ORIGIN,
          viewerProtocolPolicy: ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        },
        errorResponses: [
          {
            httpStatus: 403,
            responseHttpStatus: 200,
            responsePagePath: "/index.html",
            ttl: Duration.seconds(60),
          },
        ],
        comment: "femr-central-frontend - CloudFront Distribution",
      }
    );

    // Setup Bucket Deployment to automatically deploy new assets and invalidate cache
    new BucketDeployment(scope, `fibulareactapp-s3bucketdeployment`, {
      sources: [Source.asset("central-frontend/build")],
      destinationBucket: s3Site,
      distribution: distribution,
      distributionPaths: ["/*"],
      memoryLimit: 4096,
    });

    // Final CloudFront URL
    new CfnOutput(scope, "CloudFront URL", {
      value: distribution.distributionDomainName,
    });

    this.s3Site = s3Site;
    this.distribution = distribution;
  }

  private enableCorsOnBucket(bucket: IBucket) {
    const cfnBucket = bucket.node.findChild("Resource") as CfnBucket;
    cfnBucket.addPropertyOverride("CorsConfiguration", {
      CorsRules: [
        {
          AllowedOrigins: ["*"],
          AllowedMethods: ["HEAD", "GET", "PUT", "POST", "DELETE"],
          ExposedHeaders: [
            "x-amz-server-side-encryption",
            "x-amz-request-id",
            "x-amz-id-2",
          ],
          AllowedHeaders: ["*"],
        },
      ],
    });
  }
}
