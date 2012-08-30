---
layout: post
title: '"triangles", or "the shape of an application"'
description: "mv\* layout in client-side javascript applications"
category: code
tags: [code, javascript]
---
{% include JB/setup %}

mvc has become a bit of a buzzword. it's a complicated and nuanced concept, and even if you're using an mvc framework, it's easy to get wrong.

a year and a half ago i was interviewing for my first job as a client-side developer, and the question came up:

> what is mvc design?

i probably regurgitated something i had read on a blog post or tutorial that sounded something like:

> models are where you put your business logic.

while that may be true, it only applies to a specific use case. it glosses over the deeper concept, and as a result i made some poor design choices when i found myself in unfamiliar design territory.

regardless of your mv\* flavor (mvc, mvp, mvvm, …) one of the foundational concepts that you must get right is *separating and isolating state*, whether it's the number of items in a user's shopping cart or which todo the user is editing.

## bringing it down to earth

we'll look at a real world example that might tempt a developer to put state where it doesn't belong, and then apply mv\* concepts and see the benefits.

say you're one of the top-flight engineers on the [sparrow][] team, and you've just been [acquired by google][sparrow_gmail]. your assignment is to create a web application that measures up to the native mac and ios implementations.

### high level stuff

you do all the typical wire framing stuff and end up with some wires that look like this:

<img src="/assets/triangles/sparrow_gmail.png" />

you start banging out some code and come up with a view hierarchy that look like this:

<img src="/assets/triangles/app_structure.png" />

this is simplified for the sake of instruction, but basically you've got a view for the list of e-mails on the left, and a view for the selected message on the right. these are composed in a full mailbox view. the view hierarchy presumably reflects the dom hierarchy.

### first pass

a naïve way to hook all of this up may involve the code below (i'm using [backbone.js][backbone], because it's api is hopefully intuitive, but the concepts apply regardless of the framework).

 - user clicks an e-mail in the list, which causes the `MessageListView` to trigger the `messageselected` event:

        var MessageListView = Backbone.View.extend({
            events: {'click li': 'onMessageClick'},

            // ...

            onMessageClick: function(evnt) {
                // `message` is a Model instance for an email
                var message = this.getMessageModelFromDOMEl(evnt.target);
                self.trigger('messageselected', message);
            }
        });

 - the parent view (`InboxView`) handles the event, and delivers the newly selected model to the `MessageView`:

        var InboxView = Backbone.View.extend({
            events: {'messageselected': 'onMessageSelected'},

            // ...

            onMessageSelected: function(message) {
                // `this.messageView` is the instance of `MessageView` composed
                // by the parent `InboxView` widget
                this.messageView.setMessage(message);
            }
        });

 - the `MessageView` re-renders its contents with the selected email:

        var MessageView = Backbone.View.extend({

            // ...

            setMessage: function(message) {
                this.model = message;
                this.render();
            }
        });

### the problem

this design may seem harmless, like it's leveraging mv\* concepts with the views and the models, but the problem is we have not isolated application state in the model layer. there should be one and only one place where the page tracks what e-mail is currently selected.

as we'll see, leaving state around like this makes things complicated as the application grows.

### the geometry of a poor design

one hallmark of this sort of design is the communication triangle that forms between the parent view and its children:

<img src="/assets/triangles/triangle.png" />

the parent element should not need to be involved for this communication. this gets especially bad with heavily-nested view hierarchies. additionally, in my experience, this pattern encourages a lot of ad-hoc method names like `getMessageModelFromDOMEl` and `setMessage` which make it difficult to grok someone else's code.

### the fix

a more mv\* approach would track the selected mail message in the model layer. the `MessageListView` would simply set an attribute on a model in a collection, and the `MessageView` would listen for changes on that same collection. all the parent view has to do is make sure they've each got a reference to the same collection.

    var MessageListView = Backbone.View.extend({
        events: {'click li': 'onMessageClick'},

        constructor: function() {
            this.collection.on('change', this.onChange, this);
        }

        // ...

        onMessageClick: function(evnt) {
            var selectedMessage;

            this.collection.each(function(message) {
                // unselect everything, don't trigger any events
                message.set('selected', false, {silent: true});

                // find the selected model
                if (message.get('id') === $(evnt.target).data('message-id')) {
                    selectedMessage = message;
                }
            });

            // this will trigger a change event on the collection
            selectedMessage.set('selected', true);
        }

        // re-render the view, displaying the newly selected e-mail
        onChange: function() {
            this.model = this.collection.where({selected: true})[0];
            this.render();
        }
    });

    var MessageView = Backbone.View.extend({
        constructor: function() {
            this.collection.on('change', this.onChange, this);
        }

        // ...

        onChange: function() {
            this.model = this.collection.where({selected: true})[0];
            this.render();
        }
    });

now the collection serves as a [single point of truth][spot] for answering the question 'which e-mail is selected'.

one rule of thumb we see emerging here is that the model layer should be responsible for publishing events to disparate pieces of code. when a view is responsible for tracking state like which resource a user selected and another view needs to be notified of changes, the information must go all the way up through a common ancestor in the view hierarchy and back down.

### and the payoff

now pretend that new features have crept into the requirements (i know, right?), and when the user refreshes the page, our app must load the message the user was previously viewing. this is an excellent chance to make use of the [html5 history api][history], especially since it would give us client-side routing for free (eek!).

when the user selects a message, we'll update the url with a slug for the message's subject. so our wireframes would become something like this (notice the updated url):

<img src="/assets/triangles/sparrow_gmail_with_routing.png" />

this feature introduces a second means of setting the selected message (via the url), and in our first design it becomes extremely tricky to correctly render the views: the parent has to decide whether to update the `MessageView` based on the `MessageListView` or the url. this doesn't scale either, since the parent view must be modified every time we add a new way for the user to set the selected message.

however our second design handles this much more elegantly. we don't even need to touch the existing code, just add a bit of routing code to the top level of our application:

    window.addEventListener('popstate', function(e) {
        // `emails` is the same collection the views reference
        emails.each(function(message) {
            message.set('selected', false, {silent: true});
            if (message.get('id') === getIdFromUrl()) {
                selectedMessage = message;
            }
        });
        selectedMessage.set('selected', true);
    });

    emails.on('change', function() {
        var selectedMessage = emails.where({selected: true})[0];
        history.pushState(null, null, makeUrlFromModel(selectedMessage));
    });

the app is really leveraging mv\* design concepts now. the model layer gives us a way to loosely couple components, such that we can integrate features into the app without having to modify existing code. that's powerful.

## bringing it back up

these concepts are core to mv\* design, and while the approach is different depending on the framework (for instance [ember][] introduces a [state manager][ember_state_manager]), the key is to *isolate state*, and use that to drive updates in your views.

[sparrow]: http://sprw.me
[sparrow_gmail]: http://arstechnica.com/business/2012/07/google-acquires-sparrow-integrates-it-into-the-gmail-team/
[backbone]: http://backbonejs.org
[spot]: http://www.faqs.org/docs/artu/ch04s02.html#spot_rule
[history]: http://dev.w3.org/html5/spec/single-page.html#the-history-interface
[ember]: http://emberjs.com
[ember_state_manager]: http://docs.emberjs.com/symbols/Ember.StateManager.html
