---
title: "Serverless mimicking AWS Api Gateway"
last_modified_at: 2024-01-17
categories:
  - Serverless
tags:
  - Serverless
  - AWS
  - ApiGateway
  - Swagger
---
# Serverless mimicking AWS Api Gateway for multi query param strings

![](/assets/images/serverless.png)

We use [serverless](https://www.serverless.com/) to package our node.js app written in typescript and even though their documentation is extensive, some areas they could have done better.

While serverless is a great convenience, getting it closer to what [AWS api gateway](https://aws.amazon.com/api-gateway/) offers in terms of functionality or syntax is hard to match, especially when we use **offline** to mimic api gateway while developing local.

we are developing something and utilized serverless offline feature to test it out locally before pushing it out.

Here is my swagger for AWS api gateway for an GET end point which has path params and multi query params.

endpoint looks like /some-endpoint/abc/def/ghu?flag=abc&flag=def

```yml
  /some-endpoint/{pathParam1}/{pathParam2}/{pathParam3}:
    get:
      produces:
        - application/json
      parameters:
        - name: pathParam1
          in: path
          type: string
          required: true
        - name: pathParam2
          in: path
          type: string
          required: true
        - name: pathParam3
          in: path
          type: string
          required: true
        - name: flag
          in: query
          type: array
          required: true
          items:
            type: string
          collectionFormat: multi
      responses:
        '200':
          description: 200 response

```
and when a post request is formed to a AWS lambda from the gateway, I create request as

```yml

    requestTemplates:
        application/json: |
        #set(\$allParams = \$input.params())
        {
            "body": {
                "pathParam1": "\$util.urlDecode(\$util.escapeJavaScript(\$input.params().path.get('pathParam1')))", 
                "pathParam2": "\$util.urlDecode(\$util.escapeJavaScript(\$input.params().path.get('pathParam2')))", 
                "pathParam3": "\$util.urlDecode(\$util.escapeJavaScript(\$input.params().path.get('pathParam3')))", 
                "flags": [ 
                #foreach(\$val in \$method.request.multivaluequerystring.get('flag'))
                    "\$val"#if(\$foreach.hasNext),#end
                #end
                ]
            },

```
and the request that is made to lambda is as below

```json
 {
    "pathParam1": "abc",
    "pathParam2": "def",
    "pathParam3": "ghu",
    "flags": ["abc","def"]
 }
```

now while developing locally and testing it out serverless.yml doesn't follow same syntax as api gateway and their documentation doesn't spread out all the samples, so after trial and error here is the configuration that worked for me.

```yml

functions:
  someFunction:
    handler: src/handler.handle
    description: Retrieve values.
    events:
      - http:
          path: some-endpoint/{pathParam1}/{pathParam2}/{pathParam3}
          method: get
          integration: lambda
          request:
            template:
              application/json: '{
                  "body": 
                    {
                      "pathParam1": "$input.params(''pathParam1'')",
                      "pathParam2": "$input.params(''pathParam2'')",
                      "pathParam3": "$input.params(''pathParam3'')",
                      "flags": [
                            #foreach($val in $input.params().querystring.get(''flag''))
                                "$val" #if($foreach.hasNext),#end
                            #end
                      ]
                    }
                }'
          response:
            headers:
              Content-Type: "'application/json'"
            template: $input.path('$.body')

```

differences is there is no mention of query params or path params and way we access them is different that api gateway and serverless documentation has examples for path params but no examples are found for query strings.

Hope this helps out folks who are trying to do this in their serverless.

Happy serverless computing!