---
title: "Jackson Object Mapper"
last_modified_at: 2020-06-06
classes: wide
categories:
  - Tech
tags:
  - Database
  - Java
  - Mongodb
---
## Jackson Object Mapper

There are many tales about Jackson Object Mapper and I have seen many gotchas in my career, and every time I get struck and later find the gotch and always wanted to document.
Here are some of the quirks from last week.

#### GraphQl has it own Object Mapper

we were using Graphql with SpringBoot and we use ISO-8601 and with newer jackson if we have JSR301 module jar in the classpath ObjectMapper gets registered with new JavaTimeModule which deals with newer [Java8 time api](https://docs.oracle.com/javase/8/docs/api/java/time/package-summary.html) , however when using GraphQl we saw Instant type had problems with serializing and deserializing and after spending some time, we found it has its own object mapper and unless we explicitly register this new module it wont pick magically.
``` java
@Bean
public SchemaParserOptions schemaParserOptions() {
  // custom implementation to configure object mapper with new JavaTimeModule
  return SchemaParserOptions.newOptions()
      .objectMapperConfigurer(
          (ObjectMapper mapper, ObjectMapperConfigurerContext context) ->
              mapper.registerModule(new JavaTimeModule()))
      .build();
}
```
#### Object Mapper dealing with JSONObject.Null

We were writing a piece of code to take two JSON as Java Map and do a diff between then and we wanted a special NULL construct to represent to caller and initially we represented as Java “null” it worked when we use ObjectMapper to write it as string however when we use JSONObject ( org.json) it doesn’t write the key out when the value of it is null.

Other option was to use this special construct [JSONObject.NULL](https://stleary.github.io/JSON-java/org/json/JSONObject.html) when we try to serialize this didn’t work with ObjectMapper because this construct doesn’t have serializer or deserializer registered.

So we went back to Java null and when we started using Spring Boot Native object mapper it didn’t include the key when it is null.
eg:
This prints {“a”:null}
``` java
objectMapper.writeValueAsString(Collections.singletonMap("a", null));
```
whereas if you have a map wrapped in a bean then it conveniently skips the null value

``` java
public class InstanceDifferences {
  @JsonProperty(value = "data", required = true)
  private Map<String, Object> data;
}
```
to ensure values of maps are returned always we have to add this additional annotation.
``` java
@JsonInclude // this will ensure nulls in map are displayed as null
```
so my wrapper class becomes
``` java
public class InstanceDifferences {
  @JsonProperty(value = "data", required = true)
  @JsonInclude // this will ensure nulls in map are displayed as null
  private Map<String, Object> data;
}
```
I am sure along the way I am going to find more of these, I hope to document them.
