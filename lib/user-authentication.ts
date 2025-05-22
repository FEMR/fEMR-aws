import { Construct } from "constructs";
import { Duration, RemovalPolicy } from "aws-cdk-lib";
import {
  UserPool,
  UserPoolClient,
  AccountRecovery,
  VerificationEmailStyle,
  UserPoolDomain,
  OAuthScope,
  UserPoolOperation,
  StringAttribute,
  UserPoolClientIdentityProvider,
} from "aws-cdk-lib/aws-cognito";

export interface UserAuthenticationProps {
  domainPrefix: string;
  callbackUrls?: string[];
  logoutUrls?: string[];
  emailSendingAccount?: string;
  production?: boolean;
}

export class UserAuthentication extends Construct {
  public readonly userPool: UserPool;
  public readonly userPoolClient: UserPoolClient;
  public readonly userPoolDomain: UserPoolDomain;

  constructor(scope: Construct, id: string, props: UserAuthenticationProps) {
    super(scope, id);

    // Create the Cognito User Pool
    this.userPool = new UserPool(this, "UserPool", {
      userPoolName: `femr-user-pool`,
      selfSignUpEnabled: true,
      autoVerify: {
        email: true,
      },
      standardAttributes: {
        email: {
          required: true,
          mutable: true,
        },
        givenName: {
          required: true,
          mutable: true,
        },
        familyName: {
          required: true,
          mutable: true,
        },
      },
      customAttributes: {
        organization: new StringAttribute({ maxLen: 100, mutable: true }),
      },
      passwordPolicy: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
        tempPasswordValidity: Duration.days(7),
      },
      accountRecovery: AccountRecovery.EMAIL_ONLY,
      removalPolicy: props.production
        ? RemovalPolicy.RETAIN
        : RemovalPolicy.DESTROY,
      userVerification: {
        emailStyle: VerificationEmailStyle.LINK,
        emailSubject: `Verify your email for fEMR`,
        emailBody: `Thank you for signing up to fEMR! Please verify your email address by visiting {##this link##}.`,
      },
    });

    // Create the User Pool Client
    // TODO: Update this to actually support the installer + webapp
    this.userPoolClient = new UserPoolClient(this, "UserPoolClient", {
      userPool: this.userPool,
      authFlows: {
        userPassword: true,
        userSrp: true,
        adminUserPassword: true,
      },
      supportedIdentityProviders: [UserPoolClientIdentityProvider.COGNITO],
      preventUserExistenceErrors: true,
      generateSecret: false,
      oAuth: {
        callbackUrls: props.callbackUrls || ["http://localhost:3000/callback"],
        logoutUrls: props.logoutUrls || ["http://localhost:3000/logout"],
        flows: {
          authorizationCodeGrant: true,
        },
        scopes: [
          OAuthScope.EMAIL,
          OAuthScope.OPENID,
          OAuthScope.PROFILE,
          OAuthScope.COGNITO_ADMIN,
        ],
      },
    });

    // Create a domain for the User Pool
    this.userPoolDomain = new UserPoolDomain(this, "UserPoolDomain", {
      userPool: this.userPool,
      cognitoDomain: {
        domainPrefix: props.domainPrefix,
      },
    });
  }
}
