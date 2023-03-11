<div align="center">
  <h1>Welcome to Ply.</h1>
</div>

<div align="center">
  <!-- breaks if we dont have this blank line -->
  
  <a href="">![GitHub contributors](https://img.shields.io/github/contributors-anon/mistressAlisi/ply?style=for-the-badge)</a>
  <a href="">![GitHub issues](https://img.shields.io/github/issues/mistressAlisi/ply?style=for-the-badge)</a>
</div>

<h4 align="center">
  Nerdy name aside; Ply is a toolkit and platform to rapidly create, implement and customise websites and webapps that have Social, Sharing, and RolePlaying components.
</h4>
<hr/>
<h3 align="center">--Design Philosphy--</h3>
<p align="center">The application is built mostly with Python and Django. It makes heavy use of PostgreSQL and some neat features like PL/pgSQL for the backend: The philosophy behind the backend is to "make it as simple and efficient as possible" - one of the ways we do that is by keeping processing of data to the minimum level possible, and by reducing all not needed loops for data algos. PL/pgSQL helps us greatly in doing a lot of lifting inside the database itself to keep the Django Engine highly performant and responsive. Ply scales very well using UWSGI/Gunicorn (we test using UWSGI) and NGINX. Several key concepts that Ply relies on are explained below. (Please note; modules MAY have cross-dependencies! Such as the Dynapages module explained further below.)
</p>

<h3 align="center">--Introduction--</h3>
<p align="center">Ply is highly flexible and can be used in an infinite number of configurations to host Communites, Websites, Galleries, Role Playing games that use Pen and Paper information, and in the future, Second Life-based Roleplaying using an integrated HUD we call PlyHUD (under development.)
</p>

<p align="center">The application is built mostly with Python and Django. It makes heavy use of PostgreSQL and some neat features like PL/pgSQL for the backend: The philosophy behind the backend is to "make it as simple and efficient as possible" - one of the ways we do that is by keeping processing of data to the minimum level possible, and by reducing all not needed loops for data algos. PL/pgSQL helps us greatly in doing a lot of lifting inside the database itself to keep the Django Engine highly performant and responsive. Ply scales very well using UWSGI/Gunicorn (we test using UWSGI) and NGINX. Several key concepts that Ply relies on are explained below:
</p>

<h3 align="center">--Database design philosophy--</h3>
<p align="center">
The database design is crucial for the flexibility and scalability of the platform. We have deliberately designed it to be completely capable of many communities at once, with any given profile being able to join an unlimited number of these. To further leverage scalability; any plyhost can support any given number of virtual hosts just like NGINX or Apache. Using HTTP header matching, Ply can seamlessly support an unlimited number of Virtual Hosts, thus, an unlimited number of communities can be hosted on-platform. This design decision is critical and it leads to the database structures you will find throughought Ply.
Users can own unlimited profiles. Each profile can join unlimited communities. Each community can have unlimited groups. Users can use the same authentication token and structure consitently throughout communities as long as they are using the same account to change from one community (or host) to the other. Since a user can have an unlimited number of profiles, it is perfectly possible to keep data separate even if the same account owns the profiles. Of course, if the user so chooses, they may join any given community with both, or all of their profiles. As long as the relationship is not duplicated; it will be valid. (And ply does not allow for this duplication by design anyway - so don't worry about it!)
</p>

<h3 align="center">--Core Ply features--</h3>
<p align="center">By design, Ply is highly customisable and extensible. It relies on the Django philosophy of keeping individual "Apps" (or services) in their own separate modules inside the main ply namespace. The following modules are provided and under active development:
<ol>
  <li><strong><em>almanac</em>:</strong> A dynamic webpage and blogging module that closely resembles a CRM, with customisable, user-editable pages and menus.</li>
  <li><strong><em>categories</em>:</strong> Provides a set of Disciplines and Categories, mostly designed to implement Artwork galleries and content sharing. Disciplines and Categories allow you to tag artwork, such as, Photography/Nature for photos of such, or Artwork/calligraphy if so desired. All values are fully customisable and flexible. Ply ships with a default set of datasets which can easily be used or ignored as you need in a TSV file.</li>
  <li><strong><em>combat</em>:</strong> A module to implement RPG-style turn-and-dice combat rolls and actions for role-playing situations, both on-platform and inside the SLHUD. (under heavy development - not yet fully implemented)</li>
  <li><strong><em>Comms</em>:</strong> Implements the basic communication paradigm needed for social networks and user interaction: Notifications and Messages.</li>
  <li><strong><em>community</em>:</strong> Implements one of the most important concepts in Ply. The Community. This module underpins almost all other data relationships: At a minimum, a profile/agent must be associated with at least one community. It is so important it has its own readme inside its folder. (please review it!)
  </li>
  <li><strong><em>dashboard</em>:</strong> The central point of interaction for users with the platform. The Dashboard provides a fully bootstrap-compliant, responsive interface from which the user can perform any number of given tasks within Ply. (This module also has its own description.)
  </li>
  <li><strong><em>dynapages</em>:</strong> The Dynamic Pages (dynaPages) module implements a fully user-customisable, dynamically reconfigurable template engine based on widgets and page templates. Users and admins can create custom page views, templates, and supply widgets that can be used anywhere in the platform. This module is the underlying engine that provides this functionality and it also has its own description it its folder.</li>
  <li><strong><em>equipment</em>:</strong> Equipment will provide an inventory, and as the name suggests; a character equipment system for the RPG and the SLHUD modules.
  </li>
  <li><strong><em>events</em>:</strong> The Events module will provide a fully fledged system for creating, running and managing the results of roleplaying events for the RPG and SLHUD modules.
  </li>
  <li><strong><em>exp</em>:</strong> The exp module provides an experience and leveling system for Character/profile progression. The module supports dynamic scripting and custom triggers for leveling up.
  </li>
  <li><strong><em>forge</em>:</strong> Where Ply worlds are forged! As the name implies, the forge is where things are created and modified. It provides the user interfaces needed to create, modify and manage communities, profiles and alamanac pages. It is the primary editor of the platform that's not django-admin and it has its own documentation.
  </li>
  <li><strong><em>gallery</em>:</strong> The gallery module is a highly configurable system for creating artwork galleries. Multiple artwork types are supported by a plugin interface: For example, gallery_photos provides a photography module. gallery_writing a prose and written artwork module. The gallery module core is responsible for the logic of storing, serialising, and cataloguing the data. It supports a dynamic upload of content to any storage mechanism (see docs) and it contains the data structures for collections and items alike. The gallery plugin module is only responsible for rendering and processing the artwork for the main module. This is obviously further explained in the gallery's readme.
  </li>
  <li><strong><em>group</em>:</strong> Groups are just like social media / community groups. A grouping of n+1 profiles. They must belong to a community. Groups have custom pages just like profiles and a few other neat features like group-level communications.
  </li>
  <li><strong><em>items</em>:</strong>Items that will be used in-world. These are NOT inventory items, rather, they are objects that can exist in SL and be interacted with. (in design stage..)
  </li>
  <li><strong><em>keywords</em>:</strong>The Keywords module provides a simple, yet efficient implementation of hashtype type keywords for the platform. Particularly the stream module.
  </li>
  <li><strong><em>metrics</em>:</strong>Metrics provides a fully fledged, internally-supplied and granular analytics and metrics module to track activity and track the actions of characters and profiles in a safe, anonymous way that does not compromise privacy - it never leaves the platform! A neat Metrics API is implemented for custom data types.
  </li>
  <li><strong><em>notifications</em>:</strong>These are system-based notifications and mentions. They're generated by system modules; not profile/user interaction.
  </li>
  <li><strong><em>ply/toolkit</em>:</strong>The toolkit is the preferred way of interacting with the Ply Core modules in a consistent and stable manner. The Toolkit abstracts away most of the complexity and the intricacies of the platform and simply provides an easy way to perform almost any imaginable task. The code itself we write uses the toolkit, so it's pretty important! And it's got its own documentation.
  </li>
  <li><strong><em>plydice</em>:</strong>Our very own RPG Dice rolling system with a fully fledged audit trail.
  </li>
  <li><strong><em>plyscript</em>:</strong>PLYscript allows custom behaviour written in python to be included for specific events and triggers. It is the logic module that runs commands from SLHUD on the plyside. All scripted (custom) behaviour that is used throughout the platform is stored and managed in this module.
  </li>
  <li><strong><em>profiles</em>:</strong>Profiles provides support for a complete, customisable framework for users to create profiles for their characters or themselves. Each account can hold an unlimited number of profiles. A user can change which profile to appear as at any time. A profile can be associated to one or more communities. Each profile has a custom page, custom abilities, skills, experience, a complete audit trail, and more. This module is further documented individually.
  </li>
  <li><strong><em>preferences</em>:</strong>Preferences - As advertised. For the users and profiles.
  </li>
  <li><strong><em>skills</em>:</strong>The Skillsystem implements support for giving characters specific skills for RPG situations - with the support for plyscript supplied behaviour and integration with plydice for custom interactions.
  </li>
  <li><strong><em>SLHUD</em>:</strong>The SLHUD Module - it is supplied by the server via HTML!
  </li>
  <li><strong><em>spells</em>:</strong>The magick system for RP games! This will provide magick, which can be driven with Dice rolls and Plyscripts.
  </li>
  <li><strong><em>stats</em>:</strong>The Statistics module provides profile/character statistics, which can be customised for each community, class, and community.  </li>
  <li><strong><em>streams</em>:</strong>The Streams are "streams of thought" - they are a form of microblogging service with a limit of 5,000 chars. Streams also support attachments and can leverage dynawidgets to render specific types of content. Dice, Galleries and other events already provide stream plugins; enabling users to seamlessly share their content with the community as they create it. This module has its own documentation.
  </li>

  </ol>
</p>


