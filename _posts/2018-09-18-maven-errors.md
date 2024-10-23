---
title: "Maven TestDependency Errors"
last_modified_at: 2018-09-18
classes: wide
categories:
  - Tech
tags:
  - Maven
  - Java
---
## Maven TestDependency Errors

We started seeing weird test jar dependency error while building our code even when we skipped tests.

Let’s say you have below in your pom.xml, you are essentially telling that we have a dependency on some artifact in test scope.

``` java
<dependency>
    <groupId>${project.groupId}</groupId>
    <artifactId>some-artifact</artifactId>
    <type>test-jar</type>
    <scope>test</scope>
</dependency>
```

When you build with below command, you expect since tests are skipped it wouldn’t fail if the particular artifact is missing.
``` java
mvn clean install -Dmaven.test.skip=true
```
But with this it wouldn’t even compile tests to generate jar file.
``` java
-Dmaven.test.skip=true
```

We have error with this dependency when we bumped our version and never published test artifact to repo.

After fiddling a while on this, we figured it is related to the property and it seems we have to use skipTests which builds tests but won’t run the tests.
``` java
mvn clean install -DskipTests=true
```
#### Conclusion
###### maven.test.skip

Disables both running the tests and compiling the tests.

###### skipTests
Set this to true to skip running tests, but still compile them