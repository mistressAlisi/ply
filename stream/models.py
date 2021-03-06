import uuid
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

#PLY:
from community.models import Community
from profiles.models import Profile
from keywords.models import Keyword
from group.models import Group
#from dynapages.models import Page

# Create your models here.
# Stream Index Table:
class Stream(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Stream Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True)
    profile = models.ForeignKey(Profile,verbose_name = "Profile",on_delete=models.RESTRICT,null=True)
    group = models.ForeignKey(Group,verbose_name = "Group",on_delete=models.RESTRICT,null=True)
    type = models.TextField(verbose_name='Stream Type')
    default_perm = models.TextField(verbose_name='Stream Default Permission',default="e")
    icon = models.TextField(verbose_name='Stream Icon',blank=True,null=True)
    shares = models.IntegerField(verbose_name='Share Count',default=0)
    views = models.IntegerField(verbose_name='Views Count',default=0)
    nodes = models.IntegerField(verbose_name='Node Count',default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    opened = models.BooleanField(verbose_name="Stream FLAG: has been Opened",default=False)
    root_stream = models.BooleanField(verbose_name="Root Stream FLAG",default=False)
    bkg1 = models.TextField(verbose_name='Stream Bkg Colour #1',default="#ffffff")
    bkg2 = models.TextField(verbose_name='Stream Bkg Colour #2',default="#ffffff")
    bkgt = models.TextField(verbose_name='Stream Bkg Type',default="s1")
    opacity1 = models.DecimalField(verbose_name='Stream Bkg Opacity #1',default=0,decimal_places=3,max_digits=5)
    opacity2 = models.DecimalField(verbose_name='Stream Bkg Opacity #2',default=0,decimal_places=3,max_digits=5)
    midpoint = models.IntegerField(verbose_name='Stream Bkg Midpoint ',default=50)
    midpoint = models.IntegerField(verbose_name='Stream Bkg Midpoint ',default=50)
    angle = models.IntegerField(verbose_name='Stream Bkg Midpoint ',default=90)
    
    def rgba1(self):
        
        return f"rgba({int(self.bkg1[1:3],16)},{int(self.bkg1[3:5],16)},{int(self.bkg1[5:7],16)},{self.opacity1})"
    
    def rgba2(self):
        return f"rgba({int(self.bkg2[1:3],16)},{int(self.bkg2[3:5],16)},{int(self.bkg2[5:7],16)},{self.opacity1})"
    
    def __str__(self):
        return f"Stream for Profile: {self.profile} in community: {self.community} attached to group: {self.group} root stream: {self.root_stream}"
    
@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    pass

# Stream Suscriber Table:
class StreamSubscriber(models.Model):
    stream = models.ForeignKey(Stream,verbose_name="Notification",on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Profile,verbose_name = "Subscriber Profile",on_delete=models.RESTRICT,related_name='+')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Notification Inbox Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    last_view = models.DateTimeField(verbose_name="Last Viewed",null=True,auto_now_add=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    system = models.BooleanField(verbose_name="System FLAG",default=False)
    def __str__(self):
        return f"StreamSubscriber {self.subscriber.uuid} -follows stream -> {self.stream.uuid} in community: {self.community.uuid}"
    
@admin.register(StreamSubscriber)
class StreamSubscriberAdmin(admin.ModelAdmin):
    pass


# Stream Messages Table:
class StreamMessage(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Stream Created')
    stream = models.ForeignKey(Stream,verbose_name="Stream",on_delete=models.CASCADE)
    author = models.ForeignKey(Profile,verbose_name = "Author",on_delete=models.RESTRICT)
    type = models.TextField(verbose_name='Message Type')
    icon = models.TextField(verbose_name='Message Icon',blank=True,null=True)
    reposts = models.IntegerField(verbose_name='Reposts Count',default=0)
    replies = models.IntegerField(verbose_name='Replies Count',default=0)
    shares = models.IntegerField(verbose_name='Share Count',default=0)
    likes = models.IntegerField(verbose_name='Like Count',default=0)
    threads = models.IntegerField(verbose_name='Thread Count',default=0)
    views = models.IntegerField(verbose_name='Views Count',default=0)
    contents_text = models.TextField(verbose_name='Stream Content: Text Type',blank=True,null=True,max_length=500)
    contents_text_parsed = models.TextField(verbose_name='Stream Content: Text Type (Parsed)',blank=True,null=True)
    contents_json = models.JSONField(verbose_name='Stream Content: JSON Type',blank=True,null=True)
    contents_bin = models.BinaryField(verbose_name='Stream Content: Binary Type',blank=True,null=True)
    references = models.ForeignKey('StreamMessage',verbose_name = "References",on_delete=models.CASCADE,null=True,blank=True)
    posted_in = models.ForeignKey('Stream',verbose_name = "Posted in Stream",on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    def __str__(self):
        return f"Stream Message: {self.uuid} -in stream-> {self.stream.uuid} in community: {self.stream.community.uuid} TYPE: {self.type}"
    
@admin.register(StreamMessage)
class StreamMessageAdmin(admin.ModelAdmin):
    pass



class StreamMessageKeywords(models.Model):
    stream = models.ForeignKey(Stream,verbose_name="Stream",on_delete=models.CASCADE)
    message = models.ForeignKey(StreamMessage,verbose_name="Message",on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword,verbose_name="Keyword",on_delete=models.CASCADE)
    def __str__(self):
        return f"Stream Message Keyword: {self.keyword.hash} -in message -> {self.message.uuid} in stream: {self.stream.uuid}"
    
@admin.register(StreamMessageKeywords)
class StreamMessageKeywords(admin.ModelAdmin):
    pass



class StreamThread(models.Model):
    stream = models.ForeignKey(Stream,verbose_name="Stream",on_delete=models.CASCADE)
    hash =  models.TextField(max_length=200,verbose_name='Hash')
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Thread Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Thread Updated')
    items = models.IntegerField(verbose_name='Item Count',default=0)
    views = models.IntegerField(verbose_name='Views Count',default=0)
    likes = models.IntegerField(verbose_name='Likes Count',default=0)
    dislikes = models.IntegerField(verbose_name='DisLikes Count',default=0)
    shares = models.IntegerField(verbose_name='Shares Count',default=0)
    comments = models.IntegerField(verbose_name='Comment Count',default=0)
    active = models.BooleanField(verbose_name="Active FLAG",default=True)
    archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    def __str__(self):
        return f"Thread: #{self.hash} -in stream-> ({self.stream.uuid})"
    
@admin.register(StreamThread)
class StreamThreadAdmin(admin.ModelAdmin):
    pass   


class MessagesPerStreamView(models.Model):
    stream_created = models.DateTimeField(verbose_name="Stream Created")
    stream_type = models.TextField(verbose_name='Stream Type')
    stream_icon = models.TextField(verbose_name='Stream Icon',blank=True,null=True)
    stream_shares = models.IntegerField(verbose_name='Share Count',default=0)
    stream_views = models.IntegerField(verbose_name='Views Count',default=0)
    stream_nodes = models.IntegerField(verbose_name='Node Count',default=0)
    stream_archived = models.BooleanField(verbose_name="Archived FLAG",default=False)
    stream_hidden = models.BooleanField(verbose_name="Hidden FLAG",default=False)
    stream_system = models.BooleanField(verbose_name="System FLAG",default=False)
    stream_group_id = models.UUIDField(verbose_name="Stream Group UUID")
    profile_uuid = models.UUIDField(default = uuid.uuid4,editable = False)
    profile_created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Profile Created')
    profile_last_seen = models.DateTimeField(verbose_name='Profile Last Seen Online',auto_now_add=True)
    profile_age = models.TextField(verbose_name='Current Age',default=1,blank=True)
    profile_name = models.TextField(verbose_name='Name')
    profile_status = models.TextField(verbose_name='status',default="CITIZEN",blank=True)
    profile_species = models.TextField(verbose_name='Species',default='Sentient')
    profile_introduction = models.TextField(verbose_name='Profile Intro')
    profile_views = models.IntegerField(verbose_name='Post Count',default=0)
    profile_pronouns = models.TextField(max_length=200,verbose_name='Pronouns')
    profile_gender = models.TextField(max_length=200,verbose_name='Gender')
    profile_avatar = models.TextField(verbose_name='Avatar URL',null=True,blank=True)
    profile_posts = models.IntegerField(verbose_name='Post Count',default=0)
    profile_views = models.IntegerField(verbose_name='Post Count',default=0)
    profile_nodes = models.IntegerField(verbose_name='Node Count',default=0)
    profile_blocked = models.BooleanField(verbose_name="Blocked FLAG",default=False)
    profile_frozen = models.BooleanField(verbose_name="Frozen FLAG",default=False)
    profile_system = models.BooleanField(verbose_name="System FLAG",default=False)
    message_uuid = models.UUIDField(default = uuid.uuid4,editable = False)
    message_created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Stream Created')
    message_type = models.TextField(verbose_name='Message Type')
    message_icon = models.TextField(verbose_name='Message Icon',blank=True,null=True)
    reposts = models.IntegerField(verbose_name='Reposts Count',default=0)
    replies = models.IntegerField(verbose_name='Replies Count',default=0)
    shares = models.IntegerField(verbose_name='Share Count',default=0)
    likes = models.IntegerField(verbose_name='Like Count',default=0)
    threads = models.IntegerField(verbose_name='Thread Count',default=0)
    views = models.IntegerField(verbose_name='Views Count',default=0)
    contents_text = models.TextField(verbose_name='Stream Content: Text Type',blank=True,null=True,max_length=500)
    contents_text_parsed = models.TextField(verbose_name='Stream Content: Text Type (Parsed)',blank=True,null=True)
    contents_json = models.JSONField(verbose_name='Stream Content: JSON Type',blank=True,null=True)
    contents_bin = models.BinaryField(verbose_name='Stream Content: Binary Type',blank=True,null=True)
    references = models.ForeignKey('StreamMessage',verbose_name = "References",on_delete=models.CASCADE,null=True,blank=True)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream,verbose_name="Stream",on_delete=models.CASCADE)
    author = models.ForeignKey(Profile,verbose_name = "Author",on_delete=models.RESTRICT)
    def __str__(self):
        return f"Message in Stream View: {self.message_uuid} in stream {self.stream.uuid} in community {self.community.uuid}"
    class Meta:
        managed = False
        db_table = 'stream_messageview'
