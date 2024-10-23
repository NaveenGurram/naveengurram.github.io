---
title: "AWS Sdk logging error"
last_modified_at: 2024-01-25
classes: wide
categories:
  - AWS
tags:
  - AWS
  - Typescript
  - SDK
  - Logging
---
# AWS SDK error logging in typescript

Sometimes small things which you overlook cause most headache and one such error is logging and error in a AWS lambda with NodeJs.

I was recently authoring a lambda and using KMS api to encrypt/decrypt some content, and in local development it worked just fine, so moved ahead with actual AWS environment and it failed with an error

```typescript

{
  "level": "error",
  "message": "Error signing payload with kms  Encountered Error: {\"stack\":\"TypeError: Converting circular structure to JSON\\n    --> starting at object with constructor 'IncomingMessage'\\n    |     property 'req' -> object with constructor 'ClientRequest'\\n    --- property 'res' closes the circle\\n    at JSON.stringify (<anonymous>)\\n    at Logging.error (/var/task/node_modules/@abc/abc-utils/lib/src/logging/logging.js:108:115)\\n    at Service.<anonymous> (/var/task/src/common/service/service.js:48:42)\\n    at Generator.throw (<anonymous>)\\n    at rejected (/var/task/src/common/service/service.js:6:65)\\n    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\",\"message\":\"Converting circular structure to JSON\\n    --> starting at object with constructor 'IncomingMessage'\\n    |     property 'req' -> object with constructor 'ClientRequest'\\n    --- property 'res' closes the circle\"}"
}

```
seeing it first time, and understanding that this error happens when you are try to do convert a json to string that has a circular reference

```javascript 
let obj = {a:b};
obj.a = obj;
JSON.stringify(obj);
```
then I started looking at the code to figure out where I was converting a JSON to string and after spending countless hours and remember it didn't fail for me locally, so a working copy just freaking out in actual AWS environment caused some much angst.

After spending considerable amount of time, finally removed my logger statement to use console.log and then realized my error.

```javascript
        try {
            const response = await this.kmsClient.send(new EncryptCommand({
                KeyId: config.KMS_ID,
                Plaintext: Buffer.from(JSON.stringify(someContent, null))
            }));
            const buff = Buffer.from(response.CiphertextBlob);
            return buff.toString('base64');
        } catch (e) {
            // printing e as any in logger causing circular json stringify error.
            logger.error('Error signing payload with KMS key', e as any);
        }
```
when I pass the error object to my logger to print the stack trace, that object itself has circular references and causing the problem.

It was a access denied exception from KMS for my role, ( in my local and AWS environment, roles are different, so it worked in my local but freaked out in AWS) but the point is AWS error object has circular reference in it causing logger to fail. 

I had to do a console.log just to print the error to see what it was

```JSON
2024-01-25T19:52:18.654Z	bd0504a5-0ea4-46ca-b4f1-553ac51065db	INFO	Error signing payload with KMS key AccessDeniedException: User: arn:aws:sts::xxxx:assumed-role/xxxx/xxx is not authorized to perform: kms:Encrypt on resource: arn:aws:kms:us-east-1:xxx:key/dddd because no identity-based policy allows the kms:Encrypt action
    at throwDefaultError (/var/task/node_modules/@smithy/smithy-client/dist-cjs/index.js:838:20)
    at /var/task/node_modules/@smithy/smithy-client/dist-cjs/index.js:847:5
    at de_EncryptCommandError (/var/task/node_modules/@aws-sdk/client-kms/dist-cjs/index.js:2509:14)
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async /var/task/node_modules/@smithy/middleware-serde/dist-cjs/index.js:35:20
    at async /var/task/node_modules/@aws-sdk/client-kms/node_modules/@aws-sdk/middleware-signing/dist-cjs/index.js:184:18
    at async /var/task/node_modules/@smithy/middleware-retry/dist-cjs/index.js:320:38
    at async /var/task/node_modules/@aws-sdk/client-kms/node_modules/@aws-sdk/middleware-logger/dist-cjs/index.js:33:22 {
  '$fault': 'client',
  '$metadata': {
    httpStatusCode: 400,
    requestId: 'dsfsdf',
    extendedRequestId: undefined,
    cfId: undefined,
    attempts: 1,
    totalRetryDelay: 0
  },
  __type: 'AccessDeniedException'
}

```

Even though error was screaming at my face about the logger, I didn't realize how such inconspicuous thing will cause an error, anyway my assumption caused a big headache for couple of hours. 