---
layout: post
title: if underscore was written in es6 javascript
author: Aaron Stacy
---

<aside>
  i was originally going to present this at [austinjs][], but i ran out of time
  because we had so many good lightning talks. so i'll post it here instead.
</aside>

***UPDATE:*** parts of this became out-of-date with the introduction of [lodash's
lazy evluation][lazydash].

> what if [underscore][] (or [lodash][] for that matter) was written in [es6][]?

features like [destructuring assignments][] and [the spread operator][] would
certainly make the code more readable. but would the interface be different? i
think so. i'll demonstrate why by discussing a couple issues with underscore's
current implementation.

now i'm not trying to hate on underscore. it's a great library &mdash; an
inspired library. but this article is about how new features in es6 solve
problems we've got today, and underscore provides a context with which a lot of
us are familiar.

## issue #1: intermediate arrays

here's a pretty common snippet of code. it finds the max age of a list of user
objects:

    var activeUsers = _.filter(users,    function(user) { return user.isActive });
    var ages        = _.map(activeUsers, function(user) { return user.age });
    var maxAge      = _.reduce(ages, max, 0);

this is good code. it separates business concerns (like getting a user's age
and determining whether they're active) from the mechanism of iterating over
the arrays (this is [a thing][sepofpolicyandmechanism]). depending on the
amount of data-munging you've got to do, these pipelines of functions can grow
deeper, and it's actually so common that underscore and lodash provide [a
chaining functionality][chain] to reduce boilerplate.

the problem is that a lot of the steps you would have in these chains like
`map`, `filter`, `flatten`, etc. produce intermediate arrays. that's wasted
memory that may not be a problem in typical browser applications, but when
we're talking about the scale of map-reduce workloads that [made a certain
search engine successful][mapreduce], these inefficiencies add up. so it would
be nice if javascript provided a way to write the above code so it's both
maintainable and efficient.

## solution to issue #1: generators

let's rewrite the `map` and `filter` functions as generator functions. you can
think of generators as functions that return lazily-computed collections. so
when you call a generator function, it returns an object that will provide each
element of the collection.

here's map and filter:

    function* map(items, transform) {
      for (item of items)
        yield transform(item);
    }

    function* filter(items, predicate) {
      for (item of items)
        if (predicate(item))
          yield item;
    }

there are no `return`'s since, as we know, generator functions return
lazily-computed collections. the items of the collection are determined by
those `yield` statements.

if you're not familiar with the es6 `of` keyword, then don't worry. it does
exactly what you would expect in this code.

`reduce` returns a single item, so it's not a generator function. with these
new functions our code looks nearly identical, but it doesn't create
intermediate arrays:

    var activeUsers = filter(users,    function(user) { return user.isActive });
    var ages        = map(activeUsers, function(user) { return user.age });
    var maxAge      = reduce(ages, max, 0);

es6 allows us to write maintainable code without sacrificing performance.

## issue #2: new data types

the underscore documentation page is familiar to a lot of javascript
developers. notice that section of functions that includes `map` and `filter`:

<img src="/assets/images/underscore-dot-org.png" style="width: 100%;" />

it's titled "Collections". what's a "Collection"? is it an `Array`? is it any
`Object`? does it include new es6 data structures like [`Set`][set] and
[`Map`][map]? can i use these functions with data structures i define, like a
tree or graph?

of course we could convert any of the above into an array and pass that in as
the first argument, but now we're back to our first issue of unnecessary
intermediate arrays.

## solution to issue #2: iterators

iterators are simply an interface, or a formalized convention. i was surprised
by how readable [the iterators spec][iterspec] is. it's basically got three
parts.

- `Iterable`: an object with a specifically-named function that creates an
  `Iterator`
- `Iterator`: an object with a `next` method that produces items
- `IterableResult`: an object with a value and a "done" flag

so let's make an iterator. if you're not familiar with the idea of [symbols][],
then just pretend that `Symbol.iterator` is a regular variable referencing some
specific string.

    var iterable = {};
    iterable[Symbol.iterator] = function() {
      var count = 0;
      return {
        next: function() {
          return ++count <= 3?
            {value: 'item ' + count,  done: false},
            {value: undefined,        done: true};
        }
      }
    };
    var iterator = iterable[Symbol.iterator]();

    iterator.next(); // -> {value: 'item 1',  done: false}
    iterator.next(); // -> {value: 'item 2',  done: false}
    iterator.next(); // -> {value: 'item 3',  done: false}
    iterator.next(); // -> {value: undefined, done: true}

the code isn't very interesting, but interesting things happen when everyone
agrees on this interface. if underscore supported es6 iterators, we could use
all of those familiar functions on anything we make &mdash; graphs, database
cursors, infinite sequences, etc.

## one more thing&hellip;

javascript developers often use libraries like underscore to supplant the
language's syntax. we prefer functions like `_.each` because the `for` loop
isn't flexible enough. es6 gives us a way to work with the language syntax
though.

wouldn't it be nice if we could loop over a jquery collection using a plain old
`for` loop, without worrying about an index variable? with es6 it's pretty
easy. first we make the jquery object an iterable. generators are a really
succinct way to write functions that return iterators:


    jQuery.prototype[Symbol.iterator] = function* iterator() {
      for (var i = 0; i < this.length; i++)
        yield $(this.get(i));
    }

now remember that `of` keyword? `of` knows how to iterate over any iterable, so
now we can use simple `for` loops on jquery objects:

    for (var p of $('p'))
      p.fadeOut();

(h/t to [dave herman for this example][littlecalculist]).

and what if we want to have the index of each item (like the second parameter
of the `_.each` callback)? we can borrow from python's
[`enumerate`][enumerate]:

    function* enumerate(iterator) {
      var i = 0;

      for (var item of iterator)
        yield [i++, item];
    }

    for (var [i, p] of enumerate($('p')))
      console.log('paragraph number ' + (i + 1) + ': ', p);

combining generators and iterators makes the features more compelling than they
are alone.

[austinjs]: http://austinjavascript.com/july-15th-meetup-730-pm-lightning-talks/
[es6]: http://wiki.ecmascript.org/doku.php?id=harmony:specification_drafts
[underscore]: http://underscorejs.org
[lodash]: http://lodash.com
[destructuring assignments]: http://people.mozilla.org/~jorendorff/es6-draft.html#sec-destructuring-assignment
[the spread operator]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_operator
[chain]: http://underscorejs.org/#chaining
[sepofpolicyandmechanism]: http://en.wikipedia.org/wiki/Separation_of_mechanism_and_policy
[mapreduce]: http://research.google.com/archive/mapreduce.html
[set]: http://www.nczonline.net/blog/2012/09/25/ecmascript-6-collections-part-1-sets/
[map]: http://www.nczonline.net/blog/2012/10/09/ecmascript-6-collections-part-2-maps/
[iterspec]: https://people.mozilla.org/~jorendorff/es6-draft.html#sec-common-iteration-interfaces
[symbols]: https://people.mozilla.org/~jorendorff/es6-draft.html#sec-ecmascript-language-types-symbol-type
[underscoredocs]: /assets/images/underscore-dot-org.png
[enumerate]: https://docs.python.org/2/library/functions.html#enumerate
[littlecalculist]: http://tc39wiki.calculist.org/es6/iterators/
[lazydash]: https://github.com/lodash/lodash/issues/274#issuecomment-57593441
