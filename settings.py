
# User used when interacting with Git and when compiling
DEV_USER = 'jwhite'

# Where the source code is checked out, should be owned by DEV_USER
OPENNMS_SRC = '/home/jwhite/rcs/opennms'

# Hostname for the build server
BUILD_HOST = 'cyclone'

# Hostnames for all of the cluster members
CLUSTER_HOSTS = ['cyclone', 'n1', 'n2']

# Where OpenNMS lives locally on the cluster members
OPENNMS_HOME = '/opt/opennms'

# Where the shared data is stored
SHARED_HOME = '/mnt/nfs/opennms'
