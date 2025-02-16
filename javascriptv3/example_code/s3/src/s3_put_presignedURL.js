/* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
ABOUT THIS NODE.JS EXAMPLE: This example works with AWS SDK for JavaScript version 3 (v3),
which is available at https://github.com/aws/aws-sdk-js-v3. This example is in the 'AWS SDK for JavaScript v3 Developer Guide' at
https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/s3-example-creating-buckets.html.

Purpose:
s3_put_presignedURL.js creates a presigned URL to upload a file to an Amazon Simple Storage Service (Amazon S3) bucket.

Note: This example immediately deletes the object and bucket.

Inputs (replace in code):
- REGION


Running the code:
nodes3_put_presignedURL.js
[Outputs | Returns]:
Uploads the specified file to the specified bucket.
*/

// snippet-start:[s3.JavaScript.buckets.presignedurlv3]
// Import the required AWS SDK clients and commands for Node.js
import {
  CreateBucketCommand,
  DeleteObjectCommand,
  PutObjectCommand,
  DeleteBucketCommand }
from "@aws-sdk/client-s3";
 import { s3 } from "./libs/s3Client.js"; // Helper function that creates Amazon S3 service client module.
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import fetch from "node-fetch";

// Set parameters
// Create a random names for the Amazon Simple Storage Service (Amazon S3) bucket and key
const bucketParams = {
  Bucket: `test-bucket-${Math.ceil(Math.random() * 10 ** 10)}`,
  Key: `test-object-${Math.ceil(Math.random() * 10 ** 10)}`,
  Body: "BODY"
};
const run = async () => {
  try {
    // Create an Amazon S3 bucket.
    console.log(`Creating bucket ${bucketParams.Bucket}`);
    await s3.send(new CreateBucketCommand({ Bucket: bucketParams.Bucket }));
    console.log(`Waiting for "${bucketParams.Bucket}" bucket creation...`);
  } catch (err) {
    console.log("Error creating bucket", err);
  }
  try {
    // Create the command.
    const command = new PutObjectCommand(bucketParams);

    // Create the presigned URL.
    const signedUrl = await getSignedUrl(s3, command, {
      expiresIn: 3600,
    });
    console.log(
      `\nPutting "${params.Key}" using signedUrl with body "${bucketParams.Body}" in v3`
    );
    console.log(signedUrl);
    const response = await fetch(signedUrl);
    console.log(
      `\nResponse returned by signed URL: ${await response.text()}\n`
    );
    return response;
  } catch (err) {
    console.log("Error creating presigned URL", err);
  }
  try {
    // Delete the object.
    console.log(`\nDeleting object "${bucketParams.Key}"} from bucket`);
    await s3.send(
      new DeleteObjectCommand({ Bucket: bucketParams.Bucket, Key: params.Key })
    );
  } catch (err) {
    console.log("Error deleting object", err);
  }
  try {
    // Delete the Amazon S3 bucket.
    console.log(`\nDeleting bucket ${bucketParams.Bucket}`);
    await s3.send(new DeleteBucketCommand({ Bucket: bucketParams.Bucket }));
  } catch (err) {
    console.log("Error deleting bucket", err);
  }
};
run();
// snippet-end:[s3.JavaScript.buckets.presignedurlv3]
// For unit testing only.
// module.exports ={run, bucketParams};
