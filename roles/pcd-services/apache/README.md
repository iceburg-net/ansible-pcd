apache
######

the webserver we all love for .htaccess commodity chaos

ansible-pcd provides a stripped down apache version that bypasses
the distribution's management of modules and sites.

by default there are no default sites or mod_cgi 

configure httpd.conf directives and virtualhosts through the
ansible-pcd conf.d metadir (/etc/ansible/conf.d/apache/)


select modules with inventory variables... choose sparingly;
keep concurrent visitors from trampling your RAM sandwich!
