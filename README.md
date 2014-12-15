Broken DNS Proxy
================

Some tools like Unbound, BIND, dnssec-trigger, Free-IPA, rely on the DNSSEC support of remote DNS resolver, when using it as forwarder. Some tools are intended to detect and assess the level of DNSSEC support of such remote DNS resolver. There are many issues that can arise. Some of them are specified in the [**IETF draft**](http://www.ietf.org/id/draft-ietf-dnsop-dnssec-roadblock-avoidance-01.txt), some are based on real life issues and errors in specific implementations of DNS resolvers (e.g. wildcard NSEC issue in old versions of BIND).

Purpose of this project is to implement simple, extensible and easy to use DNS proxy for simulating such issues.
Simple DNS proxy for simulating various DNS issues

[![Code Health](https://landscape.io/github/thozza/broken-dns-proxy/master/landscape.svg)](https://landscape.io/github/thozza/broken-dns-proxy/master)
