from __future__ import with_statement
from fabric.api import env, run, cd, sudo, parallel
from fabric.exceptions import CommandTimeout
from fabric.contrib import files
from utils import if_host_offline_ignore
from settings import DEV_USER, OPENNMS_SRC, BUILD_HOST, CLUSTER_HOSTS, OPENNMS_HOME, SHARED_HOME
import os

# Default to root
env.user = 'root'

# Default to the build host for particular tasks
tasks_to_exec = set(env.tasks)
tasks_for_build_host = set(['build', 'rebuild', 'predeploy', 'install'])
if tasks_for_build_host.intersection(tasks_to_exec):
    env.hosts = [BUILD_HOST]

def cluster():
    env.hosts = CLUSTER_HOSTS

OPENNMS_BIN = OPENNMS_HOME + '/bin'

@parallel
@if_host_offline_ignore
def start():
    # If OpenNMS is not running the script will return a non-zero error code
    env.warn_only = True
    with cd(OPENNMS_BIN):
        run("./opennms start", pty=False) 

@parallel
@if_host_offline_ignore
def stop():
    env.warn_only = True
    with cd(OPENNMS_BIN):
        run("./opennms stop") 

@parallel
@if_host_offline_ignore
def restart():
    env.warn_only = True
    with cd(OPENNMS_BIN):
        run("./opennms restart") 

@parallel
@if_host_offline_ignore
def kill():
    env.warn_only = True
    with cd(OPENNMS_BIN):
        run("./opennms kill") 
        run("""kill -9 `ps ax | grep java | grep opennms | awk '{print $1;}'`""", shell=False)

@if_host_offline_ignore
def status():
    env.warn_only = True
    with cd(OPENNMS_BIN):
        run("./opennms -v status")

@parallel
@if_host_offline_ignore
def reboot():
    run("shutdown -r now")

@parallel
@if_host_offline_ignore
def slap():
    # We're expecting the server to reboot immediately after the command is ran
    # without properly closing the connection
    env.timeout = 2
    env.command_timeout = 2
    try:
        run("echo 1 > /proc/sys/kernel/sysrq  && echo b > /proc/sysrq-trigger", pty=False)
    except CommandTimeout as e:
        pass

def rebuild():
    env.user = DEV_USER
    with cd(OPENNMS_SRC):
        run("git pull")
        run("./clean.pl")
        run("./compile.pl")
        run("./assemble.pl -Dopennms.home=" + OPENNMS_HOME)

def build():
    env.user = DEV_USER
    with cd(OPENNMS_SRC):
        run("git pull")
        run("./compile.pl")
        run("./assemble.pl -Dopennms.home=" + OPENNMS_HOME)

def predeploy():
    with cd(OPENNMS_SRC + "/target"):
        run("rm -rf " + OPENNMS_HOME)
        run("mkdir -p " + OPENNMS_HOME)
        run("tar zxvf opennms-*.tar.gz -C " + OPENNMS_HOME)

    with cd(OPENNMS_HOME):
        run("mv etc etc.pristine")
        run("mv share share.pristine")
        run("ln -sf %s/etc etc" % SHARED_HOME)
        run("ln -sf %s/share share" % SHARED_HOME)
        run("chown -R root:root *")

        if not files.exists("%s/etc" % SHARED_HOME):
            run("cp -R etc.pristine %s/etc" % SHARED_HOME)

        if not files.exists("%s/share" % SHARED_HOME):
            run("cp -R share.pristine %s/share" % SHARED_HOME)

def install():
    with cd(OPENNMS_BIN):
        run("./runjava -s")
        run("./install -dis")

def reload(daemon):
    with cd(OPENNMS_BIN):
        run("./send-event.pl -p 'daemonName %s' uei.opennms.org/internal/reloadDaemonConfig" % daemon)

@parallel
def deploy():
    opennms_home_parent = os.path.abspath(os.path.join(OPENNMS_HOME, '..'))
    run("rsync -avr --delete %s:%s %s" % (BUILD_HOST, OPENNMS_HOME, opennms_home_parent))

