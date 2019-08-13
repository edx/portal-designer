New Designer Service
######################
Status
======

Accepted

Context
=======

**Quick note on "theming"**: The word "theming" will be used many times in this
document. Theming in regards to this application will primarily consist of
minor style changes (mostly a color change or two), header and footer options
(including links, logos, and possible copy text).

As we build out the learner portal for Masters / Enterprise functionality, we
need to be able to properly theme and generate custom pages for them. To
support all of these features, we chose to utilize Gatsby (a javascript
framework) on the frontend which allows to take in a configuration (that
consists of theming and pages) and will export a site with the theme "baked in"
and the unique pages generated.

With that in mind, we needed a solution that would be easy to integrate and
easy to manage.

Decision
========

A new service called "portal-designer" (or "designer" for short) will be
created based on the Wagtail (CMS) framework.

Requirements of service
-----------------------
- Easily integrate with the Gatsby site generator
- Allow creation of new sites to be generated
- Allow for theming per site
- Allow for creation of individual pages for each site (specific program or
    pathway pages in addition to an index/home page)
- Provide role-based access which would help support self-service in the future

How it will work
----------------

Context
~~~~~~~~
For each partner that wishes to have their own portal we will be generating
a unique build of the application. What this means is that the frontend
application will be built with the configuration for a site and exported into
it's own directory. We will then be pointing unique URLs at each directory, so
each customer has a custom URL pointing to custom code. As the majority of this
work will happen outside of this application, we won't go into details here.
We are just going to discuss how to support this model.

Sites
~~~~~
Each site / deployment that we want created will correspond to a single site
in Wagtail. We will make all APIs queryable by the hostname of the site, so
that when we build ``www.example.com`` we can simply query this service for
that site's theme and pages.

Theme
~~~~~~~~~~~~~
Each site will have a SiteBranding model which will be based on Wagtail's
``SiteSetting``. What this provides is an easy UI for editing a theme that
is linked to a Site and is editable in the Wagtail CMS, thus requiring us to
not allow access to Django Admin.

This is a similar idea to SiteConfiguration in other services (with the
addition of CMS access), and was previously used in our other Wagtail service
Journals.

Pages
~~~~~
In wagtail each site must have a root page, the pages are set up in a tree
structure, and each page type has it's own model. In order to support our page
requirements, we will adopt a structure where each site's root page will
correspond to the home page on their site, and all other pages (program pages,
enterprise pathway pages, site-specific FAQ pages), will lie directly under the
index page. By limiting the structure to two levels, we remove the necessity of
handling the tree structure client side which will make development easier, and
limit the overhead of editors trying to remember where things should be
located.

Note: If a desire for a tree structured system arrives in our future, this
decision does not limit us or cause undue work, it simply allows us to delay
that work until it is deemed necessary.

A example structure would looks like this ::

    - Root
        - IndexPage()
            - ProgramPage(title="Masters in Accounting")
            - ProgramPage(title="Masters in Philosophy")
            - FAQPage()
        - IndexPage()
            - PathwayPage(title="Security Compliance")
            - FAQPage()


Permissions
~~~~~~~~~~~
Wagtail provides a permissions system (built on Django's) which is based on
groups. When we generate a new site for a customer, we will also create a
group named after the site (ExamplePartner-Admin). We then give that group
permissions to their SiteBranding, as well as their IndexPage and all sub-pages
of it.

Since it is a CMS, Wagtail also provides collections for documents and images
so if we wish to store those items in site-named collections, we can create
those when we create the site link them to a group's permissions.

Most of this will be automated.

API
~~~
Gatsby will be building pages based on the responses of the APIs in this
service. Since it will be building each site individually, we will need all
APIs to be queryable by the site name.

Wagtail provides a Pages API which we will have to minimally customize, that
will provide all the necessary data for Gatsby to build the pages.

We will also have an additional API to retrieve the theme information that will
be pulled from the SiteBranding model.

Options we decided against:
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configuration data can be stored in many ways, here are some options we looked
at, but decided against.

Configuration files
+++++++++++++++++++
Having a single file or folder inside of a repo that contains all of the
configuration (theme + pages) for a site seems convenient. You have an easily
visible configuration and are able to use things like git hooks to trigger
builds. We chose not go down this route because of the requirement that an
editor would need to be knowledgeable in git and the UX for non-engineers would
not be enviable.

Netlify CMS
+++++++++++
In order to bridge the benefits of configuration files and the cons of poor UX,
we looked at Netlify CMS which works with config files in a git repository, but
provides a client side CMS that makes the experience much better. After
initially going down this route, we ran into a plethora of issues regarding
authentication and tying the service into the rest of the Open Edx ecosystem.


Consequences
============

- Designer will be allow for quick and easy customization of new configured
    learner portals.
- Future self-service customization of the Open edX experience will be more
    feasible.
- We will be able to support many lightly themed sites, versus a few which
    require heavy customization and engineer investment.
