---
title: "PMD Cyclomatic Complexity"
last_modified_at: 2020-05-14
categories:
  - Blog
tags:
  - Database
  - Java
  - Mongodb
---
## PMD Cyclomatic Complexity


If you are developing code, and running PMD as static code analysis you might have encountered violations and in this post I want to talk about my experience and how I fixed violations.

![](../assets/images/pmd/logo.png)

Recently I wrote a piece of code which is a helper class and designed it to be a single class with a sole purpose, and as it grew over the time, started seeing [PMD Cyclomatic Complexity](https://pmd.github.io/pmd-6.17.0/pmd_rules_java_design.html#cyclomaticcomplexity) violation and I tried different things to avoid but it never went away and it started some anxiety even though I try to justify there were no other ways code is complex or unmanageable.
Here is the example showing from PMD website
#### Example(s):
``` java
class Foo {
  void baseCyclo() {                // Cyclo = 1
    highCyclo();
  }
void highCyclo() {                // Cyclo = 10: reported!
    int x = 0, y = 2;
    boolean a = false, b = true;
if (a && (y == 1 ? b : true)) { // +3
      if (y == x) {                 // +1
        while (true) {              // +1
          if (x++ < 20) {           // +1
            break;                  // +1
          }
        }
      } else if (y == t && !d) {    // +2
        x = a ? y : x;              // +1
      } else {
        x = 2;
      }
    }
  }
}
```
in my case, since I was writing a helper method and I have some convenience method which are calling other methods within the class and as per requirements I have lot of if/else loops and that started increasing the complexity and after reading posts in stack overflow and others, applied some of the techniques and able to fix the violation.
#### Modifications
Before
``` java
for(int i=0;i<10;i++){
  if(object instanceof String){
    // string
  }else if(object instanceof Map){
    // map
  }else if(object instanceof List){
    // list
  }else{
    // primitive
  }
}
```
Changed to return from certain blocks if there is no additional processing
``` java
for(int i=0;i<10;i++){
  if(object instanceof String){
    // process
    continue;
  }
  if(object instanceof Map){
    // process
    return process();
  }
  if(object instanceof List){
    // list
  }else{
    // primitive
  }
}
```
Extracted all helper methods to a static class to avoid adding complexity to existing blocks.
   
When chaining method complexity will also get appended, to break the chain, if there are methods which could be a static method, those are exposed as separate classes or convert to a static method within the context also helped reduced complexity.

Extracted some of the code as Java Functional interface methods which as static final variables.
   
Before all these fixes, complexity came around 80 and after making changes I was able to remove the violation.
