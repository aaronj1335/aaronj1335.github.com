---
layout: post
title: pair programming is busted
author: Aaron Stacy
category: cs373
tags: [code, cs373, pair-programming]
---

this week in [my software engineering course][se] we covered a number of topics
including pair programming. we had to read [three][kindergarten]
[different][ppcs1] [texts][xp], all of which extolled the practice, and we were
assigned a project where we actually engaged in pair programming.

after all of this, i think the arguments fall short. if pair programming is as
great as these sources claim, then why is it so rare in the industry? "but
there are studies!" you say. "but, but... kent beck said so!" you cry. let's
check some of them against reality:

 - go into any sprint planning meeting and tell the project manager that you're
   going to need two programmers for every feature instead of one. after you're
   laughed out of the room, consider the perspective of of the business teams:
   they'll see pair programming as cutting their technical teams' manpower in
   half.  you should know that it doesn't matter if you think you'll be more
   productive with pair programming; it matters that your *team* believes that
   is is a sound *business decision*. that means when you partner up, you need
   to ship twice as much as you would alone.

 - most of the benefits only apply to evenly matched programmers. a project may
   be completed 40% faster and more accurately, but if you're doing correct
   pair programming, that's relative to the lower skill level of the two. and
   40% may seem like a big difference, but it pales in comparison to [the
   potential disparity in skill level between programmers][atwood]. think about
   it, when you're building a team for a project, you wouldn't put all of your
   rockstars on one team; you're going to assign a range of talent levels. so
   the chances that a pair of developers working on the same project are close
   enough in skill to realize those benefits seems slim.

 - one of the most awesome things about a career in software development is
   that you can work from anywhere; you just need a laptop and an internet
   connection.  it's beyond flexible, and that's a big part of why people love
   it. that goes out the window if you have to coordinate schedules with
   someone else.  i would guess that one of the reasons pair programming is
   relatively uncommon is programmers just don't want to sacrifice the
   flexibility.

don't get me wrong, i really enjoyed working with my partner on the project.
beyond that i think there are many cases where it's completely appropriate for
two developers to work together on the same problem. but on the whole i find it
similar to dogmatically applying TDD or side-effect-free function programming:
it just doesn't seem grounded in reality.

in a perfect world, we'd always write our unit tests first, it'd be easy to
find a job writing haskell, and we'd pair program everything (a
[gender-inclusive-bromance][fat], if you will). but as long as i'm living here
on earth, i'll apply these principles with a grain of salt.

[se]: https://www.cs.utexas.edu/users/downing/cs373/drupal/
[kindergarten]: http://www.cs.utexas.edu/users/downing/papers/PairProgrammingKindergarten2000.pdf
[ppcs1]: http://www.cs.utexas.edu/users/downing/papers/PairProgrammingCS12007.pdf
[xp]: http://books.google.com/books?id=l4zO3OWkdIsC&lpg=PP1&pg=PA87#v=onepage&q&f=false
[atwood]: http://www.codinghorror.com/blog/2004/09/skill-disparities-in-programming.html
[fat]: http://byfat.xxx/deleuze-on-working-together
