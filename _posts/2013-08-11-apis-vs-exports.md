---
layout: post
title: "CS373: api's vs exports"
author: Aaron Stacy
category: cs373
tags: [apis, cs373]
---

# api's vs exports

{% include byline %}

in my software engineering course we had to make a website of information about
world crises. a large portion of the project was exporting the data to xml and
sharing it between groups.

this was a well-designed project because it encouraged us to learn several
common skills in software engineering:

 - exporting and importing data
 - industry standard technologies like xml, sql, and python
 - cooperating and communicating on a standard format (the most valuable skill,
   imo)

this is all well and good.

we had a guest speaker mention "restful api's" this week, and i was caught
off-guard when someone asked what that was. i didn't learn about rest in
undergrad either, but i forgot because i use it so frequently now.

in fact during my career i've had to deal with data exports a number of times
(10? 20?), but i write code that uses api's (specifically rest api's) *every
day*. when i'm not writing code against these api's, i'm writing spec and
requirement documentation that depend on them. i've even spent a lot of time
writing [code to mock rest-ful api's][mock] so that i can [write proper unit
tests][test].

i think my experience of using api's more than exports may be indicitave of the
industry as a whole. new products are more likely to offer an api or
integration with an external api (twitter, facebook, google maps, etc.) than
data export/import. it's almost too broad to compare, but i believe that with
the ubiquity of today's internet, apps tend to use an external api's more often
than just importing/exporting their data.

so i suggest that instead of an xml import/export, future assignements center
around providing a restful json api to the data. like the existing assignment
it encourages students to learn several common skills:

 - interacting with restful api's (more common that data export/import, i would
   argue)
 - industry standard technologies like json, sql, and python (or maybe
   javascript&hellip;)
 - cooperating and communicating on a standard api format (still the most
   valuable, imo, because it requires heavy a lot of interaction)

i think this approach has all of the benefits of the import/export assignment,
but it is more relevant to the tasks students will encounter in the industry.

[mock]: https://github.com/aaronj1335/mesh/blob/2acc63de985c1cd1af41e28a06d33b3b1be73922/js/tests/mockutils.js
[test]: https://github.com/aaronj1335/mesh/blob/2acc63de985c1cd1af41e28a06d33b3b1be73922/js/tests/test_model.js
