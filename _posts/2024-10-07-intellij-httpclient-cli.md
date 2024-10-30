---
title: "How I used Intellij HttpClient CLI in Jenkins"
last_modified_at: 2024-10-07
categories:
  - IntelliJ
tags:
  - IntelliJ
  - Rest Client
  - Jenkins
---

Like many organizations we are into building scalable microservices in cloud, and we have variety of protocols like REST, Graphql etc using both server and serverless platforms, but one thing that is common is API’s everywhere and calling these API’s in a controlled manner in environments whether it is for a datafix or onboarding isn’t a unique challenge here is one of the way we were addressing it.

Intellij IDEA

Traditionally I was using Postman while testing apis locally, postman came long way to support features like pre-request, post-request scripts and way to parameterize variables through environments was very useful, however initially it lacked the ability to run it as a CLI ( over the years, they were added) and when we were doing any support related things like data fixing or onboarding via an API call through pipelines were done as cURL command, and it worked generally but when there are variables involved and need flexibility to run for different environments through a controlled manner means more bash script.

We use IntelliJ IDEA as a IDE for our development work and with its rich feature set of multi language support helped us to switch languages, frameworks build systems seamlessly and started using their built in [HttpClient](https://www.jetbrains.com/help/idea/http-client-in-product-code-editor.html) that replaced postman for me long time ago, I didn’t have to leave the IDE to go to Postman or any other tool for invoking the API’s.

We wanted to take that one step further by using their HttpClient CLI in jenkins and using that to run scripts or one-of api invocations. We used their download to create an docker build image and using that we were able to do repeatable script executions and variable replacements real-time per environment made it so easy.

1.  [https://www.jetbrains.com/ijhttp/download/#section=zip-archive](https://www.jetbrains.com/ijhttp/download/#section=zip-archive) download and unzip it in your Docker
2.  Update path variable to point to <path>ijhttp/ijhttp
3.  execute your script as

```bash
ijhttp \\  
\--log-level $logLevel \\  
\--env-file http-client.env.json \\  
\--private-env-file http-client.private.env.json \\  
\--env ${TARGET\_ENV}  script.http
```

with this we check-in script and parameterize for environment and run it where ever we want with tests to ensure script ran as expected.

There are some known issues and hopefully coming years they will be addressed and this could be a powerful tool in our DevOps arsenal.

Hope this helps someone!!.
