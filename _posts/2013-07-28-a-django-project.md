---
layout: post
title: 'a "django" project'
author: Aaron Stacy
category: cs373
tags: [javascript, cs373]
---

the [big group project][reqs] in my software engineering course involves
creating:

> a Django app with Python that emulates IMDB to track world crises

our team has been working hard, and i'm happy to say that our django app is
coming along nicely:

<div class=inset><img src=/assets/images/django-app.png /></div>

&hellip;err wait&hellip; 98% javascript? that can't be right&hellip; sometimes
github gets these counts wrong:

    astacy∂ʇoqǝɔɐʇs ☠ ~/code/cs373/wcdb  03:43:57 Jul25
    § cloc crisis crisis_app
          81 text files.
          81 unique files.
          10 files ignored.

    http://cloc.sourceforge.net v 1.58  T=2.0 s (38.0 files/s, 25414.0 lines/s)
    ---------------------------------------------------------------------------
    Language                 files          blank        comment           code
    ---------------------------------------------------------------------------
    Javascript                  30           5430           7331          25467
    CSS                         14           1589             96           8112
    Python                      16            268            123           1342
    HTML                        14             29              0            707
    XML                          2             21             13            300
    ---------------------------------------------------------------------------
    SUM:                        76           7337           7563          35928
    ---------------------------------------------------------------------------

well that brings it down to 70% javascript, but that still seems kind of high
for a "django app written in python". where is all of that coming from?

    astacy∂ʇoqǝɔɐʇs ☠ ~/code/cs373/wcdb  03:50:52 Jul25
    § ll crisis_app/static/crisis_app/js/
    total 1352
    -rwxr-xr-x  1 astacy  staff   61962 Jul 12 02:48 bootstrap.js
    -rw-r--r--  1 astacy  staff    9893 Jul 25 06:29 inlineComplete.js
    -rwxr-xr-x  1 astacy  staff  507769 Jul 12 02:48 jit.js
    -rw-r--r--  1 astacy  staff    2544 Jul 25 06:29 jt.js
    -rwxr-xr-x  1 astacy  staff   66617 Jul 12 02:48 masonry.js
    -rwxr-xr-x  1 astacy  staff   15330 Jul 12 02:48 pScrollbar.js
    -rwxr-xr-x  1 astacy  staff    4743 Jul 25 06:29 slimbox2.js
    -rwxr-xr-x  1 astacy  staff    4750 Jul 12 02:48 treemap.js

ooooooh right so it's all of those javascript libraries we copied into our app.
so there are way more lines of javascript in this project than python, but do
all of those make it a "javascript app"?

### naw

we shouldn't have to worry about that. if we were going to count all of that,
then we should probably count all of the third-party python that's powering our
site as well, right? and really the javascript is mostly just accomplishing
fringe functionality&hellip;

### but&hellip; yea

the issue is that javascript, like any other code, can still cause bugs, can
still have regressions, and can still make your team miss deadlines. conversely
it can also implement features that sell software, features that users
&hearts;, and features that make difference between a good product and a bad
one.

## the problem with ignoring frontend code

this project is all about good software engineering (testing, documentation,
etc), but we've got a hall pass on anything that runs in the browser.  that
sends mixed messages about the importance of these practices.

what's more, pages without a really interactive UI (accomplished via frontend
code) are weird and out of place on the internet these days. they're even less
interesting than pages without a database backend.

## tractability

i get it though, there's enough to go over in a single semester, we can't talk
about everything, so why talk about frontend stuff? i'm a firm believer in
shutting up unless you've got a solution, so here's my proposal:

 - ditch all the stuff about xml and uml in favor of frontend related topics:
   this may sound like bias, but spend some time talking to product managers
   and ask them to compare the time they schedule for frontend technologies vs.
   xml and uml. i think you'd be hard pressed to find projects weighted towards
   the latter. and i'm not talking about artifactual knowledge like which
   browser versions support what flavor of flexbox, i'm talking more about
   asynchronous programming, design patterns like mv\* vs reactive, and what in
   the world is a "restful api".

 - use an app framework that's focused on the frontend: frankly there's just
   not time in a single semester to learn how to write effective unit tests on
   the backend and frontend, so why bother with all of the backend code?  the
   industry is finding the duplication of effort inefficient too, and it's
   responding by shifting application code to the browser (which is a powerful
   beast these days). you can see evidence of this in frameworks like
   [meteor][], [ember][], and [hoodie][], which treat the server as little more
   than a database thinly wrapped with a restful json api.

if we were learning about software engineering by writing a game or a kernel
driver or a programming language, then javascript and css wouldn't matter.  but
we're making a website, so let's take the opportunity to get into some of these
technologies.

[reqs]: http://www.cs.utexas.edu/users/downing/cs373/drupal/wcdb2
[stephen]: https://github.com/UTAustin
[meteor]: http://www.meteor.com
[ember]: http://emberjs.com
[hoodie]: http://hood.ie
