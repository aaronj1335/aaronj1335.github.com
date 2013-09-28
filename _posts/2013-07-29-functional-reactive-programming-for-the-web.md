---
layout: post
title: functional reactive programming on the web
author: Aaron Stacy
category: cs373
tags: [code, cs373, javascript]
---

i read [the flapjax paper][flapjax] for my software engineering class at UT. it
presents a language and framework for functional reactive programming in
javascript that's suitable for the web. i think it has some really powerful
ideas that could make it a better design pattern than [mvc][] (or [mv*][addy])

aside from sounding like academic bull<img alt="hankey" src="/assets/images/emoji/hankey.png" class="emoji">, functional reactive programming
is a complicated concept. so let's begin with an over-simplified example to
motivate the problem.

## state

pretend you're writing an e-mail client web app (like gmail). in the main view
on the left you've got a link to the inbox with the number of unread messages,
and on the right you've got the list of messages with the unread ones marked in
bold.  if the user marks a message as read, you need to do two things:
un-embolden the text, and change the count of unread messages. so you write a
function called `messageWasRead()` to do so.

this seems pretty simple, but as your application grows it gets tricky to
remember all the little things that need to happen for any given action.
suddenly that `messageWasRead()` function is 700 brittle lines long and an
absolute monolith that you can't reuse in any other context.

we're talking about application state here. the message list and unread count
are just two different views of that same state, which, in large apps, becomes
large, unruly (unsavory even), and impossible to reason about comprehensively.
since we're [simple creatures][seven], developers have come up with patterns
for managing state, the most popular of which currently seems to be mv\*.
reactive programming is an alternative that's been around for a while but is
gaining popularity.

## main concepts

flapjax elegantly distills the world of application programming down into two
concepts (which is one less concept than mvc, ipso facto, functional reactive
is more elegant &lt;/joking&gt;):

### behaviors

behaviors are values that may change over time, like your age. if you set a
regular variable to the value of your age, then it's no longer correct after
your birthday. behaviors on the other hand update over time, so a behavior
representing your age will return your current age regardless of when you check
it's value.

behaviors are kind of like cells in a spreadsheet. if you've got a column of
numbers and a cell that calculates the sum, updating one of the rows will
also update the sum. behaviors similarly update themselves if any of the values
upon which they depend change.

### event streams

user interactions like clicks can't be modeled with behaviors since they're
discrete in time. it doesn't make sense to "check the value of a click," so
flapjax introduces event streams. event streams are instantiated with a
function that takes some event data and returns a value. each time the event
occurs, the function runs. the event stream can then be treated like a behavior
whose value is the item returned the last time the event fired.

## building applications

if you're used to more common approaches of app development, it's probably hard
to see how we could use the above to actually build anything. there are
[numerous (higher quality) examples][demos], but consider this short example
from the paper: a timer that displays the number of seconds passed, and a
button to reset it. the strait-forward implementation might look something like
this:

    <html>
      <head>
        <script>
          var timerID = null;
          var elapsedTime = 0;

          function doEverySecond() {
            elapsedTime += 1;
            document.getElementById("curTime").innerHTML = elapsedTime;
          }

          function startTimer() {
            timerId = setInterval("doEverySecond()", 1000);
          }

          function resetElapsed() {
            elapsedTime = 0;
          }
        </script>
      </head>
      <body onload="startTimer()">
        <input id="reset" type="button" value="Reset" onclick="resetElapsed()"/>
        <div id="curTime"></div>
      </body>
    </html>

this is about as basic of a javascript app as it gets, but essentially on page
load we're setting an interval every second that does two things:

 - update the elapsed time
 - set the page content to reflect that value

the problems may not be apparent in such a trivial example, but remember what
we said about state -- as the application grows it gets hard to manage. we've
left ourselves no way of tracking  updates to the `elapsedTime` variable (state
changes) without re-writing `doEverySecond` and `resetElapsed`.

the functional reactive approach looks like this:

    <html>
      <head>
        <script src='http://www.flapjax-lang.org/fx/flapjax.js'></script>
        <script>
          function loader() {
            var nowB = timerB(1000);
            var resetEl = document.getElementById('reset');

            var clickTimeB = $E(resetEl, 'click')
              .snapshotE(nowB)
              .startsWith(nowB.valueNow());

            var elapsedB = liftB(function(now, start) {
              return Math.floor((now - start) / 1000);
            }, nowB, clickTimeB);

            insertDomB(elapsedB, 'curTime');
          }
        </script>
      </head>
      <body onload='loader()'>
        <input id='reset' type='button' value='Reset'/>
        <div id='curTime'></div>
      </body>
    </html>

 - `var nowB = ...`: here we're creating a behavior whose value is the current
   time (in milliseconds). it updates every second.

 - `var clickTimeB = ...`: we're creating a behavior whose value is the last
   time the reset button was clicked and initializing it to the current time.

 - `var elapsedB = ...`: we're creating a behavior from `nowB` and `clickTimeB`
   which represents the seconds elapsed since the last click. notice that if
   either `nowB` or `clickTimeB` update, `elapsedB` will also update.

 - `insertDomB(...)`: we are binding the value of the `elapsedB` behavior to the
   `curTime` element.

