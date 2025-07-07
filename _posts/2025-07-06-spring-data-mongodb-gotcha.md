---
title: "🚨 Spring Data MongoDB Gotcha That Cost Us Performance!"
last_modified_at: 2025-07-06
categories:
  - Java
tags:
  - Java
  - MongoDB
---

# 🚨 Spring Data MongoDB Gotcha That Cost Us Performance!

If you're using **Spring Data MongoDB** with **`ExampleMatcher`**, here's a performance trap that can silently degrade your application's query performance — and it caught us off-guard.

---

## 🔍 The Problem

We were using `ExampleMatcher` in a Spring Data query like this:

```java
ExampleMatcher.matching()
    .withStringMatcher(StringMatcher.EXACT)
```

We expected it to generate a direct MongoDB match:

```json
{ "someField": "someValue" }
```

But what it **actually** generated under the hood was:

```json
{ "someField": { "$regex": "^someValue$" } }
```

This means `StringMatcher.EXACT` performs a **regular expression match**, not a literal equality.

---

## 🐢 Why This Hurt Performance

At smaller dataset sizes, the difference went unnoticed. But as our collection grew into hundreds of thousands of documents, we began experiencing:

- Increased query latency
- Read timeouts
- Poor index utilization

MongoDB was **not** using indexes effectively because regex queries don’t match equality-based indexes. This led to expensive collection scans.

---

## 📚 What We Learned

After analyzing query patterns in **AWS Performance Insights**, enabling MongoDB's **explain()**, and reviewing the [Spring Data documentation](https://docs.spring.io/spring-data/), we discovered this key detail:

> 🔴 `StringMatcher.EXACT` does **not** perform a true equality comparison.
> It uses a **regex match** with `^` and `$` boundaries — which is slower and non-index-friendly.

---

## ✅ The Fix

To perform true equality matching and enable MongoDB to use indexes, we switched to:

```java
ExampleMatcher.matching()
    .withStringMatcher(StringMatcher.DEFAULT)
```

This lets Spring Data generate a plain field-value query:

```json
{ "someField": "someValue" }
```

Which **does** use indexes and perform optimally.

---

## ⚡ The Result

After making the change, we saw:

- ✅ Significant reduction in query response time
- ✅ No more read timeouts
- ✅ Indexes being hit correctly
- ✅ Reduced database load

---

## 💡 Takeaway

If you're using `ExampleMatcher` in Spring Data MongoDB:

- **Don’t assume** `StringMatcher.EXACT` means “exact match.”
- It’s actually a **regex matcher** (`^value$`), which can **cripple performance** at scale.
- Use `StringMatcher.DEFAULT` for **true equality** and **index-friendly** queries.

---

## 🛡️ Bonus Tip

Always test generated queries with:

```javascript
db.collection.find({ someField: "someValue" }).explain("executionStats");
```

Verify that indexes are being used, and avoid abstraction surprises by **profiling your queries early** — not when you're already in production.

---

> Have you run into similar issues with Spring Data or MongoDB?
> Share your experience — let's help others avoid these hidden pitfalls!
