apache
======

the endearing webserver that brought us the .htaccess chaos we can't live without!

ansible-pcd provides your distribution's apache package, but strips
it down and handles the management of modules and sites.

configure httpd.conf directives and virtualhosts through the
ansible-pcd conf.d metadir (/etc/ansible/conf.d/apache/)

select modules with inventory variables... choose sparingly;
keep concurrent visitors from trampling your RAM sandwich!

by default there are no default sites or mod_cgi

