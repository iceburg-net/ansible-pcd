apache
######

the webserver we all love for .htaccess commodity chaos

ansible-pcd provides a stripped down apache version that bypasses
the distribution's management of modules and sites.

by default there are no default sites or mod_cgi 

configure httpd.conf directives through /etc/ansible/conf.d/apache/
overrides, and select modules with inventory variables...
and we recommend you choose sparingly;
keep concurrent visitors from trampling your RAM sandwich. 