though this approach looks like just as much code, we have isolated state in
the behavior variables. as long as we have a reference to `elapsedB`, we not
only know the amount of time elapsed, but we can also observe updates whenever
it changes. if want to react to changes, we don't have to rewrite any of our
existing code, we just need `elapsedB`.

### a more involved example

none of this caught my eye until i saw a functional reactive implementation of
[a draggable UI component][fjdnd]. drag and drop is easy to get wrong; i know
because my first attempt was [a train wreck][dnd]. the authors do a much better
job of explaining their code in section 2.4 of [their paper][flapjax] than i
could, but the approach is both succinct and elegant. it's interesting to
compare the level of complexity to jquery-ui's [draggable
implementation][jqui], or even [jeremy kahn's][jeremykahn] relatively simple
[library][dragon], even if it is apples-to-oranges since those address a much
wider array of use cases.

## is it worth it?

if you're thinking that all of this is solved by frontend mv\* frameworks,
you're largely correct. the majority of webapps map pretty well to [crud][]
operations on [rest][]ful api's. mv\* crushes in those applications because it
makes sense to have a model class describing each resource. for example if
you've got an api for fetching users, you have a `User` class that inherits
from the base `Model` class, and as long as you're rendering your views from a
shared instance of that model, everything works well.

reactive programming upholds the same solid principles of isolating state to a
[single point of truth][spot], but it applies them at a much finer granularity.
the obvious benefit is it addresses situations where mv\* patterns couldn't
help you (such as drag and drop or data models more complex than rest).

the two major downsides i see to reactive programming are:

 - it's initially difficult to wrap your head around it: i love learning new
   approaches and design patterns, especially when they'll benefit in the long
   run, but choosing niche technologies makes it a lot harder to hire teammates
   because not many folks are using or teaching it.

 - it's hard to debug: setting breakpoints in an mv\* app is a powerful way to
   find problems. my experience with reactive programming is it gets hard to
   determine the source of updates. reactive programming essentially builds a
   graph of data dependencies. changes precipitate their way through the graph
   and sometimes for the sake of performance this happens asynchronously (to
   allow other calculations to occur). not only is it difficult to get a full
   picture of what dependency triggered an update, one also cannot step through
   the code in a debugger.

## related work

there's a lot of folks making libraries that implement various levels of
functional reactive programming on the web. here are a few:

 - [rxjs][]
 - [baconjs][]
 - [knockout][]
 - [meteor][]
 - [frb][]

i've got a fair amount of experience with knockout, and i've really enjoyed
working with it. i think it scales well with the messier parts of big apps,
such as asynchronous input validation.

[flapjax]: http://cs.brown.edu/~sk/Publications/Papers/Published/mgbcgbk-flapjax/paper.pdf
[mvc]: https://google.com/search?q=mvc
[seven]: http://www.psych.utoronto.ca/users/peterson/psy430s2001/Miller%20GA%20Magical%20Seven%20Psych%20Review%201955.pdf
[fjdnd]: http://www.flapjax-lang.org/try/index.html?edit=drag.html
[dnd]: https://github.com/aaronj1335/gloss/blob/master/src/widgets/draggable.js
[jeremykahn]: https://twitter.com/jeremyckahn
[jqui]: https://github.com/jquery/jquery-ui/blob/master/ui/jquery.ui.draggable.js
[dragon]: https://github.com/jeremyckahn/dragon/blob/master/src/jquery.dragon.js
[addy]: http://addyosmani.com/blog/short-musings-on-javascript-mv-tech-stacks/
[crud]: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete
[rest]: http://en.wikipedia.org/wiki/REST_API
[spot]: http://www.catb.org/~esr/writings/taoup/html/ch04s02.html#spot_rule
[rxjs]: https://github.com/Reactive-Extensions/RxJS
[baconjs]: https://github.com/raimohanska/bacon.js
[knockout]: http://knockoutjs.com
[meteor]: http://www.meteor.com
[frb]: https://github.com/montagejs/frb
[demos]: http://www.flapjax-lang.org/demos/
