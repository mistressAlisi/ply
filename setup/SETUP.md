<div align="center">
  <h1>The abridged Ply setup guide.</h1>
</div>
<p>This is a really brief description for getting your own local devel instance of Ply up and running. We do our devwork on Debian Linux - and our setup script is designed for debian. But it can easily be modified for RHEL and Ark distros.</p>
<h3 align="center">--In a Nutshell:--</h3>
<p>
You might want to review setup.sh as your read along.<br/>To get started quickly, the script will (if it is not installed) install python3 and python3-venv, ask you for a path to create a virtual env, and then install our 'requirements.txt' into the virtual env. We also need pwgen and we install it at this point.
</p>
<p>
In order to support containerisation and portability; the design assumes that .config will be mounted at any given time the application runs. You should create an external config dir and bind-mount it even if you intend to run locally - this way your config is not inside the devtree and it should never be.
</p>
<p>
<em>config.ini</em> is generated from the skeleton file that's supplied with the SETUP folder; it will be rehashed with a new DJANGO_SECRET key.
</p>

<p>
Ply is built on PostgreSQL release 13. If we're using it locally for development, at this point the script will assist in installing and configuring the Server locally: If using a previously configured or external PG server, simply skip installation and enter the connection parameters into the script.
</p>

<p>
Once the database is created; the script will automatically execute migrations and then run the SQL installation procedure to install SQL routines to the database. Afterwards, please follow the prompts to create a superuser, install timezones, templates, dynapages, and other database initialisation routines.
Finally, the script will ask you to create a community as detailed in the main README.md: at the very least; you must have one community for the application to function.
</p>

<p>After that, you should be all set!</p>
