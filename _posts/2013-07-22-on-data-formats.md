---
layout: post
title: "CS373: on data formats"
author: Aaron Stacy
category: cs373
tags: [dataformats, cs373]
---

# on data formats

{% include byline %}

a significant portion of the first big group project in my software engineering
course was deciding on a data format and schema. we were required to use
[xml][], and though we weren't required to agree on a schema, we will have to
import eachother's data later in the course, so we made our future lives much
easier by developing and adhering to a shared schema.

by the grace of everything holy this was my first (and hopefully last)
experience with xml. i thought it might be interesting to compare it to formats
with which i'm more familiar, [json][] and [yaml][].

## json

json is designed to be lightweight and easily parsed. it assumes several
implicit types including:

 - strings
 - numbers (though it doesn’t define machine representation)
 - lists
 - maps (or dictionaries, or associative arrays, or records, or whatever you’d
   like to call them -- the keys must be stings)

json is actually a strict subset of javascript (from which its name comes), and
almost a strict subset of python. json does not define any mechanism for
referencing other parts of the document; it doesn't allow multi-line strings,
and it is relatively inflexible about syntax. for instance it does not allow
single-quoted strings or trailing commas on the final item in a collection.

while this may seem limiting, it turns out to strike a good balance between
simplicity and power, and it is gaining (has gained) popularity in arenas
including [configuration][], [archiving][], and most prevalantly [api's][].

## yaml

yaml aims to be human readable above all. it is pleasant to write and read, and
it includes implicit types like json (though it has many more).

unfortunately all of this convenience and syntactic flexibility isn't free.
yaml is very difficult to parse -- compare the lines of code in the [pyyaml][]
versus [simplejson][] python libraries. this also makes it difficult to
[standardize implementations][tricky] and [eradicate security issues][pwned].

while its complexity makes it undesirable for something like an api (where you
cannot tolerate ambiguity), its sweet spot is configuration files and things
like internationalization string bundles where you just want something
readable.

## xml

xml [is][xml1] [extensively][xml2] [standardized][xml], available in nearly
every language (often several times over), and very well understood by the
industry. it is the most expressive of the formats presented here, which
explains its applications to not only the aforementioned tasks, but also more
intricate problems such as user interface definition (see [.xaml][], [.xib][],
[glade][], and arguably web apps written in xhtml).

xml is also the most verbose of the formats. if json is a gentleman’s
handshake, then xml is a 100-page legal document. while json and yaml have
implicit types, xml leaves that function up to the application, which is less
convenient, but more extensible.

## preferences

if i could have chosen a data interchange format for this assignment, i would
have used json because it is the most convenient and expressive enough for our
needs. beyond that, in my experience it seems like a more common choice for new
projects without any legacy restrictions. that is of course biased by the fact
that i write javascript for a living, and json is the data lingua franca of my
programming community. i am curious why the professor chose xml though.

[json]: http://www.json.org
[yaml]: http://www.yaml.org
[xml]: http://www.w3.org/TR/REC-xml/
[configuration]: https://npmjs.org/doc/json.html
[archiving]: http://docs.mongodb.org/manual/core/import-export/
[api's]: http://www.programmableweb.com/apis/directory/1?format=JSON
[pyyaml]: http://pyyaml.org/browser
[simplejson]: https://github.com/simplejson/simplejson
[tricky]: http://en.wikipedia.org/wiki/YAML%23Pitfalls_and_implementation_defects
[pwned]: http://tenderlovemaking.com/2013/02/06/yaml-f7u12.html
[xml1]: http://www.ietf.org/rfc/rfc4646.txt
[xml2]: http://www.ietf.org/rfc/rfc4647.txt
[.xaml]: http://msdn.microsoft.com/en-us/library/cc295302.aspx
[.xib]: http://en.wikipedia.org/wiki/Interface_Builder
[glade]: https://glade.gnome.org
