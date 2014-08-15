ansible-pcd
===========

ansible-pcd provides [ansible](https://github.com/ansible/ansible) roles and
structural conventions to easily automate (even massive) *nix infrastructure.

roles are organized by _system_, _service_, or _application_ and tasks are
tagged with either `prepare`, `configure`, or `deploy`. this is scalable and
drastically reduces execution time by visiting only necessary tasks.

the project has the following **goals**;
* embrace ansible-best-practices -- remain understandable and community friendly
* distribution agnostic approach (support Debian, RedHat, &c)
* encourage reusable automation components, avoid redundancy


See the [ginas](https://github.com/ginas/ginas/) project as an alternative.


  
usage
==============

The pcd_*.yml playbooks are used to apply a single role to specified host(s). 
They will prompt for the role/host if not provided via --extra-vars on the command line.


For instance, you can use the [pcd_service.yml](https://github.com/iceburg-net/ansible-pcd/blob/master/pcd_service.yml)
playbook to quickly apply mysql to a host via `ansible-playbook -i inventory/iceburg.hosts pcd_service.yml --extra-vars="PCD_TARGET_HOST=chi-db-1.iceburg.net PCD_TARGET_ROLE=mysql"`


Running the pcd_*.yml playbooks without tags will execute all tasks. 
Thus, the above example executes `prepare`, `configure`, and `deploy` tasks in that order.
* `prepare` tasks are ideally run once per host. They install packages, add users, &c.
* `configure` tasks are run more often. They setup cron jobs, template configuration files, set timezone, &c. 
* `deploy` tasks are run most often, and limited to [applications](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-apps) and [sites](https://github.com/iceburg-net/ansible-pcd/tree/master/sites). Run to deploy code changes. 


Many pcd roles provide [default configuration variables](https://github.com/iceburg-net/ansible-pcd/blob/master/roles/pcd-apps/awstats/defaults/main.yml) meant to be overriden. These are typically UPPERCASED. Configure to your liking by redefining them in your [inventory variables](https://github.com/iceburg-net/ansible-pcd/tree/master/inventory/group_vars).


It's best to define your own infrastructure and the applications/services that
run on it. You do this through standard ansible playbooks. Included is an 
example that provisions an entire environemnt and deploys websites. See:
  * [site.yml](https://github.com/iceburg-net/ansible-pcd/blob/master/site.yml) 
  * [webservers.yml](https://github.com/iceburg-net/ansible-pcd/blob/master/webservers.yml)
  * [iceburg-sites.yml](https://github.com/iceburg-net/ansible-pcd/blob/master/iceburg-sites.yml)
  

#### examples

```
# apply a service to host(s) (you will be prompted for service and host name)
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml

# reconfigure the apache service on a specific host
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml -t configure --extra-vars="PCD_TARGET_HOST=iceburg-ocean-1.iceburg.net PCD_TARGET_ROLE=apache"

##

# provision a host with a consistent environment (you will be prompted for host)
ansible-playbook -i inventory/iceburg.hosts pcd_system.yml 

# reconfigure the environment on all hosts in the webservers group
ansible-playbook -i inventory/iceburg.hosts pcd_system.yml -t configure --extra-vars="PCD_TARGET_HOST=webservers"

##

# apply a site to host(s) (you will be prompted for host, site, and site org)
ansible-playbook -i inventory/iceburg.hosts pcd_site.yml

# deploy (in this case; git checkout) www.iceburg.net to all webservers
ansible-playbook -i inventory/iceburg.hosts pcd_site.yml -t deploy --extra-vars="PCD_TARGET_HOST=webservers PCD_TARGET_SITE_NAME=www.iceburg.net PCD_TARGET_SITE_ORG=iceburg"

```

notes
  * use ansible's --limit to further limit selected hosts to a pattern
  * use ansible's --list-tasks to preview the tasks to be executed



setup
=====

* ensure ansible 1.6+

```
cp -a private.sample private
```

* remove /private from .gitignore if you want to check-in private keys, etc.
  * you can use the vault module to encrypt files in /private
  * you can define the private directory location via the _PCD_PRIVATE_DIR_ inventory variable.

* configure inventory and vars accordingly


#### connecting, initial provisioning

pcd-systems roles provision hosts with a consistent environment. they ensure the 
root user's authorized keys for ansible to connect, set the fqdn properly, 
install a common set of packages, and tighten security. when connecting to a 
host for the first time (that doesn't yet have an authorized key for the root 
user), pass the --ask-pass flag to ansible-playbook.

by default, ansible-pcd connects to hosts as the root user over ssh using keys
in the /private/keys directory. the key is determined by the 
**ansible_ssh_private_key_file** inventory variable and defaults to
`{{ PCD_KEYS_DIR }}/{{ PCD_DEFAULT_ORG }}+{{ ansible_ssh_user }}.key`. for
instance, if we're connecting to a host in the *chicago-east*
organization/environment, ansible would select
`/private/keys/chicago-east+root.key`. 



status
======

**development**

ansible-pcd is under development. there may be breaking api changes in the near future. 

#### current functionality

at this time ansible-pcd provides a "webhost in a box" for **debian 7 (wheezy)**

[hosts](https://github.com/iceburg-net/ansible-pcd/blob/master/inventory/iceburg.hosts) are provisioned with a consistent, secure environment. [services](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-services) are
configurable [per host](https://github.com/iceburg-net/ansible-pcd/blob/master/webservers.yml) using playbooks and inventory.


[websites](https://github.com/iceburg-net/ansible-pcd/tree/master/sites) are defined in YAML
with built-in, real-world conveniences;
* git based sites (deployment via shallow checkout)
* [wordpress/silverstripe/&c rewrites](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-sites/apache_site/templates/includes)
* pcd.mysql integration (create user + database)
* pcd.awstats integration (registers logfile to be analyzed) 
* pcd.backup integration (site assets/uploads > clound storage via s3ql)  


more to come, please contribute!



contributing
============

ansible-pcd is licensed under the GPLv3 , the same as ansible.

Please feel free to contribute roles and fixes via github pull requests.

#### conventions

* role tasks must be tagged as either prepare, configure, or deploy. to reduce redundancy and add convenience, tasks are typically separated into tagged includes. 
```
# example pcd-role/tasks/main.yml

- { include: prepare.yml, tags: ['prepare'] }
- { include: configure.yml, tags: ['configure'] }
- { include: deploy.yml, tags: ['deploy'], sudo: True, sudo_user: "{{ HTTPD_USER }}" }

# example pcd-role/tasks/prepare.yml

- debug: msg="I am executed when the `prepare` tag is passed."
```

* shared tasks (e.g. adduser) are registered via the pcd-common role. prefix shared tasks with `pcd_task`, provide usage example in task file.
```
# excerpt from pcd-common/vars/main.yml

pcd_task_add_apache_site: "{{ PCD_TASKS }}/add_apache_site.yml"
pcd_task_add_s3ql_mount: "{{ PCD_TASKS }}/add_s3ql_mount.yml"
pcd_task_add_user: "{{ PCD_TASKS }}/add_user.yml"

```

* If a variable is a good candidate to be shared by other roles, place it in [pcd-common/vars/shared.yml](http://LINK).

* Follow the [edX project](https://github.com/edx/configuration) standard and CAPITALIZE the names of variables likely to be overriden/configured by users. Place them at the top of your defaults/main.yml.

* try to at least support `Debian` and `RedHat` OS families



support
=======

Report issues to the github issue tracker.

* https://github.com/iceburg-net/ansible-pcd/issues


For *support*, please post to stackoverflow using the ansible-pcd tag:

* http://stackoverflow.com/questions/ask?tags=ansible-pcd



developer-todo
==============

* reach feature parity on RedHat distributions
* ncurses based UI   
* map system uuid => fqdn to more easily identify remote backups
* add redhat support to awstats (currently assumes debian httpd-prerotate functionality in apache2 logrotate.d conf)
* make awstats apache/nginx agnostic, set inventory preference for nginx|apache
