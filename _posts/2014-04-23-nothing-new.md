---
layout: post
title: there is nothing new under the sun
author: Aaron Stacy
published: false
---

i've had the opportunity to do [some][hw3] [c++][proj] lately, and i've been
reading up on iterator concepts, specifically boost's [iterator facade][]. i
couldn't help but notice the similarities between [incrementable iterators][]
and the generators found in [python][pygenerators] and now
[javascript][es6generators].

c++ iterators are more complex than generators though.  they introduce a
[heirarchy of concepts][concepts] that provides more control. they (at least
basic c++ iterators) also [conflate traversal and element access][conflate]
&mdash; something i understand that boost attempts to untangle.

so is this complexity necessary? it probably allows for higher performance, and
python and javascript don't concern themselves with as much type information as
c++. but is all of that worth the complexity it introduces?

i think it's telling that python and javascript provide only generators, and
leave the higher level iterator concepts up to the application. i don't see the
necessity for the added complexity, but then again, i'm still pretty new to c++
&#9786;.

either way i always find it interesting to read about concepts that, while new
to some languages, have existed for a while in others. there's still nothing
new under the sun.

[hw3]: https://github.com/aaronj1335/cse392-hw3
[proj]: https://github.com/aaronj1335/cs388-final-project
[iterator facade]: http://www.boost.org/doc/libs/1_43_0/libs/iterator/doc/iterator_facade.html
[incrementable iterators]: http://www.boost.org/doc/libs/1_43_0/libs/iterator/doc/new-iter-concepts.html#incrementable-iterators-lib-incrementable-iterators
[pygenerators]: https://wiki.python.org/moin/Generators
[es6generators]: http://wiki.ecmascript.org/doku.php?id=harmony:generators
[concepts]: http://www.boost.org/doc/libs/1_43_0/libs/iterator/doc/new-iter-concepts.html#iterator-traversal-concepts-lib-iterator-traversal
[conflate]: http://www.boost.org/doc/libs/1_43_0/libs/iterator/doc/new-iter-concepts.html#motivation
