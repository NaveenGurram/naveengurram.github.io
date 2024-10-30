---
title: "Calling Graphql mutation using WebClient"
last_modified_at: 2024-10-20
categories:
  - Java
tags:
  - Java
  - Webclient
  - GraphQl
  - Apache Beam
  - Rest
---
Calling Graphql mutation using WebClient
========================================

I had a requirement to call a graphql mutation endpoint from java and even with multiple graphql tools, requirement was to use a standard REST client to make the call and there is not much info out there to show the call is made from java or for that matter how the body look like if you were to make the call using any standard http library.

Here is how query look like, in this example there is a mutation to create an individual

```json
{  
    "query": "mutation createIndividual($individual: CreateIndividualInput!) { createIndividual(individual: $individualInput) { individualId, message }}",  
    "variables": {  
        "individualInput": {  
            "firstName": "test",  
            "lastName": "test",  
            "phoneNumber": "123-123-1234",  
        }  
    }  
}
```
Java code to generate the request using standard libraries and then using webclient to make the call.

```java  
Map<String, Object> variables = new HashMap<>();  
Map<String, Object> individualMap = new HashMap<>();  
  
individualMap.put("email", collectedDataMap.get("emailAddress"));  
individualMap.put("firstName", collectedDataMap.get("firstName"));  
individualMap.put("lastName", collectedDataMap.get("lastName"));  
individualMap.put("phoneNumber", collectedDataMap.get("phoneNumber"));  
individualMap.put("middleName", collectedDataMap.get("middleName"));  
individualMap.put("suffix", collectedDataMap.get("suffix"));  
variables.put("individual", individualMap);  
  
Map<String, Object> mutation = new HashMap<>();  
mutation.put("query", "mutation createIndividual($individual: CreateIndividualInput!) { createIndividual(individual: $individual) { individualId, message }}");  
mutation.put("variables", variables);  
  
String jsonReq = gson.toJson(mutation);  
// call graphql endpoint and get output in map format  
Map output = webClient.post().uri(GRAPHQL\_URL).bodyValue(jsonReq)  
.retrieve()  
.onStatus(httpStatusCode -> httpStatusCode.is4xxClientError()  
        || httpStatusCode.is5xxServerError(),  
    clientResponse -> clientResponse.statusCode().is4xxClientError() ? Mono.error(  
        new IllegalArgumentException("Exception creating individual"))  
        : Mono.error(new IllegalStateException("Exception creating individual")))  
.bodyToMono(Map.class).block();
```
