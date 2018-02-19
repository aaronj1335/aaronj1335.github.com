---
layout: page
title: aaron
tagline: not in the face
---

<img class=me src="/assets/images/aaron.jpg" />

i am a <span id=my-age>33</span> year old software engineer living in [austin,
texas][where], and even though i currently work on android stuff at google,
my heart's still with the open web.

i've got a couple kids, a wife that's way out of my league, and i’m [a Jesus
follower][bible].

texas is home now, but i'm originally from indiana. i graduated from [purdue
university’s computer engineering program][puece] in 2009, and then got a
master's degree in computer science from [university of texas][utcs]. i also
spent several years in the marine corps, during which i had the opportunity to
serve overseas with [an exemplary reserve unit][det1comm].

if you'd like to get a hold of me, [twitter is good place to start][twitter].

# code

if you're interested in my work, feel free to [browse some of my
code][the_hubs].  i'd recommend starting with one of these:

 - [`csi`][csi]: client-side package management with [`npm`][npm]
 - [t.js][tjs]: a javascript tree traversal library
 - [the geometry of innocent signals on the wire][geom]: a school project where
   i hacked a [square][] credit card reader

# talks

 - [don't just build, ship][shipit] ([slides][shipit-slides]): i gave a talk at
   [jquery conference austin][jqconf] about tools that help us ship our
   projects
 - [git: complex, but worth it][git-talk] ([slides][git-talk-slides]): i talked
   to a few of [professor glen downing's][gpd] classes about git, version
   control, and software development workflows

# writings

against my better judgement, i sometimes write about code and computers:

<ul class="posts none">
  {% for post in site.posts %}
    <li><span class=date>{{ post.date | date: "%d %B, %Y" }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

<div class=here-be-pyrates>☠</div>


[where]: https://maps.google.com/?ll=30.317321,-97.748709&spn=0.076612,0.055189&t=m&z=14
[employer]: http://www.amazon.com
[bible]: http://biblia.com/books/esv/Jn13.35
[puece]: https://engineering.purdue.edu/ECE/
[utcs]: http://www.cs.utexas.edu/
[det1comm]: http://www.facebook.com/pages/Detachment-1-Communications-Company/302302460425
[twitter]: http://twitter.com/aaronj1335
[the_hubs]: https://github.com/aaronj1335
[csi]: https://github.com/aaronj1335/csi
[npm]: https://npmjs.org/
[tjs]: http://aaronj1335.github.com/t-js/
[geom]: https://github.com/aaronj1335/the-geometry-of-innocent-signals-on-the-wire
[square]: https://squareup.com/
[jqconf]: http://events.jquery.org/2013/austin/
[gpd]: https://www.cs.utexas.edu/users/downing/
[shipit]: https://github.com/aaronj1335/shipit
[shipit-slides]: http://aaronstacy.com/shipit/
[git-talk]: https://github.com/aaronj1335/git-complex-but-worth-it
[git-talk-slides]: http://aaronstacy.com/git-complex-but-worth-it/
[this guy]: http://aaronstacy.com/anderson-davids-growth-chart/
