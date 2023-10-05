import json
from datetime import datetime
import django
django.setup()

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from actions.models import Action
from actions.serializers import ActionSerializer


class InboxConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("inbox-%s" % self.scope['user'].id, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)("inbox-%s" % self.scope['user'].id, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)("inbox-%s" % self.scope['user'].id, {
            "type": "chat.message",
            "text": json.loads(text_data)
        })

    def chat_message(self, event):
        print(event)
        message = event['text']

        ##
        #
        # refresh,act
        #
        ##

        if(message['action'] == 'refresh'):
            user = get_user_model().objects.get(email=self.scope['user'])
            uncompleted_actions = Action.objects.filter(owner=user, completed=False)
            self.send(text_data=json.dumps({'action': 'refresh', 'data': ActionSerializer(instance=uncompleted_actions, many=True).data, 'asof': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}))

        # Send message to WebSocket
        else:
            self.send(text_data=json.dumps({
                'text': "cla: %s, grp: %s" % (self.channel_layer_alias, self.groups)
            }))
