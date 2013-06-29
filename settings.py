
# User used when interacting with Git and when compiling
DEV_USER = 'jwhite'

# Where the source code is checked out, should be owned by DEV_USER
OPENNMS_SRC = '/home/jwhite/rcs/opennms'

# Hostnames for all of the cluster members
CLUSTER_HOSTS = ['onms-n1', 'onms-n2', 'onms-n3']

# Where OpenNMS lives locally on the cluster members
OPENNMS_HOME = '/opt/opennms'

# Where the shared data is stored
SHARED_HOME = '/mnt/cephfs/opennms'
