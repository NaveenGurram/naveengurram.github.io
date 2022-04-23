---
title: "Reverse Lucene Index"
last_modified_at: 2018-06-30
categories:
  - Blog
tags:
  - Lucene
  - Java
---
## Reverse Lucene Index

[Apache Lucene](https://lucene.apache.org/) is a free and open-source information retrieval software library, originally written completely in Java by Doug Cutting. It is supported by the Apache Software Foundation and is released under the Apache Software License.

![](/assets/images/lucene/lucene_logo.png)

#### Apache Lucene
We were using Lucene throughout the years to store data and in one particular instance I had to get some data that is stored with Lucene as “no store” which means this information can be used in searches but cannot be retrieved, which is perceived one the security features. When need arise to get this information we had to go to some of the internals to get that info.
Approach we followed which I am going to describe is not a new one, and one famous example of this is used in Luke tool http://www.getopt.org/luke/

#### Reverse Index

Theory behind this is Lucene creates index so retrieval is easy, in case of “no store” they are stored as separate index along with the document Id. So when we are doing this reverse index first we find all the terms and for each term we will get all the documents (this is done because there is an index Lucene maintains for all terms) .

#### Algorithm
- Extract all the terms
- For each term find all the documents
- If document is the list which we are searching for found, then that term is part of the document

#### Java Code

``` java
// creates an multimap of key and participants.
public static ListMultimap<String, String> termKeyMap = ArrayListMultimap.create();

public static void reInvertIndex(){
    Directory directory = FSDirectory.open(LUCENE_FILE);
    IndexReader indexReader = IndexReader.open(directory, true);
    IndexSearcher indexSearcher = new IndexSearcher(indexReader);
    BooleanQuery booleanClauses = new BooleanQuery();
    booleanClauses.add(new TermQuery(new Term(FLD_A, FLD_A_VAL)), BooleanClause.Occur.MUST);
    booleanClauses.add(new TermQuery(new Term(FLD_B,FLD_B_VAL)), BooleanClause.Occur.MUST);
    booleanClauses.add(new TermQuery(new Term(FLD_C,FLD_C_VAL)), BooleanClause.Occur.MUST);
    TopDocs topDocs = indexSearcher.search(booleanClauses, Integer.MAX_VALUE);
    System.out.println("Number of documents: "+topDocs.scoreDocs.length);

    // get all participants unique terms.
    TermEnum terms = indexReader.terms(new Term(TERMS_FLD));

     while (terms.next()) {
        final Term term = terms.term();
        if(term.text().startsWith(XYZ_VAL) || term.text().startsWith(YUX_VAL)) {
            // for each term find out corresponding keys.
            searchByTerm(indexReader,term.text());
        }
    }
}
private static void searchByTerm(IndexReader indexReader,String term) throws Exception {
    TermDocs termDocs =  indexReader.termDocs(new Term(TERMS_FLD,participant));
    System.out.println("Searching all docs for term Value: "+term);
    while(termDocs.next()){
        // get key for docid, because we only understand key. Doc is for lucene.
        String key= getKeyForDoc(indexReader,termDocs.doc());
        if(key != null) {
            termKeyMap.put(key, term);
        }
    }
}

// print all the key value to a file.
for (String keyValue : termKeyMap.keySet()) {
    List terms = termKeyMap.get(keyValue);
}
```

#### Conclusion
If we choose to store some of the values as “no store” then with above strategy we can find them, however note that this reverse index process is very time and memory intensive especially if your index is big.