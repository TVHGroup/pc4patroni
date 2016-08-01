pc4patroni
==========
Proxy configurator for [Patroni](https://github.com/zalando/patroni) managed [PostgreSQL](http://www.postgresql.org/) clusters.


About
-----
PC4Patroni is deprecated, it is no longer needed now that Patroni has confd configuration samples included. 

Pc4Patroni is a simple python script that continuously monitors the configuration of a Patroni managed PostgreSQL cluster and when the master or slaves change it updates the configuration files of your database proxy. Currently it only supports clusters that store their information in [Etcd](https://github.com/coreos/etcd). 

The proxy comes with a sample configuration file for [PgBouncer](https://pgbouncer.github.io). Writing a configuration file for other proxies like [HAProxy](http://www.haproxy.org/) should be straightforward for someone familiar with the chosen solution. It is designed with the intent to be generic enough to support any proxy without coding changes. 

Requirements
------------
* The following python modules, that can be installed with pip: patroni, jinja2, pyaml
* It is only tested with python 2.7

Installation
------------
Installation is currently manual. I copy everything to /opt, copy the config file from `extras/settings.yml` to `/etc/pc4patroni/settings.yml`, the configuration template `extras/pgbouncer.j2` to `/etc/pgbouncer/pcbouncer.j2` .


If your systems uses systemd, you could copy extras/pc4patroni.service to /etc/systemd/system/pc4patroni.service . 
Next use `sudo systemctl daemon-reload` to load this config and `sudo systemctl start pc4patroni` to start it. 
Otherwise, the way to start it is something like `/usr/bin/python /opt/pc4patroni/pc4patrony.py /etc/pc4patroni/settings.yml` .

You will probably need to change the sample configurations (the files in the extras folder) to meet your needs. 

Configuration
-------------
Please look at the sample configuration file in `extras/settings.yml`, it contains comments that explain all options.


Things you should know
----------------------
* pc4patroni does not start the pgbouncer with the included configuration and does not include anything to check if your proxy is running, it only updates the configuration and upon a configuration change it triggers a command of your choice (typically the proxy's reload config command.)
* No attempt is made to parse existing proxy configuration, if the configuration is changed externally pc4patroni will not notice.
* The configurations are always written out and a configuration reload is triggered immediately after restart, even if the proxies configuration was already correct.
* The script is designed to run under the same user as the proxy. 
* The scripts polls the configuration (currently form Etcd), so there may be a slight delay (a few seconds) between a failover and a configuration reload. 

License
-------
We have chosen to stick with the license Patroni uses for simplicity: the MIT License. 
