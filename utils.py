from fabric.api import env
from paramiko import Transport
from socket import getdefaulttimeout, setdefaulttimeout
from settings import BUILD_HOST

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

def only_run_on_build_server(fn):
    def wrapped():
        if env.host != BUILD_HOST:
            print "Skipping %s on %s" % (env.command, env.host)
            return
        return fn()
    return wrapped

def skip_on_build_server(fn):
    def wrapped():
        if env.host == BUILD_HOST:
            print "Skipping %s on %s" % (env.command, env.host)
            return
        return fn()
    return wrapped
