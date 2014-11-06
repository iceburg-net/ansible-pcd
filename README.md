ansible-pcd
===========

ansible-pcd provides [ansible](https://github.com/ansible/ansible) roles and
structural conventions to easily automate (even massive) *nix infrastructure.

roles are organized by _system_, _service_, or _application_ and tasks are
tagged as either `prepare`, `configure`, or `deploy`. this is scalable and
drastically reduces execution time by visiting only intended tasks.

the project has the following **goals**;
* remain distribution agnostic (support Debian, RedHat, &c out-of-box)
* encourage reusable automation components, avoid redundancy
* embrace ansible-best-practices -- remain understandable and community friendly


See the [ginas](https://github.com/ginas/ginas/) project as an alternative.


quick start
===========

* ensure ansible 1.6+
* clone or download ansible pcd to a directory (now known as _PCDROOT_)
* create your private directory (which holds keys & passwords)
  ```
  cp -a /PCDROOT/private.sample /PCDROOT/private
  ```
  * you may define an alternative location of the private directory by overriding the _PCD_PRIVATE_DIR_ inventory variable.
  * remove /private from /PCDROOT/.gitignore if you want to check-in private keys & passwords.
    * you may use the [vault](http://docs.ansible.com/playbooks_vault.html) to encrypt files
* create your host inventory, use [/PCDROOT/inventory/iceburg.hosts](https://github.com/iceburg-net/ansible-pcd/blob/master/inventory/iceburg.hosts) as a _reference_
* configure your private directory, set passwords, ssl certs, and add ssh keys for connecting to hosts
  ```
  ssh-keygen -t rsa -f /PCDROOT/private/keys/ENV+root.key
  ```
  * see /PCDROOT/private.sample/vars files as _reference_
* configure hosts using inventory variables
  * see /PCDROOT/inventory/group_vars files and /PCDROOT/inventory/host_vars files as _reference_
  * PCD roles provide overridable defaults - visit the roles to get an idea of what you can configure. 
* modify /PCDROOT/site.yml to your needs and execute
  ```
  ansible-playbook -i inventory/my.hosts site.yml
  ````
  * use the --ask-pass flag to connect to hosts that have not yet been provisioned via the pcd_system role.

  
usage
==============

The pcd_*.yml playbooks are used to apply a single role to specified host(s). They
are executed via `ansible-playbook`, and you pass paramaters to indicate the
desired role, tasks, and target hosts to execute upon. 

For example, you can use the [pcd_service.yml](https://github.com/iceburg-net/ansible-pcd/blob/master/pcd_service.yml)
playbook to quickly provision mysql on all hosts in the dbservers group via `ansible-playbook -i inventory/iceburg.hosts pcd_service.yml --limit=dbservers -e PCD_ROLE=mysql`


Running the pcd_*.yml playbooks without tags will execute all tasks. 
As such, the above example will execute `prepare`, `configure`, and `deploy` tasks in that order.
* `prepare` tasks are ideally run once per host. They install packages, add users, create directories, &c.
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

# provision all hosts in your inventory file
ansible-playbook -i inventory/iceburg.hosts pcd_system.yml 


# reconfigure the apache service on a specific host
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml -t configure -l ocean-1.iceburg.net -e PCD_ROLE=apache"


# apply a site to all webservers (you will be prompted for site name and org if not passed)
ansible-playbook -i inventory/iceburg.hosts pcd_site.yml -l webservers


# deploy (in this case; git checkout) www.iceburg.net to ocean-1.iceburg.net
ansible-playbook -i inventory/iceburg.hosts pcd_site.yml -t deploy -l ocean-1.iceburg.net --extra-vars="PCD_SITE_NAME=www.iceburg.net PCD_SITE_ORG=iceburg"

```

#### connecting, initial provisioning

The [pcd-systems](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-systems
roles provision hosts with a consistent environment. They ensure the 
root user's authorized keys for ansible to connect, set the fqdn properly, 
install a common set of packages, and tighten security. 


_When connecting to a host for the first time (that doesn't yet have an authorized key for the root 
user), pass the --ask-pass flag to ansible-playbook._


By default, ansible-pcd connects to hosts as the root user using ssh keys
from the /PCDROOT/private/keys directory. The **ansible_ssh_private_key_file** inventory 
variable determines the key used, and defaults to
`{{ PCD_KEYS_DIR }}/{{ PCD_DEFAULT_ORG }}+{{ ansible_ssh_user }}.key`.


For instance, if we're connecting to a host belonging to the *chicago-east*
organization, ansible would select `<pcd-root>/private/keys/chicago-east+root.key`. 
Again, all this is configured via [inventory variables](https://github.com/iceburg-net/ansible-pcd/tree/master/inventory). 



status
======

**development**

ansible-pcd is under development. there may be breaking api changes in the near future. 

#### current functionality

at this time ansible-pcd provides a "webhost in a box"

[hosts](https://github.com/iceburg-net/ansible-pcd/blob/master/inventory/iceburg.hosts) are provisioned with a consistent, secure environment. [services](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-services) are
configurable [per host](https://github.com/iceburg-net/ansible-pcd/blob/master/webservers.yml) using playbooks and inventory.


[websites](https://github.com/iceburg-net/ansible-pcd/tree/master/sites) are defined in YAML
with built-in, real-world conveniences;
* git based sites (deployment via shallow checkout)
* [wordpress/silverstripe/&c rewrites](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-sites/apache_site/templates/includes)
* pcd.mysql integration (create user + database)
* pcd.awstats integration (registers logfile to be analyzed) 
* pcd.backup integration (site assets/uploads > clound storage via s3ql)  


_Also featured are useful infrastructure roles for monitoring, remote filesystems, varnish caching, and VPN connectivity._

more to come, please contribute!


contributing
============

ansible-pcd is licensed under the GPLv3 , the same as ansible.

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

* If a variable is a good candidate to be shared by other roles, place it in [pcd-common/defaults/main.yml](https://github.com/iceburg-net/ansible-pcd/blob/master/roles/pcd-common/defaults/main.yml). If it is distribution/OS specific, place appropriate values in [pcd-common/vars](https://github.com/iceburg-net/ansible-pcd/tree/master/roles/pcd-common/vars).

* Follow the [edX project](https://github.com/edx/configuration) standard and CAPITALIZE the names of variables likely to be overriden/configured by users. Place them at the top of your defaults/main.yml.

* Please support both `Debian` and `RedHat` OS families



support
=======

Report issues to the github issue tracker.

* https://github.com/iceburg-net/ansible-pcd/issues


For *support*, please post to stackoverflow using the ansible-pcd tag:

* http://stackoverflow.com/questions/ask?tags=ansible-pcd



developer-todo
==============

* ncurses based UI for applying roles
* map system uuid => fqdn to more easily identify remote backups
* make awstats apache/nginx agnostic, set inventory preference for nginx|apache
* iptables role to compliment pptpd and openvpn [ferm!]
