---
title: "Java SSL within AWS Lambda"
last_modified_at: 2018-07-24
categories:
  - Blog
tags:
  - AWS
  - Lambda
  - Java
  - SSL
---
## Java SSL within AWS Lambda

Developing a java function with AWS lambda is fairly simple and straight forward, however if we choose to call another service as part of lambda is still easy but if that service is on “HTTPS” that’s where you will run into set of problems

Problem I am going to talk about here is Certificate issues, when we communicate to a secured end point through java or any other framework at the network level it consists of handshake and data transfer.

We were trying to call a service hosted in AWS in our VPC and we used Amazon self signed cert for our internal services, in this particular case, we have to find a way to trust the cert presented by the service.

Since we are using AWS self signed certs, which are created using Amazon’s own Certificate Authority (CA) and EC2, ELB’s dies very often they are not issued for the hostname, rather issued at the domain.

Using self signed certs for internal usage saves lots of money on getting trusted certs like verisign, that same simplicity causes issues within lambda.

First problem is we don’t have DNS setup in lambda which makes us to use IP address rather than a DNS.

Second one is we are running a lambda so adding the self signed cert to our trust store like adding to underlying java cacerts is out of the question.
#### Possible options were
- Create trust store programatically and use it in AWS Lambda infrastructure
- Trust self signed and remove host name verification, in other words ignore SSL validation errors.
  
We went with option#2 since our services are internal to our VPC and we know for sure they are self signed. Below is the piece of code using Apache HttpClient
``` java
// trust self signed
SSLContext sslcontext = SSLContexts.custom().loadTrustMaterial(null, new TrustSelfSignedStrategy()).build();

SSLConnectionSocketFactory sslsf = new SSLConnectionSocketFactory(
        sslcontext,
        null,
        null,
        new NoopHostnameVerifier()/*ignoring hostname verifier*/);

CloseableHttpClient httpclient = HttpClients.custom()
        .setSSLSocketFactory(sslsf)
        .build();
```        
Even though we solved it, I got curious and decided to solve the other option and here is how I was able to do it.
Created a truststore of my own with the required cert in it and stored in S3 some place where Lambda can access it.
Within lambda able to fetch above file from S3 and using java environment able to setup the trust store and use that for SSL connection.
#### Conclusion
May be AWS can let Lambda developers to choose cert from ACM when developing using Java to avoid this extra step when SSL communication is choosen.