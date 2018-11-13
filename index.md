---
layout: page
title: Aaron
tagline: not in the face
---

<img class="me" src="/assets/images/aaron.jpg" />

I am a <span id="my-age">33</span> year old software engineer living in [Austin,
Texas][where], and even though I currently work on Android stuff at Google,
my heart's still with the open web.

I've got a few kids, a wife that's way out of my league, and I’m [a Jesus
follower][bible].

Texas is home now, but I'm originally from Indiana. I graduated from [Purdue
University’s computer engineering program][puece] in 2009, and then got a
master's degree in computer science from the [University of Texas][utcs]. I also
spent several years in the Marine Corps, during which i had the opportunity to
serve overseas with [an exemplary reserve unit][det1comm].

If you'd like to get a hold of me, [Twitter is good place to start][twitter].

# Code

I like working on big mobile apps, and so far that's all been closed source, but [I write code in my free time too][the_hubs]. Some projects include:

 - [Everywhere Bible][]: [2 of the world's 3 billion internet users can't use today's Bible apps][everywherebible_splash]. That's unfortunate because many of those are more likely to have a smart phone than running water. [This app][everywherebible_app] is a proof-of-concept that we can do a better job of getting the Bible out there.
- [Refugee Services of Texas checklist app][rst_checklist]: A hackathon project where my team worked with local non-profits to help Austin area asylum seekers through the relocation process.
- [the geometry of innocent signals on the wire][geom]: An old project for school evaluating attack vectors on a [Square][] credit card reader.

# Talks

 - [Don't just build, ship][shipit] ([slides][shipit-slides]): I gave a talk at
   [jQuery Conference Austin][jqconf] about tools that help us ship our
   projects.
 - [Git: complex, but worth it][git-talk] ([slides][git-talk-slides]): I talked
   to a few of [Professor Glen Downing's][gpd] classes about git, version
   control, and software development workflows.

# Writings

Against my better judgement, I used to write about code and computers:

<ul class="posts none">
  {% for post in site.posts %}
    <li><span class="date">{{ post.date | date: "%d %B, %Y" }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

<div class="here-be-pyrates">☠</div>


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
[Everywhere Bible]: https://github.com/everywherebible/app
[everywherebible_splash]: https://everywherebible.org
[everywherebible_app]: https://en.everywherebible.org
[rst_checklist]: https://github.com/g11x/checklistapp
