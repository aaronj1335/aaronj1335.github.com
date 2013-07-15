---
layout: post
title: "CS373: deploying your app to heroku"
author: Aaron Stacy
category: cs373
tags: [devops, cs373]
---

# deploying your app to heroku

{% include byline %}

in my summer software engineering course we're making a website of information
about world crises using [django][]. we were experiencing some trouble with
deploying our apps. the original setup was a single university-hosted apache
instance with [mod\_wsgi][] loaded and configured in our local directories
using .htaccess files. it's difficult to administer a system in which you have
limited privileges for several reasons:

 - you can't control software versions, which is more difficult when you've
   developed your app locally on newer versions of the software.

 - you can't reload the server when you upload new code, so you're never quite
   certain whether the server just hadn't reloaded or the change you made
   didn't have any effects.

 - as deadlines approach, everyone is making numerous changes, and the network
   filesystem seems to become a bottleneck, making any action tediously slow.

[one of my classmates][eddie] was sharp enough to suggest we use [heroku][] for
future projects. as i've mentioned before, my professor is good at encouraging
us to use modern technologies in this course, so he agreed.  hopefully his
decision is reinforced by a good experience with heroku.

## reasons to use heroku

the trend these days seems to be towards hosted solutions. whether it's
[version control][github], [continuous integration][travis], or deployments,
small companies especially have a lot to gain by focusing their efforts on
their core business and spending their money on hosted solutions rather than
devops personnel. the heroku-style of platform-as-a-service also seems to be
popular, as other companies are following suit with platforms like
[openshift][] and [nodejitsu][] (though not all of them experience the same
[hot drama][drama]).

if nothing else, using heroku on these projects will give you valuable
experience, but i think it can also make your life easier. the pain points i
outlined above are all addressed:

 - heroku allows you to specify the versions of everything, from python to
   django to other third party libraries like minixsv. any library on [pypi][]
   is just a couple command line moves away, no support tickets, no licensing
   hassles.

 - deploying is as easy as pushing to a remote git repository. aside from
   convenience, this encourages good software engineering.

 - instead of burdening some poor corner of the university IT system, heroku
   has all the weight of [aws][] to absorb course deadlines. while the free
   instances are kinda wimpy, their performance is good enough, and more
   importantly, it's predictable.

## how to

our use-case is strait forward, so i found heroku's docs spot on. i'll end up
repeating a lot of their (superior) [tutorial][] below, but i'll try to
customize it a bit for our class and maybe inject a bit of hopefully-unbiased
opinions. we've all got our projects set up already, so we're not starting from
scratch as their article presumes.

**opinion #1: develop locally on your laptop** -- if you're main computer is
mac or linux this is especially blissful. either way you've probably already
got your dev environment setup from the first project, so just stick with that
because life is too short to spend it wrangling `$PYTHONPATH`'s.

### bootstrap

skip the `mkdir hellodjango && cd hellodjango` part in heroku's tutorial and
just make your `virtualenv`. `virtualenv` is basically a local python
installation for nothing but your project. that may seem weird but it's
actually colossally awesome because it saves you from [dependency
hell][dephell] which is a real place regardless of your religious inclinations.
run the commands:

    $ virtualenv venv --distribute
    $ source venv/bin/activate

don't check the `venv` directory into your repo. in fact you may want to make a
`.gitignore` file right now:

    venv
    *.pyc
    staticfiles

### install prerequisite dependencies

    $ pip install django-toolbelt

this installs a bunch of python modules you need to run django apps on heroku to your newly created `virtualenv`. while you're at it, install the project dependencies:

    $ pip install MySQL-python minixsv

`pip install` any other libraries you dig, and then record them for heroku by running:

    $ pip freeze > requirements.txt

at this point you may notice that heroku uses [postgresql][] by default instead
of mysql. you should probably just use with postgres since it's free and
default, and up to this point there hasn't been any reason to have written
custom sql, rather you should have just been using django's database management
facilities.

