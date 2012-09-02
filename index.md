---
layout: page
title: aaron stacy dot com
tagline: not in the face
---
{% include JB/setup %}

<img class=me src="/assets/images/aaron.jpg" />

i am a 27 year old software developer living in [austin, texas][where], and I
am currently employed by [storediq][employer]. i am happily married to a
beautiful girl named ashly, and i’m a follower of Jesus Christ ([read
more][bible]).

in may of 2009 i graduated from [purdue university’s computer engineering
program][puece], and now i'm working on a [mater's in computer science at
university of texas][utcs]. i also spent several years in the marine corps,
during which i had the opportunity to serve overseas with [an exemplary reserve
unit][det1comm].

if you'd like to get a hold of me, [twitter is good place to start][twitter].

# code

if you're interested in my work, feel free to [browse some of my
code][the_hubs] or [the code i've written for storediq][siq_hubs].  there's a
lot there, so i'd reccomend starting with one of these:

 - [`csi`][csi]: client-side package management with [`npm`][npm]
 - [t.js][tjs]: a javascript tree traversal library
 - [the geometry of innocent signals on the wire][geom]: a school project where
   i hacked a [square][] credit card reader

# writings

against my better judgement, i sometimes write about code and computers:

<ul class="posts">
  {% for post in site.posts %}
    <li><span class=date>{{ post.date | date: "%d %B, %Y" }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

<div class=here-be-pyrates>☠</div>

[where]: https://maps.google.com/?ll=30.317321,-97.748709&spn=0.076612,0.055189&t=m&z=14
[employer]: http://storediq.com/
[bible]: http://biblia.com/books/esv/Jn13.35
[puece]: https://engineering.purdue.edu/ECE/
[utcs]: http://www.cs.utexas.edu/
[det1comm]: http://www.facebook.com/pages/Detachment-1-Communications-Company/302302460425
[twitter]: http://twitter.com/aaronj1335
[the_hubs]: https://github.com/aaronj1335
[csi]: http://siq.github.com/csi/
[siq_hubs]: http://github.com/siq/
[npm]: https://npmjs.org/
[tjs]: http://aaronj1335.github.com/t-js/
[geom]: https://github.com/aaronj1335/the-geometry-of-innocent-signals-on-the-wire
[square]: https://squareup.com/
