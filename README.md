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


See the [ginas)(https://github.com/ginas/ginas/) project as an alternative.


#### current functionality

at this time ansible-pcd provides a "webhost in a box" for **debian 7 (wheezy)**

websites are defined in YAML (see [sites/](https://github.com/iceburg-net/ansible-pcd/tree/master/sites)).
the following conveniences are provided;
* git based sites (shallow checkout during deployment)
* toggle user + database creation
* toggle awstats integration
* wordpress/silverstripe/&c rewrites
* backups (e.g. asset/upload folder(s) > cloud storage)  

hosts are provisioned with a consistent, secure environment. [services](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-services) are
configured with playbooks and inventory
* remote/cloud backups via s3ql
* nullmailer MTA
* LAMP stack 

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

by default, ansible-pcd connects to hosts as the root user over ssh using keys
in the /private/keys directory. the key is determined by the 
**ansible_ssh_private_key_file** inventory variable and defaults to
`{{ PCD_KEYS_DIR }}/{{ PCD_DEFAULT_ORG }}+{{ ansible_ssh_user }}.key`. for
instance, if we're connecting to a host in the *chicago-east*
organization/environment, ansible would select
`/private/keys/chicago-east+root.key`. 

pcd-systems roles provision hosts with a consistent environment. they ensure the 
root user's authorized keys for ansible to connect, set the fqdn properly, 
install a common set of packages, and tighten security. when connecting to a 
host for the first time (that doesn't yet have an authorized key for the root 
user), pass the --ask-pass flag to ansible-playbook.

@todo tutorial on running site.yml


examples

```
# Reconfigure a specific host/group
ansible-playbook -i inventory/iceburg.hosts pcd_system.yml -t configure -e PCD_TARGET_HOST=iceburg-ocean-1.iceburg.net

##

# Add the nullmailer service to a host/group
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml --extra-vars="PCD_TARGET_HOST=webservers PCD_TARGET_ROLE=nullmailer"

# Reconfigure nullmailer on all hosts
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml -t configure --extra-vars="PCD_TARGET_HOST=all"

##

# Deploy a specific site to all webservers
ansible-playbook -i inventory/iceburg.hosts pcd_site.yml -t deploy --extra-vars="PCD_TARGET_HOST=webservers"

```

notes
  * use ansible's --limit to further limit selected hosts to a pattern
  * use ansible's --list-tasks to preview the tasks to be executed



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

* mail service => nullmailer service
* denyhosts belongs as a service; not part of base system configuration
* reach feature parity on RedHat distributions
* ncurses based UI   

#### normal priority

* standardize logging service across distributions
* map system uuid => fqdn to more easily identify remote backups
* add redhat support to awstats (currently assumes debian httpd-prerotate functionality in apache2 logrotate.d conf)

#### lowest priority

* refactor all roles to adopt edX standards
* improve upon skip_tasks hack; find better way to load role var defaults.
* make awstats apache/nginx agnostic, set inventory preference for nginx|apache


