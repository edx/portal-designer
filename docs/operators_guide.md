# Guide to managing portal-designer
## Setting up permissions
There are 3 distinct levels of permissions.
  - Administrators: Can access everything
  - Operators: Can manage all sites and pages
  - `<site>`_Moderators: Can manage pages for their site

Before you can assign a user to a group, they'll need to have attempted to login into the site before. They can do this by going to `<hostname>/login`. They will receive an access denied error at first, but will then show up in the Users view, where they can be added to the correct group.

## Creating a new branded portal
Before a new site can be created, some configuration and infrastructure must be set up first. Please enter a ticket with engineering to set this up first. Once this is done:
1. Enter `<hostname>/cms/`
2. Click `Settings`
3. Click `Add a site`
4. Enter sitename/hostname for the site and click `Create Site`.

Note that `sitename` is the name that will show up in the CMS and `hostname` needs to be the hostname that the site will be deployed at. They can also be the same.

Creating the site will also create the `<sitename>_Moderators` group that will only have permissions to that site.

It will also create a new page under Pages called `<sitename> Index Page`.

## Creating Programs
1. Click on the `<sitename> Index Page` of the site that you wish to add a program to.
2. Click `Add Child Page`
3. Fill out the data for site
    - `Title` will be the name of the program in the portal
    - `Slug` will be program name in the URL (e.g. if the slug is `comp-sci`, then the URL will be `organization.example.com/comp-sci`)
    -
