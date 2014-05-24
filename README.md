ansible-pcd
===========

ansible prepare, configure, deploy framework


overview
========

* ansible-pcd provides conventions to help encourage reusable automation components (e.g. roles).

* roles are categorized into systems, services, and applications.
  * suitable for massive installs

* pcd roles organize tasks into prepare, configure, and deploy tags. 
  * prepare: typically run one time per host (e.g. create user)
  * configure: run whenever configuration changes (e.g. update httpd port)
  * deploy: run on site/application releases 
  
#### goals
* drastically reduce execution time by visiting only necessary tasks
* provide standards for shared tasks and intralinked roles
* support multiple distributions (Debian, RedHat, &c)
* remain simple, intuitive, and community friendly
* avoid redundancy, be maintainable

#### current functionality

ansible-pcd currently provides an ansible-managed "webhost in a box"

* YAML website definitions - see [sites/](https://github.com/iceburg-net/ansible-pcd/tree/master/sites)
  * apache and nginx server options
  * git based sites (shallow clone during deployment), multiple branch support.
  * conveniences for;
    * mysql user + database creation
    * awstats integration
    * wordpress/silverstripe/&c rewrites
    * backups (e.g. asset/upload folder(s) > cloud storage)  
* nullmailer MTA replacement
* remote/cloud backups via s3ql

more to come, please contribute!

setup
=====

* ensure ansible 1.6+

```
cp -a private.sample private
```

* remove /private from .gitignore if you want to check-in private keys, etc.
  * you can use the vault module to encrypt files in /private
  
* configure accordingly
  * inventory vars
  * site.yml
  * iceburg-sites.yml
  

usage
==============

examples

```
# Provision (prepare, configure) hosts listed in inventory/iceburg.hosts
ansible-playbook -i inventory/iceburg.hosts pcd_system.yml

# Reconfigure a specific host/group
ansible-playbook -i inventory/iceburg.hosts pcd_system.yml -t configure -e PCD_TARGET_HOST=iceburg-ocean-1.iceburg.net

##

# Add the nullmailer service to a host/group
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml --extra-vars="PCD_TARGET_HOST=webservers PCD_TARGET_ROLE=nullmailer"

# Reconfigure nullmailer on all hosts
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml -t configure --extra-vars="PCD_TARGET_HOST=all"

##

# Provision (prepare, configure, deploy) all sites
ansible-playbook -i inventory/iceburg.hosts iceburg-sites.yml

# Deploy a specific site to all webservers
ansible-playbook -i inventory/iceburg.hosts pcd_site.yml -t deploy --extra-vars="PCD_TARGET_HOST=webservers"

```

notes
  * use ansible's --limit to further limit selected hosts to a pattern
  * use ansible's --list-tasks to preview the tasks to be executed


more to come


status
======

**development**

ansible-pcd is under development.  there may be breaking api
changes, and I'd like to conform to the standards set by the edX project ( https://github.com/edx/configuration )

Contributions are welcome.


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
- { include: deploy.yml, tags: ['deploy'], sudo: True, sudo_user: "{{ httpd_user }}" }

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
* try to at least support `Debian` and `RedHat` OS families




support
=======

Report issues to the github issue tracker.

* https://github.com/iceburg-net/ansible-pcd/issues


For *support*, please post to stackoverflow using the ansible-pcd tag:

* http://stackoverflow.com/questions/ask?tags=ansible-pcd



developer-todo
==============

#### highest priority

* fix backup to work with rewrite
* mail service => nullmailer service
* ncurses based UI   

#### normal priority

* denyhosts belongs as a service; not part of base system configuration
* standardize logging service across distributions
* add redhat support to awstats (currently assumes debian httpd-prerotate functionality in apache2 logrotate.d conf)
* reach feature parity on RedHat distributions

#### lowest priority

* refactor all roles to adopt edX standards
* improve upon skip_tasks hack; find better way to load role var defaults.
* make awstats apache/nginx agnostic, set inventory preference for nginx|apache


