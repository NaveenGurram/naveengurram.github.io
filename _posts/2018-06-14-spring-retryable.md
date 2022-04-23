---
title: "Spring Retryable Mocking"
last_modified_at: 2018-06-14T16:20:02-05:00
categories:
  - Blog
tags:
  - Mock
  - Java
  - Unit testing
  - Spring
---
## Spring Retryable Mocking

Spring retryable is a spring own’s implementation of in-memory retry. I found a weird issue while doing Junit testing and trick that saved the day for me.

We have integration tests which uses retryable interface marked with test profile for our JUnits and when we try to autowire them by name, autowire failed. Retryable interface is using proxy rather than concrete implementation and to make matte worse, we have a public filed in implementation not defined in interface.

It took quite a while to figure out alternatives like doing a mock but these tests being integration tests we couldn’t convert all of them at once to use mocks.

Trick that saved the day was to use AopTestUtils to generate a concrete service class on that we used reflection to set field value.

```java
JunitConcreteService serviceWithoutProxy 
     = AopTestUtils.getUltimateTargetObject(serviceImpl);
     
ReflectionTestUtils.setField(serviceWithoutProxy, "user", someDto);
```