**opinion #2: keep it database agnoistic** -- i believe good [dependency
inversion][depinv] principles (which we'll learn about later in the course)
would instruct us to write an app that works with a mysql, postgres, or sqlite
backend (downing if you're reading this i'm sorry if i'm misleading; i assume
you'll have the chance to correct me in class). the thing is we're not doing
anything novel and we're not going to need to scale these apps, so it would be
awesome if we could just write some really robust code that works with a range
of databases.

i ended up using 3 different backends for this assignment, which is stupid, but
in-memory sqlite was fastest, so i typically used that for unit tests, mysql
was a requirement, so i set that up initially, and postgres is free and default
on heroku, so i deployed to that. like i mentioned, i didn't write a line of
sql, it was all just a matter of tweaking django's `settings.py` file.

### update settings.py

i slightly amended the heroku article's suggestions to [this][settings.py]:

<pre>
  <code class=python>
    if 'test' in sys.argv:
        # use in-memory db for unit testing b/c it's effin slow otherwise
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'crisis',
                'USER': 'crisisuser',
                'PASSWORD': 'bacon',
                'HOST': '',
                'PORT': '',
            }
        }
    elif 'PRODUCTION' in os.environ:
        # this is the heroku environment
        import dj_database_url
        DATABASES = { 'default': dj_database_url.config() }
    else:
        # and this is what you'll get when u run ./manage.py runserver
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'crisis',
                'USER': 'crisisuser',
                'PASSWORD': 'tupac',
                'HOST': '',
                'PORT': '',
            }
        }

    # Honor the 'X-Forwarded-Proto' header for request.is_secure() (whatevr
    # that means)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Static asset configuration
    import os
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(PROJECT_PATH, 'static'),
        os.path.normpath(os.path.join(PROJECT_PATH, '../crisis_app/static')),
    )
  </code>
</pre>

you can see the 3 different database configurations. the cool thing about
heroku is you can run the unit tests locally with sqlite or remotely in the
heroku environment quite easily.

### update wsgi.py

they also instruct you to update you `wsgi.py` file:

    from django.core.wsgi import get_wsgi_application
    from dj_static import Cling

    application = Cling(get_wsgi_application())

### deploying to heroku

this is where it actually happens:

    $ git add .
    $ git commit -m "added heroku stuff"
    $ heroku create
    $ git push heroku master
    $ heroku config:set PRODUCTION=1

that was it. much easier than zweb, right? now you can turn on your app and
visit the site:

    $ heroku ps:scale web=1
    # maybe wait a min?
    $ heroku run python manage.py syncdb
    $ heroku open

notice that running all of the django admin commands are the same as before
except you prepend `heroku run` if you want them to run on your deployed app.

## conclusion

awesome things happen when you make the right thing the easy thing, and heroku
exemplifies this by baking rock-solid engineering principles into every aspect
of website deployment and hosting. i'd definitely recommend using heroku for
the following phases of the project.

[eddie]: https://github.com/eddies5
[tutorial]: https://devcenter.heroku.com/articles/django
[dephell]: http://en.wikipedia.org/wiki/Dependency_hell
[depinv]: http://www.cs.utexas.edu/users/downing/papers/DSP1996.pdf
[drama]: http://news.rapgenius.com/James-somers-herokus-ugly-secret-lyrics
[heroku]: https://www.heroku.com
[mod\_wsgi]: http://code.google.com/p/modwsgi/
[django]: https://www.djangoproject.com
[github]: https://github.com
[travis]: https://travis-ci.org
[openshift]: https://www.openshift.com
[nodejitsu]: https://www.nodejitsu.com
[aws]: http://aws.amazon.com
[postgresql]: http://www.postgresql.org
[pypi]: https://pypi.python.org/pypi
[settings.py]: https://gist.github.com/aaronj1335/5997057
