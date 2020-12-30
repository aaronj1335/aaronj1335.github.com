---
layout: post
title: the problem with the professor's code
author: Aaron Stacy
category: cs373
tags: [code, cs373, python]
---

the first project for [my software engineering class at UT][cs373] was to
submit solutions for the [collatz conjecture][conjecture] to [a system called
sphere][sphere] which judges the output and ranks everyone's results. the
project was focused more on good engineering practices like testing and
documentation than the problem itself. i [managed to get second place][vanity]
on the [all-time best list for python 2.7][scoreboard], and the individual
coming in first happens to be [a current classmate][chiang].

the professor was kind enough to give us a skeleton of the project code, but he
also asked us to use the exact set of functions he laid out. i thought this was
unfortunate because [the code he posted][profcode] is not very good.

<p class="disclaimer">
<strong><em>disclaimer</em></strong>: apologies for the flame-bait title. it's
admittedly a cheap trick employed by poor writers to make an otherwise boring
piece more interesting, and there's nothing different here. the professor is
more intelligent than i am, and the course is among the best i've taken at UT.
i'm guessing he authored the code in this manner out of pedagogical motivations
since the average student is relatively new to programming most experienced
with java.
</p>

let's consider the function used to read the input integer pairs:

    def collatz_read (r, a) :
        """
        reads two ints into a[0] and a[1]
        r is a  reader
        a is an array of int
        return true if that succeeds, false otherwise
        """
        s = r.readline()
        if s == "" :
            return False
        l = s.split()
        a[0] = int(l[0])
        a[1] = int(l[1])
        assert a[0] > 0
        assert a[1] > 0
        return True

i believe this function fails in two main areas: the interface, and the coding
style.

## the interface

the function uses the return value to indicate whether there was output and the
`a` parameter to store the output. there is no way of determining what is input
or output by simply looking at the function signature, and i find it much more
clear to follow the convention that **function arguments are inputs and return
values are outputs**. the professor's approach is acceptable in a less
expressive language like C or a language like C++ which allows `const`
arguments to indicate inputs. but python is wonderfully expressive and it
doesn't have `const`.

i believe the right tool for this job is a [generator][]. generators (and
[python's iteration protocol][iter]) are powerfully composable concepts, and
some of the best parts of the language. generators are important to python the
way pipes are important to unix -- beyond their role as abstractions, they also
inform the design and philosophy of the systems by encouraging small, reusable
building blocks that form the foundation for larger systems.  david beazely has
[an awesome peice on building systems with generators][gen_tricks]. you should
stop reading this and go read that now. you should also appreciate how
generators make it possible for peter norvig to write [a spelling corrector in
a mere 21 lines][spell].

so if we re-write `collatz_read` with generators, parameters only for inputs,
and the return value only for outputs, i think it would look more like:

    def collatz_read(infile):
        """
        generate input pairs for the collatz problem from a readable file-like
        object that's formatted as specified here:
        http://www.spoj.com/problems/PROBTNPO/

        infile: readable file-like object
        returns: generator of arrays of int pairs
        """
        return filter(lambda i: len(i) == 2, (map(int, l.split()) for l in infile))

let's break that down:

 - `for l in infile`: iterate through the lines of the `infile` [file-like
   object][file]
 - `map(int, l.split())`: split the line on whitespace, and convert strings to
   numbers by applying the `int` function to each item
 - `lambda i: len(i) == 2`: this is a function that returns true if its input
   has length of 2
 - `filter(<length is 2>, <input as int arrays>)`: this filters out everything
   that is not a pair of `int`'s, so blank or improperly formatted lines are not
   returned

this version is better because:

 - it runs faster by implementing a number of loop optimizations (see [this
   optimization anecdote][anecdote])
 - data flows in through the parameters and out through the return value,
   removing the ambiguity around which arguments are input vs. output
 - it returns a nicely composable generator instead of an ad-hoc mechanism to
   signal the end of input

## coding style

you might have noticed the professor's implementation has spaces before colons
and after the function parameters list. additionally the file names (along with
the other file names in the project) are capitalized. this is non-standard
style, and it doesn't conform to [PEP-8][pep8], [the google python
styleguide][googlepystyle], [the python standard libraries][stdlib], or major
community projects like [django][].

before you write me off as a whiny pedant, understand my motivations. this is
not about nit-picking or my own pet preferences, **this is about attention to
detail and respecting the decisions of the community**.

developers managing open source projects are very busy people. the first thing
they'll notice in any patch you submit is whether it conforms to the style of
the rest of the project. sure, the patch may be correct, but if it looks
different it communicates that you can't be bothered to understand the
community's preferences, so they'll probably have much less tolerance for your
proposed changes.

this all may still seem like hair-splitting, but remember: it's about the
community. the community behind a technology is often more influential in
determining its success than the language's features and performance. one of
your first steps in adopting any technology should be getting to know its
community, which affects everything from how much you can improve things to
what type of people will be attracted to your team.

## recap

 - if you're going to use python, use generators
 - speak the native accent of the technology you're using

[cs373]: https://www.cs.utexas.edu/users/downing/cs373/drupal/
[conjecture]: http://en.wikipedia.org/wiki/Collatz_conjecture
[sphere]: http://www.spoj.com/problems/PROBTNPO/
[vanity]: /assets/images/vanity.png
[scoreboard]: http://www.spoj.com/ranks/PROBTNPO/lang=PYTH%202.7
[chiang]: http://csw373.wordpress.com
[profcode]: https://github.com/gpdowning/cs373/blob/868e4b2fca1f1540547fab8d353cf12e5e2abdec/projects/collatz/Collatz.py
[Church]: http://en.wikipedia.org/wiki/Alonzo_Church
[generator]: http://wiki.python.org/moin/Generators
[iter]: http://docs.python.org/2/tutorial/classes.html#iterators
[gen_tricks]: http://www.dabeaz.com/generators/
[file]: http://docs.python.org/2/library/stdtypes.html#file-objects
[anecdote]: http://www.python.org/doc/essays/list2str.html
[pep8]: http://www.python.org/dev/peps/pep-0008/
[googlepystyle]: http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
[stdlib]: http://svn.python.org/view/python/trunk/Lib/
[django]: https://github.com/django/django
[spell]: http://norvig.com/spell-correct.html
