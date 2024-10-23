---
title: "Navigating the Node.js \"Unsupported\" error with PFX Certificates in HTTPAgent"
last_modified_at: 2024-03-01
classes: wide
categories:
  - Node.js
tags:
  - Node.js
  - Certificates
  - PFX
  - Fetch
---
# Navigating Dreaded "Unsupported" error with HTTPAgent in Node.Js

![](/assets/images/nodejs.webp)

If you ever worked with [Node Fetch](https://www.npmjs.com/package/node-fetch) to connect to an https endpoint using HTTPAgent especially with Node 18+ you might have encountered dreaded unsupported error as below

```Javascript
Error: unsupported
  at configSecureContext (node:internal/tls/secure-context:278:15)
  at Object.createSecureContext (node:_tls_common:117:3)
  at Object.connect (node:_tls_wrap:1641:48)
  at Agent.createConnection (node:https:150:22)
  at Agent.createSocket (node:_http_agent:341:26)
  at Agent.addRequest (node:_http_agent:288:10)
  at new ClientRequest (node:_http_client:342:16)
  at Object.request (node:https:358:10)
```
when your code 

```javascript
  const agent = new https.Agent({ pfx: s.readFileSync(__dirname + '/cert.pfx');,passphrase: ''});

  res = await fetch( 'https://example.com',
      {
          method: 'POST',
          body: JSON.stringify(body),
          headers: {'Content-Type': 'application/json'}
          headers: {'Content-Type': 'application/json'},
          agent: agent,
      });
  data = await res.text();
```

and upon searching stack overflow and other forums most of them suggest to use
 ```javascript
NODE_OPTIONS=-openssl-legacy-provider
``` 
I had similar run with the problem, when we were trying to connect using a p12 file, if you understand the error, the certificate we are using is not up to the current standards so we are telling Node.js to fall back on legacy implementation.

In my case, I was happy to apply node options when testing locally, however when running in AWS lambda, these weren't option for me, even though I set them AWS lambda runtime didn't work accordingly.

So as alternative is to get a new cert with new standards or transform the existing one, I choose the later to verify just before asking external partners to regenerate new cert.

I used a tool [KeyStore Explorer](https://keystore-explorer.org/) to generate a new PFX and with the help of that new file I was able to overcome the error.

This regeneration is not going to impact the authenticity of the cert, just that we are wrapping it as new so Node.js could parse without the option to fall back on legacy. 

here are screenshots showing how to do it with keystore.

![](/assets/images/keystore/1.png)

![](/assets/images/keystore/2.png)