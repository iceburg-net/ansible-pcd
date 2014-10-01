Varnish
=======


Varnish is a frontend caching proxy. It sits in front of your "backend" 
webservers, such as Apache, and serves cachable content directly from RAM.

Processing is handled through VCL files which compile into C for lighting-fast
responses. 

A few use-cases;

  + Load balance between multiple backends
  + Gracefully respond with stale content when backend servers are unreachable
  + Speedup Apache's static asset handling (e.g. quickly serve image, css, and js)
  + Pre-process and transform requests
    - use as a security firewall; https://github.com/comotion/VSF
  
  
Websockets are supported out of box.

For site-specific configuration, add your template to templates/sites 
and re-configure the varnish role on your server(s). 

See templates/sites/www.example.com.vcl.j2 as an example.

By default, our varnish listens on port 8080 and expects backends to respond
on port 80. This allows you to test varnish on :8080 before commiting
it to handle your production traffic. 

To configure varnish to sit in front of Apache/NginX, set the following 
inventory variables;

  + VARNISH_PORT: 80
  + VARNISH_HTTPD_PORT: 81
  + HTTPD_HTTP_PORT: 81
  
Then re-configure the apache-service, virtualhosts, and varnish. E.g. 

```

# reconfigure apache
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml --extra-vars="PCD_TARGET_HOST=webservers PCD_TARGET_ROLE=apache" --tags=configure


# update virtualhosts
ansible-playbook -i inventory/iceburg.hosts iceburg-sites.yml --tags=configure


# reconfigure varnish
ansible-playbook -i inventory/iceburg.hosts pcd_service.yml --extra-vars="PCD_TARGET_HOST=webservers PCD_TARGET_ROLE=varnish" --tags=configure

```

To handle server-side logging you may consider disabling apache access logs via APACHE_ENABLE_ACCESS_LOGS, 
and setting your sites to use SITE_LOG_FILE: "{{ HTTPD_LOG_DIR }}/access/varnish.log". After re-configuring
your sites the AWStats will look at the varnish.log file.

See the defaults/main.yml for more configuration options.

