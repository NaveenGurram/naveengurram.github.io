---
title: "Download file in GWT"
last_modified_at: 2018-09-26
categories:
  - Blog
tags:
  - GWT
  - Java
---
## Download file in GWT

Over the years working on GWT was always fun at the same time I have some many war stories where found quirks along the way to get to the solution. One such was the below one.

The requirement is to provide download feature and my initial idea was to make RPC calls to some service layer which happens to be a servlet on which I can write out content to servlet output stream. In my GWT controller, I planned to leave the RPC async onSuccess response block.

*Note: Servlet extending a RemoteServlet you can get the response by calling getThreadLocalResponse() gives HttpServletResponse*

But in reality even though in my Servlet I write response stream out it doesn’t force the browser to save the file in fact call reaches GWT async onSuccess method. I tried other alternatives of calling a different micro service which forces the download that also didn’t give me my intended experience of downloading the file.

After trying a little bit, I went to implement a native javascript solution in my async method which did the trick. Here is the code block
``` java
public static native void downloadFile(String fileName, String urlData) /*-{
    var aLink = document.createElement('a');
    aLink.download = fileName;
    aLink.href = encodeURI(urlData);
    var event = new MouseEvent('click');
    aLink.dispatchEvent(event);
}-*/;
```