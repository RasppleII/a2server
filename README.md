# A2SERVER
AppleTalk server for Apple // computers developed by Ivan Drucker

Documentation here is sparse for the moment; see [Ivan's site]() for
information about A2SERVER and how it all works.  There's a lot there and it's
kind of evolved organically over the years just as the scripts themselves
have, so it's going to be awhile before that information can be backfilled and
perhaps organized into something you might call a user manual.

Such a manual should not be considered a replacement for Ivan's organic online
documentation--those contents themselves represent Apple // history, if a
relatively modern piece of it.  As such they should be preserved as they are.

## Developer note

To use the scripts on a server other than Ivan's, you'll want to export
the shell variable A2SERVER_SCRIPT_URL to the base URL of this repository
on your server.  The base-URL should be slash-terminated.  You can then run
the following snippet:

~~~ bash
wget -O a2server-setup ${A2SERVER_SCRIPT_URL}setup/index.txt; source a2server-setup
~~~

A simple method for installing from a local subdirectory is to `cd` to it and
then type `python -m SimpleHTTPServer`. Then
`export A2SERVER_SCRIPT_URL="http://localhost:8000/"`
or use the IP address of the host machine on your LAN instead of localhost.

You should probably export A2SERVER_SCRIPT_URL in your .bashrc or whatever
file configures your development environment.  Also be advised that as of
version 1.24 of A2SERVER, you must use the snippet above.

[Ivan's site]: http://appleii.ivanx.com/a2server/
