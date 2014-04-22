#!/bin/sh

#sudo -u {{ apache_sites_user }} {{ awstats_site_dir }}/awstats_updateall.pl now
{% if cronic_cron %}cronic {% endif %}{{ awstats_site_dir }}/awstats_updateall.pl now