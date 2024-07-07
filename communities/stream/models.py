import uuid
from django.db import models
from django.contrib import admin

#PLY:
from communities.community.models import Community
from communities.profiles.models import Profile
from content_manager.keywords.models import Keyword
from communities.group.models import Group


class StreamType(models.Model):

    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Type Created')
    name = models.TextField(verbose_name='Type Name',null=True,blank=True)
    descr = models.TextField(verbose_name='Type Descr',null=True,blank=True)
    class Meta:
        db_table = "communities_stream.stream_type"
        constraints = [
            models.UniqueConstraint(fields=['name','community'], name='unique_stream_type')
    ]
    def __str__(self):
        return f"Stream Type: {self.name}"

# Create your models here.
# Stream Index Table:
class Stream(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Stream Created')
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.RESTRICT,null=True)
    profile = models.ForeignKey(Profile,verbose_name = "Profile",on_delete=models.RESTRICT,null=True)
    group = models.ForeignKey(Group,verbose_name = "Group",on_delete=models.RESTRICT,null=True,blank=True)
    streamtype = models.ForeignKey(StreamType,verbose_name="Stream Type (public)",on_delete=models.RESTRICT,null=True,blank=True)
    type = models.TextField(verbose_name='Stream Type (internal)')
    name = models.TextField(verbose_name='Stream Name',null=True,blank=True)
    descr = models.TextField(verbose_name='Stream Description',null=True,blank=True)
    tag = models.TextField(verbose_name='Stream Tag',null=True,blank=True)
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
    class Meta:
        db_table = "communities_stream_stream"
        constraints = [
            models.UniqueConstraint(fields=['tag','profile','community'], name='unique_stream_tag')
    ]
    def rgba1(self):

        return f"rgba({int(self.bkg1[1:3],16)},{int(self.bkg1[3:5],16)},{int(self.bkg1[5:7],16)},{self.opacity1})"

    def rgba2(self):
        return f"rgba({int(self.bkg2[1:3],16)},{int(self.bkg2[3:5],16)},{int(self.bkg2[5:7],16)},{self.opacity1})"

    def __str__(self):
        return f"Stream for Profile: {self.profile} in community: {self.community} attached to group: {self.group} root stream: {self.root_stream} Type: {self.type}, name: {self.name}. tag: {self.tag}"

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    pass

# Stream Suscriber Table:
class StreamSubscriber(models.Model):
    class Meta:
        db_table = "communities_stream_stream_subscriber"
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
    class Meta:
        db_table = "communities_stream_stream_message"
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


    # This function will select all keywords associated to the string message using StreamMessageKeywords, and increase their view count by one.
    def incrementKeywordViews(self):
        kws = StreamMessageKeywords.objects.filter(stream=self.stream,message=self)
        for k in kws:
            k.keyword.views += 1
            k.keyword.save()

    def __str__(self):
        return f"Stream Message: {self.uuid} -in stream-> {self.stream.uuid} in community: {self.stream.community.uuid} TYPE: {self.type}"

@admin.register(StreamMessage)
class StreamMessageAdmin(admin.ModelAdmin):
    pass



class StreamMessageKeywords(models.Model):
    class Meta:
        db_table = "communities_stream_stream_message_keywords"
    stream = models.ForeignKey(Stream,verbose_name="Stream",on_delete=models.CASCADE)
    message = models.ForeignKey(StreamMessage,verbose_name="Message",on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword,verbose_name="Keyword",on_delete=models.CASCADE)
    def __str__(self):
        return f"Stream Message Keyword: {self.keyword.hash} -in message -> {self.message.uuid} in stream: {self.stream.uuid}"

@admin.register(StreamMessageKeywords)
class StreamMessageKeywordsAdmin(admin.ModelAdmin):
    pass



class StreamThread(models.Model):
    class Meta:
        db_table = "communities_stream_stream_thread"
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
class StreamXMPPSettings(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False,verbose_name="Enable XMPP Subsystem",help_text="Enable the XMPP Subsystem and integration with Ejabberd and the global XMPP network.")
    endpoint = models.TextField(verbose_name="XMPP API REST Endpoint",help_text="Ejabberd mod_http management API endpoint URL")
    server = models.TextField(verbose_name="XMPP Server Hostname",help_text="XMPP Server Hostname (where clients connect to)")
    domain = models.TextField(verbose_name="XMPP Server FQDN",help_text="XMPP Server Domain (For JID creation: user@fqdn)")
    streams = models.TextField(verbose_name="XMPP Streams Hostname",help_text="XMPP Streams Service Hostname (where Stream objects are created): subdomain only!")
    pubsub = models.TextField(verbose_name="XMPP Pubsub Hostname",help_text="XMPP Pubsub Service Hostname (where Pubsub objects are created): subdomain only!")
    conference = models.TextField(verbose_name="XMPP Conference Hostname",help_text="XMPP Conf Hostname (where Conf objects are created): subdomain only!")
    self_reg = models.BooleanField(default=True,verbose_name="Enable User self-registration",help_text="Allow users to register JIDs by themselves: UID@fqdn from their User Dashboard!")
    auto_group = models.BooleanField(default=True,verbose_name="Automatic MUC for Groups",help_text="Automatically create a MUC (Multi User Channel/Chat) for any created groups, streams, users, etc.")
    # grant_admin = models.BooleanField(default=True,verbose_name="Grant XMPP Admin for Admin Profiles",help_text="For Profiles with ADMIN Status, grant XMPP Admin status during JID creation.")
    # grant_mod = models.BooleanField(default=False,verbose_name="Grant XMPP Mod for Admin Profiles",help_text="For Profiles with ADMIN Status, grant XMPP Mod status during JID creation.")
    # grant_admin2staff = models.BooleanField(default=False,verbose_name="Grant XMPP Admin for Staff Profiles",help_text="For Profiles with Staff Status, grant XMPP Admin status during JID creation.")
    # grant_mod2staff = models.BooleanField(default=True,verbose_name="Grant XMPP Mod for Staff Profiles",help_text="For Profiles with Staff Status, grant XMPP Mod status during JID creation.")
    #


    class Meta:
        db_table = "communities_stream_stream_xmpp_settings"
        constraints = [
            models.UniqueConstraint(fields=['community'], name='unique_xmpp_settings')
        ]

    def __str__(self):
        return f"XMPP Settings - Community: {self.community.name}. XMPP Enabled: {self.enabled}"


