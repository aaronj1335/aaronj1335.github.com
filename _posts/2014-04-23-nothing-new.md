---
layout: post
title: there is nothing new under the sun
author: Aaron Stacy
notes: .this can be easily dismissed with "right tool for the right job", but my
  point is the right tool, even when you need perf (c++), is still too complex.
  this article has two different points, 1. there's nothing new, and 2. c++ is
  too complex. it should only have one point.
---

i've had the opportunity to do [some][hw3] [c++][proj] lately, and i've been
reading up on [stl iterators][iterator library]. i couldn't help but notice
similar use cases with [input iterators][] and the generators found in
[python][pygenerators] and now [javascript][es6generators], though the
mechanisms are very different. two things stick out to me.

## complexity

c++ iterators are so much more complex than generators. they introduce a
[hierarchy of categories][categories] that provides more control. they (at least
basic c++ iterators) also [conflate traversal and element access][conflate]
&mdash; something i understand that boost attempts to untangle.

is this complexity necessary? it probably allows for higher performance, and
python and javascript don't concern themselves with as much type information as
c++. but is all of that worth the complexity it introduces?

i think it's telling that python and javascript generators provide the lowest
level of iterator functionality and leave the more complex stuff up to the
application. i don't see the necessity for the added complexity, but then again,
i'm still pretty new to c++ &#9786;

## it's all been done before

either way i always find it interesting to learn about concepts that, while new
to some languages, have existed for a while in others. there is still nothing
new under the sun, but there are certainly opportunities to learn from prior
experience.

[hw3]: https://github.com/aaronj1335/cse392-hw3
[proj]: https://github.com/aaronj1335/cs388-final-project
[iterator library]: http://en.cppreference.com/w/cpp/iterator
[input iterators]: http://en.cppreference.com/w/cpp/concept/InputIterator
[pygenerators]: https://wiki.python.org/moin/Generators
[es6generators]: http://wiki.ecmascript.org/doku.php?id=harmony:generators
[categories]: http://en.cppreference.com/w/cpp/iterator#Iterator_categories
[conflate]: http://www.boost.org/doc/libs/1_43_0/libs/iterator/doc/new-iter-concepts.html#motivation
