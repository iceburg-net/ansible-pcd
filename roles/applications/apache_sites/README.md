apache_sites
============

preparation:
===

* creates "siteop" user (defined defaults/main.yml as apache_sites_user)
  * siteop home defaults to /sites
  * adds github signatures to known_hosts (to allow git checkout without interruption)
  

deployment:
===

* loops through `apache_sites_list` (typically defined as host or group inventory var)
  * ensure /sites/<org> exists
  * checkout to /sites/<org>/<name>  @todo (add stage/prod support)
  * registers site with apache (prepare virtualhost entries)
  