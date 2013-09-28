---
layout: post
title: why can't i just require('bootstrap')?
author: Aaron Stacy
description: "comprehensive dependency management in client-side applications"
category: code
tags: [code, javascript]
---

if you're a client-side developer and you've had the chance to spend any time doing [`node.js`][nodejs] development, it's easy to appreciate the module system. suddenly you don't have to care that package A depends on B depends on C, etc. you just `require()` the code you need, and everything is cool.

if you're going the other way, from environments like node, ruby, python, etc. to the client-side, you're probably be even *more* aware of the pain of manually dependency management since you got used to life with it built in to the runtime.

either way, a lot of folks are using tools like [amd][] (i.e. [`require.js`][requirejs]), [`browserify`][browserify], and the [rails asset pipeline][assetpipeline] to provide code modules in client-side development. these abstractions are key building blocks in large applications, and the ecmascript spec authors agree -- in time [modules will hopefully be a part of the language][ecmascriptmodules].

## javascript modules are not sufficient

but i don't build javascript applications, i build **web** applications composed not only of javascript, but html and css too. html and css are code dependencies just like javascript.

suppose you need to pop up a modal dialog in your application. instead of re-inventing the wheel you decide to use [the one from twitter's bootstrap][bsmodal]. you don't want to mess with the details of getting it on the page, so you utilize [the `jam` package manager][jam]. you run the command:

    # command-line installation of both jquery and bootstrap 
    $ jam install jquery bootstrap

and you bang out some code:

    require([
        'jquery',
        'bootstrap/js/bootstrap-modal'
    ], function($) {
        $('#myModal').modal();
    });

but it looks all wrong. the javascript is there but the styling is missing.  all you need to do is add the stylesheet:

    <link rel=stylesheet href="/jam/bootstrap/css/bootstrap.css" />

maybe this seems natural to you, but would you ever want to use the bootstrap modal *without* the corresponding css? no, if your application depends on the bootstrap modal, it depends on the bootstrap css as well. maybe you should be asking:

> why can't i just `require('bootstrap')`?

it turns out you wouldn't be the only one raising the question, and the community is at least *starting* to address it:

 - [tj holowaychuk's post on web components][tj] and his corresponding [`component(1)`][components] tool

 - [twitter's `bower`][bower] package manager, which treats html and css as first-class dependencies (even though it doesn't provide the module-loading capabilities)

 - the [montagejs][] module system [mr][] and corresponding [template loader][montagetmpl] (which loads css dependencies as well)

 - i'll also mention my company's humble offering [csi][], which, in spite of the self-promotion, hopefully lends me some street cred on this subject &#9786;

these systems are complicated, and probably deserve a separate post just to compare them, but for now we'll take them as evidence that **javascript modules are not sufficient**, we need more.

## what's stopping us?

well, nothing we can't overcome &#9786; there are significant hurdles though.

fair warning: the next few sections get a bit technical.

### hurdle #1: getting css on the page

the dom api has no explicit call for programmatically injecting css. fortunately it is a fairly well-understood problem and solutions exist, but i mention it because they tend to be hacky for older browsers (lookup the [`<link>` element's `onload` event support][linkonload] and [IE's external stylesheet limit][ie_limit]). also many client-side module loading systems don't officially support specifying css as a dependency, [notably `require.js`][requirejs].

but, like i said, this is one that module runtimes can work around, and since production code will be concatenated and minified, it's only an issue in development.

### hurdle #2: ordering css

there's a reason they're called 'cascading' stylesheets… order matters. typically you want to design UI widgets with base styles that are just enough to make them functional (what [smacss][] might call ['module styles'][smacssmodule]), then add layers of look-and-feel, branding, etc.

this creates an ordering problem. it may seem easy to solve, just order your `require` calls with the dominant styles last (assuming commonjs modules here):

    var myWidget = require('my-widget');
    var bootstrap = require('bootstrap.css');

but subtle bugs ensue. depending on the implementation, caching, network latency, and the shape of the dependency tree, you can easily run into the scenario where the above calls load the bootstrap css immediately, but the base styes for `myWidget` are asynchronously loaded afterwards. trust me, if you're developing real-world applications in this style, you'll run into it.

the simple solution here is providing a means of imposing a global ordering -- think of something like a [`z-index`][zindex] for stylesheets:

    // load bootstrap.css with a priority of 100, which would be higher than
    // the default of 0
    var bootstrap = require('100:bootstrap.css');

it's ugly, but [it's working (and necessary) for us][cssorder].

a more elegant solution may involve ordering the css via [a depth-first traversal][dfs] of the dependency tree. this would address the above issue, but it's tricky to get right, especially without loading all the dependencies up front, and i'm not sure if it is a universal fix.

### hurlde #3: paths in css

css url's are relative to the stylesheet, so a css file loaded from `http://example.com/widgets/dropdown.css` with the rule:

    .down-arrow {
        background-image: url("down-arrow.png");
    }

would make a request for `http://example.com/widgets/down-arrow.png`. nothing new here.

as you develop a massive, modular application, you quickly get to the point where you need to concatenate and minify assets, including css.

now we have a problem, because our gigantic concatenated file living at `http://example.com/stylesheets/style.css` includes a path relative to the `widgets` directory, which will serve up a big fat 404.

once again, this is a fixable problem. your build tool could easily re-write paths relative to the concatenated file using something like [cssom][]. at my company we started with this approach, but ended up moving away from it because (at the time) cssom didn't play well with [dx filters][dxfilters]. [we fixed it][cssrewrite] by using a regexp \*gasp\*, which admittedly is a tradeoff between accuracy and performance.

## the real hurdle: community consensus

the biggest argument against specifying html and css dependencies in javascript is the fact that the community hasn't converged on a single solution. the web-development community is huge, and it takes a long time to get everyone on the same page. that means that right now any given solution will suffer from some combination of lack of features/functionality, documentation, support, or just plain google-ability.

but the web moves fast, and the future is bright. like i said, it's nothing we can't overcome, so i hope we rise to the challenge and come up with a solution.

and above all, have fun while we're at it &#9786;

[amd]: https://github.com/amdjs/amdjs-api/wiki/AMD
[requirejs]: http://requirejs.org
[browserify]: https://github.com/substack/node-browserify
[nodejs]: http://nodejs.org
[assetpipeline]: http://guides.rubyonrails.org/asset_pipeline.html
[ecmascriptmodules]: http://wiki.ecmascript.org/doku.php?id=harmony:modules
[tj]: http://tjholowaychuk.com/post/27984551477/components
[components]: https://github.com/component/component
[bower]: http://twitter.github.com/bower/
[bsmodal]: http://twitter.github.com/bootstrap/javascript.html#modals
[jam]: http://jamjs.org
[montagejs]: http://tetsubo.org/home/montage/
[montagetmpl]: https://github.com/montagejs/montage/blob/master/ui/template.js#L741
[mr]: https://github.com/kriskowal/mr
[csi]: https://github.com/aaronj1335/csi
[ie_limit]: http://support.microsoft.com/kb/262161
[linkonload]: http://stackoverflow.com/questions/3078584/link-element-onload
[requirejscss]: http://requirejs.org/docs/faq-advanced.html#css
[smacss]: http://smacss.com
[zindex]: https://developer.mozilla.org/en-US/docs/CSS/z-index
[cssorder]: https://github.com/siq/csi/blob/master/lib/css_requirejs_plugin.js#L105
[dfs]: http://en.wikipedia.org/wiki/Depth-first_search
[cssrewrite]: https://github.com/siq/csi/blob/master/lib/css_rewrite.js
[dxfilters]: http://msdn.microsoft.com/en-us/library/ie/hh801215(v=vs.85).aspx
[smacssmodule]: http://smacss.com/book/type-module
[cssom]: http://nv.github.com/CSSOM/docs/parse.html
