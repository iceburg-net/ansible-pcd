apache_sites
============

deploy sites in git repositories to an apache web server.

optionally provision databases + users users as well

  
### usage

* define sites via `apache_sites_list` (typically an inventory variable for your
host/group)

e.g.

```
---
#  iceburg-web-servers Inventory Variables


# Apache Site Definitions
# 
#   name: site name, typically www.domain.com
#
#   org: site organization, defaults to {{ apache_sites_default_org }}
#
#   repo: git repository containing site files
#
#   branches: branches to checkout, defaults to ["master"]. checked out to;
#     {{ apache_sites_user_home }}/<org>/<name>/<branch> }}  e.g.
#     /sites/iceburg/www.iceburg.net/master
#   
#   template: jinja template of apache config file (virtualhost definition),
#      defaults to apache_config.j2, can be full path.
#
#   docroot: document root (path to public web files) within repository,
#      defaults to "www", can be empty. "www" represents;
#      {{ apache_sites_user_home }}/<org>/<name>/<branch>/www  e.g.
#      DocumentRoot /sites/iceburg/www.iceburg.net/master/www
#  
#####################  
apache_sites_list:
  - {
    name: www.iceburg.net,
    org: iceburg, 
    repo: "git@github.com:iceburg-net/www.iceburg.net.git",
    branches: ["master", "stage"] 
    }
```

* prepare and/or deploy your site(s) to apache web servers.


```
# prepare and deploy all sites
ansible-playbook -i inventory/iceburg.hosts application_prepare.yml 


# deploy a specific site
ansible-playbook -i inventory/iceburg.hosts application_prepare.yml --tags=deploy --extra-vars=apache_sites_site=www.iceburg.net
```

apache_sites has the additional ability to provision databases + users as well.
mysql is currently supported. define your databases in the [OPTIONAL]
_apache_sites_private_file_ variable file. the location of this file defaults
to: "{{ pcd_private_dir }}/vars/apache_sites/{{ inventory_hostname }}.yml",
although you may easily override via inventory vars &c. Below is an example;

```
---
#  iceburg-web-servers apache_sites private variables


apache_sites_mysql_login_host: localhost
apache_sites_mysql_login_user: root
apache_sites_mysql_login_password: ""


# site mysql databases to create. NOTE that key must match site name
apache_sites_mysql_list:
  www.iceburg.net:
    [ {name: prod_iceburg, user: iceburg_adm, pass: Zal3091gHz},
      {name: stage_iceburg, user: iceburg_adm, pass: Zal3091gHz}
    ]
```




### prepare phase

* creates "siteop" user (defined defaults/main.yml as apache_sites_user)
  * siteop home defaults to _/sites_
  * adds github signatures to known_hosts (to allow git checkout without interruption)
* provisions databases if supplied
  

### deploy phase

* loops through `apache_sites_list` (typically defined as host or group inventory var)
  * ensure _/sites/<org>_ exists
  * git checkout to _/sites/<org>/<name>_  @todo (add stage/prod support)
  * registers site with apache (template virtualhost entry to _os_apache_sites_dir/<name>_)