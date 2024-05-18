from communities.community.models import VHost
from ply.toolkit.logger import getLogger
import logging
# get_vhost_community: Find the right community node for the given Vhost.
# To match VHosts, we must at least match the host name, and optionally, the iapddr.
# 
vhost_logger = getLogger('toolkit.vhosts',name='toolkit.vhosts')
#print(vhost_logger)
#vhost_logger = logging.getLogger('vhosts')
def get_vhost_community(hostname, ipaddr=None):
    try:
        if (ipaddr):
            host = VHost.objects.get(hostname=hostname,ipaddr=ipaddr,archived=False,frozen=False,blocked=False)
        else:
            host = VHost.objects.get(hostname=hostname,archived=False,frozen=False,blocked=False)
        return host.community
    except VHost.DoesNotExist as e:
        logging.error(f"VHost '{hostname}' (IP: {ipaddr}): not found.");
        return None


def get_vhost_and_community(request, ipaddr=None):
    try:
        if (ipaddr):
            host = VHost.objects.get(hostname=request.META["HTTP_HOST"], ipaddr=ipaddr, archived=False, frozen=False, blocked=False)
        else:
            host = VHost.objects.get(hostname=request.META["HTTP_HOST"], archived=False, frozen=False, blocked=False)
        print(request.META["HTTP_HOST"],host)
        return host,host.community
    except VHost.DoesNotExist as e:
        host = request.META["HTTP_HOST"]
        logging.error(f"VHost '{host}' (IP: {ipaddr}): not found.");
        return None

