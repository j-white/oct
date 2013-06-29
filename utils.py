from fabric.api import env
from paramiko import Transport
from socket import getdefaulttimeout, setdefaulttimeout

def if_host_offline_ignore(fn):
    def wrapped():
        original_timeout = getdefaulttimeout()
        setdefaulttimeout(3)
        try:
            Transport((env.host, int(env.port)))
            return fn()
        except:
            print "The following host appears to be offline: " + env.host
        setdefaulttimeout(original_timeout)
    return wrapped

