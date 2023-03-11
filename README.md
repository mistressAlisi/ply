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
</ol>
</p>


