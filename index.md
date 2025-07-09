---
layout: page
title: Aaron
tagline: snacks and naps
---

<img class="me" src="/assets/images/aaron.jpg" />

Hi! I'm Aaron. This is my website where I collect little digital side projects.

On the personal side, my family and I live in Austin, and [my faith](http://biblia.com/books/esv/Jn13.35) is very important to me. While Texas is home now, I've got roots in Indiana.

I am a software engineer and former Marine. [My LinkedIn profile](https://www.linkedin.com/in/aaronrstacy) has my professional info.

# Code

I like working on the largest scale mobile systems possible, and so far that's been mostly closed source, but [I write code in my free time too][the_hubs]. Some projects include:

 - [Everywhere Bible][]: [2 of the world's 3 billion internet users can't use today's Bible apps][everywherebible_splash]. That's unfortunate because many of those are more likely to have a smart phone than running water. [This app][everywherebible_app] is a proof-of-concept that we can do a better job of getting the Bible out there.
- [Refugee Services of Texas checklist app][rst_checklist]: A hackathon project where my team worked with local non-profits to help Austin area asylum seekers through the relocation process.
- [the geometry of innocent signals on the wire][geom]: An old project for school evaluating attack vectors on a [Square][] credit card reader.

# Talks

 - [The web and Android][webnandroid] ([slides][webnandroid-slides]): After
   spending ~4 years each on both large scale web and Android apps, I gave this
   talk about what each does well, and what they could learn from eachother.
 - [Don't just build, ship][shipit] ([slides][shipit-slides]): I gave a talk at
   [jQuery Conference Austin][jqconf] about tools that help us ship our
   projects.
 - [Git: complex, but worth it][git-talk] ([slides][git-talk-slides]): I talked
   to a few of [Professor Glen Downing's][gpd] classes about git, version
   control, and software development workflows.

# Writings

Against my better judgement, I infrequently write about code and computers:

<ul class="posts none">
  {% for post in site.posts %}
    <li><span class="date">{{ post.date | date: "%d %B, %Y" }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

<div class="here-be-pyrates">☠</div>


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
[webnandroid]: https://github.com/aaronj1335/the-web-and-android
[webnandroid-slides]: http://aaronstacy.com/the-web-and-android/