@admin.register(StreamXMPPSettings)
class StreamXMPPSettingsAdmin(admin.ModelAdmin):
    pass


class StreamProfileXMPPSettings(models.Model):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name="Profile",on_delete=models.CASCADE)
    jid = models.TextField(verbose_name="JID")
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Settings Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Settings Updated')
    auto_add_friend = models.BooleanField(default=True,verbose_name="Automatically add new friends to XMPP Contacts",help_text="When enabled, any new friends you add on the site will be automatically added to your XMPP contact list as well.")
    create_mucs = models.BooleanField(default=True,verbose_name="Create MUCs (Multi user Chatrooms) for new streams",help_text="When enabled, any new stream you create will automatically be assigned a MUC in the XMPP server.")
    publish_streams = models.BooleanField(default=True,verbose_name="Automatically Publish Stream content to XMPP",help_text="When enabled, any stream posts you create on-site will be published via the XMPP service automatically.")
    publish_notices = models.BooleanField(default=True,verbose_name="Automatically Publish Stream notifications to XMPP",help_text="When enabled, any stream posts you create on-site will be published via the XMPP service automatically.")
    publish_to_groups = models.BooleanField(default=True,verbose_name="Automatically Publish Stream content to Group XMPP Streams",help_text="When enabled, any stream posts you create on-site will be published via the XMPP service to the related groups.")
    join_group_mucs = models.BooleanField(default=True,verbose_name="Automaticlaly join the XMPP MUCs for any group joined",help_text="When enabled, you'll be automatically added to the XMPP multi-user-chat (MUC) for any group you join on the site.")
    pubsub_to_friends = models.BooleanField(default=True,verbose_name="Enable Publish/Subscribe module for XMPP Friends",help_text="When enabled, any content you create is published in streams your friends can follow using an XMPP client.")
    enable_webclient = models.BooleanField(default=True,verbose_name="Enable XMPP Webclient",help_text="Enable/disable the embedded XMPP client for all pages on the site. This does not control/disable other XMPP Clients")



    class Meta:
        db_table = "communities_stream_stream_xmpp_profile_settings"
        constraints = [
            models.UniqueConstraint(fields=['profile', 'community'], name='unique_stream_xmpp_profile'),
            models.UniqueConstraint(fields=['jid'], name='unique_stream_xmpp_jid')
        ]


    def __str__(self):
        return f"XMPP Profile Settings - Community: {self.community.name}. Profile: {self.profile.name}"

    def get_UID(self):
        return self.jid.split("@")[0]

@admin.register(StreamProfileXMPPSettings)
class StreamProfileXMPPSettingsAdmin(admin.ModelAdmin):
    pass



class StreamProfileXMPPMUCs(models.Model):
    class Meta:
        db_table = "communities_stream_stream_xmpp_profile_mucs"
        constraints = [
            models.UniqueConstraint(fields=['name', 'service','host'], name='unique_stream_xmpp_muc'),
        ]

    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    XMPPJID = models.ForeignKey(StreamProfileXMPPSettings,verbose_name="Source XMPP JID",on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,verbose_name="Profile",on_delete=models.CASCADE)
    name = models.TextField(verbose_name="Room Name")
    descr = models.TextField(verbose_name="Room Description")
    service = models.TextField(verbose_name="Service Host FQDN")
    host = models.TextField(verbose_name="Room Host/Virtual Host")
    created = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='Settings Created')
    updated = models.DateTimeField(auto_now=True,editable=False,verbose_name='Settings Updated')


    def __str__(self):
        return f"XMPP Profile MUC - Source JID: {self.XMPPJID.jid}. Room: {self.name}@{self.service} at {self.host}"


@admin.register(StreamProfileXMPPMUCs)
class StreamProfileXMPPMUCsAdmin(admin.ModelAdmin):
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
        db_table = 'communities_stream_message_view'



class MessagesPerNamedStreamView(models.Model):
    stream_created = models.DateTimeField(verbose_name="Stream Created")
    stream_type = models.TextField(verbose_name='Stream Type')
    stream_name = models.TextField(verbose_name='Stream Name')
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
        return f"Message in Stream Named View:  {self.stream_name} in community {self.community.uuid} Type: {self.message_type}"
    class Meta:
        managed = False
        db_table = 'communities_stream_named_message_view'



