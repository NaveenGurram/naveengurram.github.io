---
title: "Python file writing mishaps"
last_modified_at: 2023-08-24
classes: wide
categories:
  - Programming
tags:
  - Python
  - AppStoreApi
---

We had a requirement to pull data from Apple [AppStoreApi](https://developer.apple.com/documentation/appstoreconnectapi) and api response comes as compressed tab separated file and we coded it in python and quickly deployed to DEV and QA. After initial validation we started noticing number of rows we are getting from same AppStore Environment between DEV and QA is different and   quickly turned out local,DEV and QA are pulling different number of rows.

After initial round, we quickly realized it is not the API that's fault here, as we compared the number of rows in the compressed file it is quickly evident its the way we are parsing the response and writing to CSV.

Below is the our initial code.
```python
import csv

txt_file = r"mytxt.txt"
csv_file = r"mycsv.csv"
in_txt = csv.reader(open(txt_file, "rb"), delimiter = '\t')
out_csv = csv.writer(open(csv_file, 'wb'))

out_csv.writerows(in_txt)
```
while writing itself I noticed there is no way to flush after writing it to the file and assumed CSV python module takes care of it, in reality no such thing exists in the library, then I had to quickly rewrite the code as below to fix the problem.

```python
import csv

txt_file = r"mytxt.txt"
csv_file = r"mycsv.csv"
in_txt = csv.reader(open(txt_file, "rb"), delimiter = '\t')
csvF=open(csv_file, 'wb')
out_csv = csv.writer(csvF)
out_csv.writerows(in_txt)
csvF.flush()
csvF.close()
```
lesson learnt concise doesn't always means right way.