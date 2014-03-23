ansible-pcd
===========

ansible provision, configure, deploy framework


overview
========


automation of applications, services, and systems broken down into 
prepare, configure, and deploy steps. 

this approach reduces execution times nof playbooks... 
especially when compared to monolithic playbooks that execute 
everything every time on all hosts. 

organization is defined as;

* **applications** > application code (e.g. your github project), can be prepared and deployed
* **services** > third party services (e.g. apache, elasticsearch, &c), can be prepared and configured
* **systems** > remote hosts (e.g. your VMs in EC2), can be prepared and configured


steps/playbooks defined as;

* **prepare** > run once/rarely (e.g. creates application users, hardens operating system). consider "provisioning"
* **configure** > run often during setup/changes (e.g. update httpd.conf and restart apache). consider "syncing"
* **deploy** run continuously (e.g. triggered by jenkins). consider "continuous integration"


fwiw; ansible supports tags as an effective strategy to limit behavior.
organizing playbooks in steps + tagging is my preferred route, a la ansible-pcd.


setup
=====

* ensure ansible 1.4+

```
cp -a private.sample private
cp -a inventory.sample inventory
```


usage
=====

```
# Prepare all hosts listed in inventory/digome.hosts
ansible-playbook -i inventory/digome.hosts systems/prepare.yml

# Prepare the specified host/group (passed via-limit)
ansible-playbook -i inventory/digome.hosts systems/prepare.yml --limit digome-ocean-1.iceburg.net
```


... work in progress