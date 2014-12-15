permissions-data-tools
======================

Tools for checking and verifying permissions data

Dependencies:

apt-get install build-essential python-dev libmysqlclient-dev

apt-get install python-setuptools

easy_install pip

pip install MySQL-python

Note: for osx, MySQL-python needs the following fix-up:

Error:
    import MySQLdb
  File "/usr/local/lib/python2.7/site-packages/MySQLdb/__init__.py", line 19, in <module>
    import _mysql
ImportError: dlopen(/usr/local/lib/python2.7/site-packages/_mysql.so, 2): Library not loaded: libmysqlclient.18.dylib
  Referenced from: /usr/local/lib/python2.7/site-packages/_mysql.so
  Reason: image not found

Fix:

ln -s /path/to/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib

e.g.

ln -s /usr/local//mysql-5.6.22-osx10.8-x86_64/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib

pip install colorama
