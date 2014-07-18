---
layout: post
title: if underscore was written in es6 javascript
author: Aaron Stacy
published: false
---

<aside>
  i was originally going to give this as a lightning talk at [austinjs][], but
  i ran out of time because we had so many good talks. so i'll post it here
  instead.
</aside>

> what if [underscore][] (or [lodash][] for that matter) was written in [es6][]?

certainly there would be a number of changes to the code. features like
[destructuring assignments][] and [the spread operator][] would enhance
readability. but would the interface be different? i think so.

now to be clear i think underscore is not just a good library, it's an inspired
library. the point of this article is how new features in es6 solve problems
that we've got today, not to imply there's some problem with "javascript's
utility belt".

## issue #1: intermediate arrays

here's a pretty common snippet of code. it finds the max age of a list of user
objects:

    var activeUsers = _.filter(users,    function(user) { return user.isActive });
    var ages        = _.map(activeUsers, function(user) { return user.age });
    var maxAge      = _.reduce(ages, max, 0);

this is good code. it separates business concerns (like getting a user's age
and determining whether they're active) from the mechanism of iterating over
the arrays (this is [a thing][sepofpolicyandmechanism]). and it's actually
common to have pipelines of underscore functions like this. so common in fact,
underscore and lodash provide [a chaining functionality][chain] to reduce some
boilerplate.

the problem is that a lot of the steps you would have in these chains like
`map`, `filter`, `flatten`, etc. produce intermediate arrays. that's wasted
memory that may not be a problem in typical browser applications, but when
we're talking about the scale of map-reduce workloads that [made a certain
search engine successful][mapreduce], these inefficiencies start to add up. so
it would be nice if javascript provided a way to write the above code so it's
both maintainable and efficient.

## solution to issue #1: generators

let's rewrite the `map` and `filter` functions as generator functions. you can
think of generators as functions that return lazily-computed collections. so
when you call a generator function, it returns an object that will provide each
element of the collection. here's map and filter:

    function* map(items, transform) {
      for (item of items)
        yield transform(item);
    }

    function* filter(items, predicate) {
      for (item of items)
        if (predicate(item))
          yield item;
    }

there are no `return`'s because we already know generator functions return
lazily-computed collections. the items of the collection are determined by
those `yield` statements.

the discerning reader will also notice that `of` keyword. if you're not
familiar with es6 `of` then for now just know that it does exactly what you
would expect. more on that later.

`reduce` returns a single item, so it's not a generator function. with these
new functions our code looks nearly identical, but it doesn't create
intermediate arrays:

    var activeUsers = filter(users,    function(user) { return user.isActive });
    var ages        = map(activeUsers, function(user) { return user.age });
    var maxAge      = reduce(ages, max, 0);

es6 allows us to write maintainable code without sacrificing performance.

## issue #2: new data types

the underscore documentation page is familiar to a lot of javascript
developers. notice that section of functions that includes `map` and `set`:

![underscore documentation page][underscoredocs]

it's titled "Collections". what's a "Collection"? is it an `Array`? is it any
`Object`? does it include new es6 data structures like [`Set`][set] and
[`Map`][map]? can i use these functions with data structures i define, like
maybe a tree or graph?

well of course we could, we would just convert any of the above into an array,
and pass that in as the first argument, but now we're back to our first issue
of unnecessary intermediate arrays.

## solution to issue #2: iterators

iterators are little more than an interface, or a formalized convention. i was
surprised by how readable [the iterators spec][iterspec] is. it's basically got
three parts.

- `Iterable`'s: anything with a specifically-named function that creates an iterator
- `Iterator`'s: objects with a `next` method that produce items
- `IterableResult`'s: objects with a value and a "done" flag

so let's make an iterable. if you're not familiar with the idea of [symbols][],
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

    iterator.next()  // -> {value: 'item 1', done: false}
    iterator.next()  // -> {value: 'item 2', done: false}
    iterator.next()  // -> {value: 'item 3', done: false}
    iterator.next()  // -> {value: undefined, done: true}

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
