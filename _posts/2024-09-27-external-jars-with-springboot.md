---
title: "Augment Spring boot app with external jars"
last_modified_at: 2024-09-27
classes: wide
categories:
  - Java
tags:
  - SpringBoot
  - Java
---
Augment Spring boot app with external jars
=============================================

Spring Boot packaging to run as a standalone jar has it advantages, like you can pack all the dependencies into single uber jar and run it on the command line is is refreshing and with the amount of tooling support for build framework is more appealing to use a spring boot framework in the first place.

I had a requirement to add an external jar to the spring boot after it is packaged, you might ask why can’t you package it at build time, requirement was like that after a spring boot jar is created, during runtime I want to augment it with external jar and here are some of the experiments about getting it right.

[Java Xbootclasspath](https://docs.oracle.com/cd/E15289_01/JRCLR/optionx.htm#i1018570)
--------------------------------------------------------------------------------------

Initially jar I want to add to spring boot was a plain simple java function without any external dependencies and I was able to use it to append to the classpath.

```bash
java -Xbootclasspath:a/path/augumented.jar -jar application.jar
```

with the above I was able to load it into classpath but not without limitations, if this jar we are augmenting has any other dependencies and unless that jar is a another fat jar and even if the existing spring boot has those dependencies, reason being this is loaded as first classloader and that will need to have all the dependencies.

Modifying the spring boot jar
-----------------------------

Since this is an jar file, I can extract it and add required libraries and put the jar back. And spring boot gives good documentaiton how the jar looks like [https://docs.spring.io/spring-boot/specification/executable-jar/index.html](https://docs.spring.io/spring-boot/specification/executable-jar/index.html) and based on the understading, I ran below script to add my additional jar at the run time.

```bash
jar -x -f application.jar  
\# this extracts as folders BOOT-INT META-INF com  
  
\# add the new jar to BOOT-INF/lib and add an entry to classpath.idx  
cp new.jar ./BOOT-INF/lib  
echo '- "BOOT-INF/lib/new.jar"' >> BOOT-INF/classpath.idx  
  
\# then assemble the jar and don't compress   
jar -c -f application.jar -0 -m META-INF/MANIFEST.MF BOOT-INF META-INF com
```

with above steps essentially open the package add new and repackage and it works as expected.

Using Spring boot property loader
---------------------------------

with this approach while building the jar change the main-class to the propertyLoader from jarLauncher.

*   Note: I haven’t verified it, but here are changes

```groovy
bootJar {  
    mainClass.set('com.example.SampleApp')  
    enabled = true  
    archiveClassifier = 'boot'  
    manifest {  
        attributes 'Main-Class': 'org.springframework.boot.loader.PropertiesLauncher'  
    }  
}
```

provide new loader path with all the properties and jars. Documentation [https://docs.spring.io/spring-boot/specification/executable-jar/property-launcher.html](https://docs.spring.io/spring-boot/specification/executable-jar/property-launcher.html) has all the required info.

Hope this help anyone who is trying to augment new classes dynamically for spring boot.
