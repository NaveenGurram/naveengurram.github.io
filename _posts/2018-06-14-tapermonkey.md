---
title: "How Tapermonkey helped me replace safari extensions"
last_modified_at: 2018-06-14T16:20:02-05:00
categories:
  - Blog
tags:
  - Tapermonkey
  - Safari
  - Browser plugins
---
## How Tapermonkey helped me replace safari extensions
I am one of the guy who like to automate small things so they help my productivity, after all that’s what software engineers do, don’t they?

Some of my open source work is on creating Chrome Extensions and they are very small javascript using JQuery, Bootstrap. They are small and easy that can be ported to Safari or firefox with minimum effort.

Chrome extension developer account is 5 buck one time payment and can publish upto 25, apple follows a different approach for Safari extensions. Their developer account is tied with AppStore that makes safari extension developers who choose to not make money from safari extension are subject to pay 99$ yearly subscription. This leaves me people like me not to port extensions to safari, even if I choose to publish and distribute internally.

That’s where [TaperMonkey](tapermonkey.net) helped me write one set of scripts and use it across platforms. Now I am a full fledged Mac Safari user using taper monkey to run my scripts (modifying DOM with help of JQuery) in all browsers exactly the same.

I haven’t tried all kinds but I use it mostly to run scripts which deal with the page DOM.Some of the use cases I tried
- Using JQuery to hide some elements
- Using JQuery to provide custom CSS for the elements.

There are other ways to run Safari Plugin locally, but that stays only for a session until Safari is restarted. I will have another post how I ported my chrome plugin to safari.