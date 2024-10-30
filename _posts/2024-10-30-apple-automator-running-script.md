---
title: "Using Apple Automator to open webpage and run script"
last_modified_at: 2024-10-20
categories:
  - Automator
tags:
  - Automator
  - Tapermonkey
  - Script
---
Sometime back, I wrote an [article](https://medium.com/i-me-myself-naveen/sample-story-e15a7af54687) how I was using [Tapermonkey](https://www.tampermonkey.net/) to replace extension on the browsers when I want to run some script on the page.

I was using this effectively to not write custom plugins to run some script on a webpage, whether it is to change the dom to present it differently or to block some url’s. My company recently implemented a security policy where all extensions are removed and only approved extension can be installed in the browsers, and guess what Tapermonkey is not there and essentially made all my nifty scripts useless.

I was trying to find another way to be able to run these scripts and that when I stumbled on apple automator which comes with Mac operating system.

before this I used Automator to automate lot of mundane tasks like opening a webpage without going to a browser or running some scripts and for all these, I create an application and that is visible in Mac spotlight search and easier to invoke them via keyboard for me.

Coming back to my requirement, earlier I was using tapermonkey to run a script to select a radio button on a page and submit the form, this is like a internal SSO page where you select an app to go to that, but instead of manually doing it I was doing it via script.

Now that same thing I am doing it with automator and as a bonus I didn’t even have to go to browser to select the url, that part is also done by my automator.

Here is the script and I will explain step by step how to set it up.

```applescript
on run {input, parameters}
 tell application "Google Chrome"
  tell front window
   set curTabIndex to active tab index
   set URL of (make new tab) to ¬
    "https://designsystem.digital.gov/components/radio-buttons/"
   repeat until (loading of active tab is false)
    delay 0.1
   end repeat
   tell active tab to execute javascript ¬
    "document.getElementById('historical-figures').checked = true"
   tell active tab to execute javascript ¬
    "document.getElementById('submit').click();"
  end tell
 end tell
end run
```

Automator is telling application “Google Chrome” to open a url in a new tab and make it active and wait for the page to load and once opened, select a radio button by id and then click a button.

once saved this can be invoked via spotlight search ( command + spacebar).

1. Open automator and select “Application”
![](/assets/images/automator/1.png)
2. look for “Run Applescript” by searching in library
![](/assets/images/automator/2.png)
3. Drag “Run AppleScript to right side”
![](/assets/images/automator/3.png)
4. put in the script and test it by clicking the ‘run’ button.
![](/assets/images/automator/4.png)

---

Hope this helps someone trying to automate some scripts, in next post, I will cover how I am using automator to run scripts or code.