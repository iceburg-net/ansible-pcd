apache_sites
============

### preparation

* creates "siteop" user (defined defaults/main.yml as apache_sites_user)
  * siteop home defaults to _/sites_
  * adds github signatures to known_hosts (to allow git checkout without interruption)
  

### deployment

* loops through `apache_sites_list` (typically defined as host or group inventory var)
  * ensure _/sites/<org>_ exists
  * git checkout to _/sites/<org>/<name>_  @todo (add stage/prod support)
  * registers site with apache (template virtualhost entry to _os_apache_sites_dir/<name>_)
  
### usage

```
# prepare and deploy all sites
ansible-playbook -i inventory/iceburg.hosts application_prepare.yml 


# deploy a specific site
ansible-playbook -i inventory/iceburg.hosts application_prepare.yml --tags=deploy --extra-vars=apache_sites_site=www.iceburg.net
```