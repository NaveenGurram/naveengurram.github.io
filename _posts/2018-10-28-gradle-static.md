---
title: "Externalize static analysis configs in Gradle"
last_modified_at: 2018-11-28
categories:
  - Tech
tags:
  - Gradle
  - Java
  - PMD
  - Spotbugs
---
## Externalize static analysis configs in Gradle
With Gradle for a project we can create config files in the project and refer them relative to root project.

```
checkstyle {
    toolVersion = "8.0"
    configFile = rootProject.file('config/checkstyle/checkstyle.xml')
    sourceSets = [] // disables checkstyle with normal 'build' task, to run checkstyle tasks specify directly on command line
    ignoreFailures = false
    showViolations = true
}

pmd {
    toolVersion = "5.8.1"
    ruleSetFiles = rootProject.files("config/pmd/ruleset.xml")
    sourceSets = []
}

findbugs {
    toolVersion = "3.0.1"
    excludeFilter = rootProject.file("config/findbugs/findbugs-exclude.xml")
    sourceSets = []
}
```
in my case we have multiple micro services and we wanted to use same set of configurations and here is how we achieved it.

Created new module with the configuration files and created a jar and published to a remote artifactory and then added that jar in our dependency and modified tasks to read configuration files from the jar as below.

```
checkstyle {
      toolVersion = "8.0"
      config = project.resources.text.fromString(getClass().getResource("checkstyle.xml").text)
      sourceSets = [] // disables checkstyle with normal 'build' task, to run checkstyle tasks specify directly on command line
      ignoreFailures = false
      showViolations = true
  }

  pmd {
      toolVersion = "5.8.1"
      ruleSetConfig = project.resources.text.fromString(getClass().getResource("pmd-ruleset.xml").text)
      sourceSets = []
  }

  findbugs {
      toolVersion = "3.0.1"
      excludeFilterConfig = project.resources.text.fromString(getClass().getResource("findbugs-exclude.xml").text)
      sourceSets = []
  }
```  
Static analysis gradle plugins allows options to load file or set it as resourceFile.