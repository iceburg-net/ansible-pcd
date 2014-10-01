awstats
=======

AWStats analyzes webserver log files and outputs useful statistics on
visitors, pages, and bandwidth usage.

Statistics are available through the statistics site, which can be
reached via http://stats._fqdn_/ by default (e.g. http://stats.nashville-app-1.iceburg.net/).

You can override the statistics site server name by setting AWSTATS_SITE_NAME
in your inventory variables, e.g. "AWSTATS_SITE_NAME = stats.iceburg.net"

The statistics site will give an overview of the sites on your server,
sorted by bandwidth usage. Clicking on a site will open the AWStats 
frontend for more detailed information. 

We use the JAWStats-fork frontend by default -- mainly because it drops the
dependency on mod_cgi ...as if we haven't been hacked through an [exposed mod_cgi script](http://archive09.linux.com/feature/113974) before!
If you prefer, use the stock AWStats fronend by setting 
AWSTATS_ENABLE_JAWSTATS_FRONTEND to False. Be sure to enable mod_cgi 
if you disable JAWStats. 

The statistics site is protected with HTTP Basic Authentication, and user/pass 
is controlled via AWSTATS_HTPASSWD_USER and AWSTATS_HTPASSWD_PASS. They default
to the `private_user_name` and `private_user_pass` variables from your
_PRIVATE_/vars/private.yml -- and can be set to whatever you like.


