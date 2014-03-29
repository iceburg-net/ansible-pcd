apache_sites
============

deploy sites in git repositories to an apache web server.

optionally provision databases + users users as well

  
### usage

* define enabled and disabled sites via the `apache_sites_enabled_list` and   
`apache_sites_disabled_list` variables. set these via inventory variables
(typical) or explictly (atypical). example inventory file;


```
---
#  iceburg-web-servers Inventory Variables

# Apache Site Definitions
# 
#   name: (required) site name, typically www.domain.com
#
#   org: (opt) site organization, defaults to {{ apache_sites_default_org }}
#
#   apache_alias: (opt) apache ServerAlias line, e.g. "domain.com alias.net"
#
#   apache_config: (opt) template to use for apache config / virtualhost def.
#      defaults to virtualhost_default.j2.
#        can be full path, or relative to apache_sites/templates directory.
#
#   git_repo: (opt) git repository containing site files
#
#   branches: (opt) branches to checkout, defined as an array.
#     defaults to ["master"]. branches are checked out as; 
#       {{ apache_sites_user_home }}/<org>/<name>/<branch> }}  e.g.
#       /sites/iceburg/www.iceburg.net/master
#
#   docroot: (opt) document root / path to public web files within repository,
#      defaults to "www", can be empty. "www" represents;
#        {{ apache_sites_user_home }}/<org>/<name>/<branch>/www  e.g.
#        DocumentRoot /sites/iceburg/www.iceburg.net/master/www
#
#      common repository structure 
#      /  
#      /assets  [ asset files - e.g. databases, photoshop mocks, &c ]
#      /www     [ docroot ]
#
##################### 
apache_sites_enabled_list:
  - {
    name: www.iceburg.net,
    org: iceburg, 
    repo: "git@github.com:iceburg-net/www.iceburg.net.git",
    branches: ["master", "stage"] 
    }

apache_sites_disabled_list:
  - {
    name: dev.example.com,
    org: "{{ apache_sites_default_org }}",
    repo: False
    }
```

* optionally provision mysql databases &c during site preparation by providing
definitions in a private variable file. the location of this file is controlled
by the `apache_sites_private_file` and defaults to: 
"{{ pcd_private_dir }}/vars/apache_sites/{{ inventory_hostname }}.yml". 
example private var file;

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


* execute a playbook that includes the apache_sites role. example;


```
# prepare and deploy all sites
ansible-playbook -i inventory/iceburg.hosts application_prepare.yml 


# deploy a specific site
ansible-playbook -i inventory/iceburg.hosts application_prepare.yml --tags=deploy --extra-vars=apache_sites_site=www.iceburg.net
```


#### prepare phase

* creates "siteop" user (defined defaults/main.yml as apache_sites_user)
  * siteop home defaults to _/sites_
  * adds github signatures to known_hosts (to allow git checkout without interruption)
* provisions databases if supplied
  

#### deploy phase

* loops through `apache_sites_list` 
  * ensure _/sites/<org>_ exists
  * git checkout to _/sites/<org>/<name>_  @todo (add stage/prod support)
  * registers site with apache (template virtualhost entry to _os_apache_sites_dir/<name>_)