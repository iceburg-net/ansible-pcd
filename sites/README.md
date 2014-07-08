ansible-pcd site definitions
============================

ansible-pcd makes it easy to manage sites on a host.

* by default, site definitions reside in the /sites directory
  * you may change the location by setting PCD_SITE_DEFINITIONS in inventory.
  
* sites have a parent organization, e.g. "stats.iceburg.net" belongs to "iceburg"
  * site definitions reside in a subfolder named after their parent organization
    * e.g. /sites/iceburg/stats.iceburg.net.yml
  * this convention allows for easier maintenance of massive installs
  
* your definitions override sane defaults (referenced below). only override what is necessary.

```
# Site Definitions
#
# SITE_ALIASES: (list | []) site aliases, e.g. ["domain.com", "domain.net"]
# SITE_TYPE: (str | "") silverstripe-3.1, wordpress-3, &c.
# SITE_INCLUDES: (list | []) templates appended to server/virtualhost definition
# 
# SITE_HTTP: (bool | True) enables http site
# SITE_HTTP_IP: (str | "*") site http ip address
# SITE_HTTP_PORT: (int | {{ HTTPD_HTTP_PORT }}) site http port
# 
# SITE_HTTPS: (bool | False) enables https site                   [ssl]
# SITE_HTTPS_IP: (str | "*") site https ip address                [ssl]
# SITE_HTTPS_PORT: (int | {{ HTTPD_HTTPS_PORT }}) site https port [ssl]
#
# SITE_SSL_KEY: (path | "{{PCD_CERTS_DIR }}/{{ site_name }}.key") SSL Key File
# SITE_SSL_CRT: (path | "{{PCD_CERTS_DIR }}/{{ site_name }}.crt") SSL CRT File
#
# SITE_PATH: (path | "{{ PCD_SITES_DIR }}/{{ site_org }}/{{ site_name }})")
# SITE_DOCROOT: (str | "www") DocumentRoot folder (relative to SITE_PATH)
# SITE_SERVERADMIN: (str | "{{ SITE_DEFAULT_SERVERADMIN }}") admin email address
#
# SITE_LOG_FILE: (path | {{ HTTPD_LOG_DIR }}/access/{{ site_org }}.log) log file
# SITE_LOG_ERRORS_FILE: (path | {{ HTTPD_LOG_DIR }}/errors/{{ site_org }}.log)
# SITE_LOG_FORMAT: (str | {{ HTTPD_LOG_FORMAT }}) log file format
#
# set SITE_GIT_REPO to clone URL if site is contained in git repository
# SITE_GIT_REPO: (str | "") git repository (clone URL) containing site
# SITE_GIT_BRANCH: (str | "master")
#
# set SITE_MYSQL_DB to create a MySQL database + user belonging to this site
# SITE_MYSQL_DB: (str | "") mysql database name
# SITE_MYSQL_USER: (str | {{ SITE_DEFAULT_MYSQL_USER }}) mysql username
# SITE_MYSQL_PASS: (str | {{ SITE_DEFAULT_MYSQL_PASS }}) mysql username password
#
# SITE_REDIRECT: (str | "") URL Site Redirects to - e.g. "http://othersite.com"
#
# SITE_ENABLE_AWSTATS: (bool | False) aggregate statistics with awstats
# SITE_ENABLE_BACKUP: (bool | False) include site assets in backups
# SITE_ENABLE_OVERRIDES: (bool | False) allow apache .htaccess overrides
#
```

notes
=====

* you may provide an apache/nginx virtualhost/server template per site.
  * save the template in the site definition directory and name it;
    * for apache, <site_name>-apache.j2, e.g. /sites/iceburg/www.iceburg.net-apache.j2
    * for nginx, <site_name>-nginx.j2, e.g. /sites/iceburg/www.iceburg.net-nginx.j2
  * [default virtualhost template](https://github.com/iceburg-net/ansible-pcd/blob/master/roles/pcd-sites/apache_site/templates/virtualhost.j2) is in the roles/pcd-sites/(apache_site|nginx_site)/templates directory

* you may provide an awstats config template per site.
  * save the template in the site definition directory and name it;
    * <site_name>-awstats.j2, e.g. /sites/iceburg/www.iceburg.net-awstats.j2
  * [default awstats template](https://github.com/iceburg-net/ansible-pcd/blob/master/roles/pcd-apps/awstats/templates/awstats_default.j2) is in the roles/pcd-apps/awstats/templates directory
  
    