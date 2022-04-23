---
title: "Creating Compound Unique Index in AWS DocumentDB"
last_modified_at: 2020-05-14
categories:
  - Tech
tags:
  - Database
  - Java
  - Mongodb
---
## Creating Compound Unique Index in AWS DocumentDB

![](../assets/images/docdb/logo.png)

In this I want to describe problem we faced and solution, just in case helpful for folks looking for solution, because I haven’t find any and has to rely on AWS support.

Let me describe the problem.

We are relying on scripting Indexes for our DocumentDb cluster by executing scripts in mongodb shell. We created a unique compound index and and didn’t verify whether it was created, because mongo shell gives immediate feedback of whether script was able to create index or not but it doesn’t tell you whether it is of type “unique” or not in this case.

Below is the initial script
``` bash
db.collection.createIndex(
        { field1: 1, field2: 1, field3: 1, field4: 1 },
    { name: "instc_indx1"},
    { unique: true}
);
```
with this one we were able to create a compound index but it wasn’t unique.

After struggling for couple of days, searching mongo documentation, forums etc, we opened a ticket with AWS and they were able to suggest change in the syntax to achieve what we were looking
``` shell
db.collection.createIndex(
        { field1: 1, field2: 1, field3: 1, field4: 1 },
    { name: "instc_indx1", unique: true }
);
```
difference is we need to combine “name” and “unique” property in a single statement.

**Note:** if you create without name it works, reason we had to give a name instead of relying on the system generated was because mongo generated was exceeding the size in Mongo itself.