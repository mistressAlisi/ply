import uuid
import requests
from django.http import JsonResponse

from ply.toolkit import logger as plylog
#queue = GalleryPublisher(ply.settings.PLY_MSG_BROKER_URL,log)
from communities.stream.models import StreamXMPPSettings, StreamProfileXMPPSettings,StreamProfileXMPPMUCs
log = plylog.getLogger('EjabberAPICtl',name='ejabberapictl.api_views')

class RESTAPIClient:
    settings = False
    def __init__(self,community):
        self.settings =  StreamXMPPSettings.objects.get(community=community)

    def _send(self,url,data):
        r = requests.get(f"{self.settings.endpoint}{url}",data)
        if r.status_code != 200:
            log.error(f"Unable to POST to URL: {self.settings.endpoint}{url} - Status: {r.status_code}, Data: {r.text}")
            print(data)
            return False,r
        return True,r.text


    def register_jid(self,uid,domain,password):
        jid = f"{uid}@{domain}"
        if len(StreamProfileXMPPSettings.objects.filter(jid=jid)) > 0:
            return False
        # Go request JID creation:
        success,data = self._send("register",{"user":uid,"host":domain,"password":password})
        if not success:
            raise Exception(f"Unable to Register JID {jid}: {data.text}")
        return True


    def register_muc(self,name,host,service):
        if len(StreamProfileXMPPMUCs.objects.filter(name=name,host=host,service=service)) > 0:
            return False
        success,data = self._send("create_room",{"name":name,"host":host,"service":f"{service}.{host}"})
        if not success:
            raise Exception(f"Unable to Register MUC {name}@{service} in host {host}: {data.text}")
        return True

    def update_password(self,uid,domain,password):
        jid = f"{uid}@{domain}"
        if len(StreamProfileXMPPSettings.objects.filter(jid=jid)) < 1:
            return False
        # Go request JID creation:
        success,data = self._send("change_password",{"user":uid,"host":domain,"newpass":password})
        if not success:
            raise Exception(f"Unable to Update JID {jid}: PW")
        return True


