---
title: "Parallel Threads with Spring Context"
last_modified_at: 2020-04-29
categories:
  - Blog
tags:
  - Spring
  - Java
  - Concurrency
---
## Parallel Threads with Spring Context
We are developing a piece of code and in that we are executing bunch of methods in sequence, and these method are not working on a shared resource so we thought converting that to a parallel might help us with the execution time, so we used [FixedThreadPool](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/Executors.html), however we started seeing some issues with Spring Security Context not available in the methods which are executed in these threads.

There were no errors, but more runtime errors where information we expect wasn’t available, and luckily previous build worked fine and after doing a diff we found only code change we did was to use ThreadPool and digging further we noticed spring context is missing.

Luckily [SecurityContextHolder](https://docs.spring.io/spring-security/site/docs/3.0.x/apidocs/org/springframework/security/core/context/SecurityContextHolder.html) which holds our spring security Authentication object has a property to enable this in inheritable threads via MODE_INHERITABLETHREADLOCAL
```java
SecurityContextHolder.setStrategyName(SecurityContextHolder.MODE_INHERITABLETHREADLOCAL);
```