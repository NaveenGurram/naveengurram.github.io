---
title: "PMD Unused private method"
last_modified_at: 2018-11-02
categories:
  - Tech
tags:
  - PMD
  - Java
---
## PMD Unused private method
We use PMD for static analysis of our code and while doing that we encountered “unused private method” and while our IDE (Intellij in this case) clearly shows that method is used.

Since this method is a private method invoked from another private method which in-turn invoked by a public interface implementation method, so initial suspicion was on the this invocation tree and that effort didn’t help.
``` java
// Entry point
private void startProcess() {
   this.createEvent(a,new JSONObject(b).toString(),c);
}
// method invoked 
private void createEvent(
    String a, String b, String c) {
  // do some logic
}
```
After going through the PMD documentation and looking at some of the bug reports, second argument in startProcess method is the offender since the method is expecting a String type by doing new JSONObject(b) PMD deduces its a different type and is not looking at the toString().

We had to change the code to resolved the second argument as String upfront before passing it to the next method.

``` java
// Entry point
private void startProcess() {
   String str = new JSONObject(b).toString();
   this.createEvent(a,str,c);
}
```
This seems like a counter intuitive thing, now just for PMD we are creating a variable and increasing the number of lines in the program and on the flip side might be more readable.

Below are the links to the rule and bug report which did give out some clue to fix it.

https://pmd.github.io/pmd-5.8.1/pmd-java/rules/java/unusedcode.html#UnusedPrivateMethod

https://sourceforge.net/p/pmd/bugs/1156/