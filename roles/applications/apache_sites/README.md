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
#  nashville-web-servers Inventory Variables

# Apache Site Definitions
#########################
#
#   name: (required, unique) apache ServerName, typically www.domain.com
#
#   org: (opt) site organization, defaults to {{ apache_sites_default_org }}
#
#   apache_alias: (opt) apache ServerAlias, e.g. "domain.com domain.net"
#
#   apache_config: (opt) template to use for apache config (virtualhost def),
#     defaults to "virtualhost_default.j2". relative to apache_sites/templates
#
#   apache_config_includes: (opt) files to include in the virtualhost definition
#     defaults to: []
#
#   apache_serveradmin: (opt) apache ServerAdmin, e.g. "webmaster@domain.com",
#     default_user_email, override via apache_sites_default_apache_serveradmin
#  
#   ip: (opt) ip address (e.g. <VirtualHost <ip>:<port>), defaults to "*"
#   port: (opt) port, defaults to {{ apache_http_port }}
#
#   ssl: (opt) True/False to enable SSL
#      defaults to False. When True, apache_config will default to 
#      "virtualhost_default_ssl.j2", with http traffic redirected to https
#
#   ssl_ip: (opt) SSL ip (<VirtualHost <ssl_ip>:<ssl_port>), defaults to "*"/SNI
#   ssl_port: (opt) port, defaults to {{ apache_https_port }}
#   ssl_key: (opt) key file, defaults to {{pcd_certs_dir }}/<name>.key
#   ssl_crt: (opt) certificate file, defaults to  {{pcd_certs_dir }}/<name>.crt
#
#   git_repo: (opt) git repository (clone URL) containing site(s)
#
#   git_branch: (opt) branch to checkout, defaults to "master"
#     target {{ apache_sites_user_home }}/git-checkouts/<git_repo>-<git_branch>
#     creates {{ apache_sites_user_home }}/<org>/<name>-<git_branch> as link,
#     e.g. /sites/ansible/www.domain.com  --> 
#          /sites/ansible/git-checkouts/<git_repo>-<git_branch>
#
#   docroot: (opt) document root / path to public web files within repository,
#      defaults to "www", can be empty string. e.g.
#      DocumentRoot /sites/ansible/www.domain.com-master/www
#
#   allow_override: (opt) True (AllowOverride All) or False (AllowOverride None)
#      defaults to False.
#      apache_sites recommends disabling overrides for performance. 
#      consider adding your .htaccess content via an include.
#
#########################


apache_sites_enabled_list:
  - {
    name: www.iceburg.net,
    org: iceburg, 
    git_repo: "git@github.com:iceburg-net/www.iceburg.net.git",
    }

apache_sites_disabled_list:
  - www.domain.com
  - another.disabled-domain.com
```

* optionally provision mysql databases &c during site preparation by providing
definitions in your private variable file. example; 

```
---
#  nashville-web-servers apache_sites private variables


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