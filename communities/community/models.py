from logging import NullHandler

from django.db import models
from django.contrib import admin
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.apps import apps

# PLY

from communities.profiles.models import Profile
from communities.group.models import Group
from core.dynapages.models import Page, Widget, Templates
from ply.toolkit.core import get_ply_appinfo


# Create your models here.
class Community(models.Model):
    class Meta:
        db_table = "communities_community_community"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hash = models.TextField(max_length=200, verbose_name="Community Hash")
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Profile Created"
    )
    updated = models.DateTimeField(verbose_name="Profile Updated", auto_now_add=True)
    dynapage = models.ForeignKey(Page, on_delete=models.RESTRICT, blank=True, null=True)
    name = models.TextField(verbose_name="Name")
    action_call_cover = models.TextField(verbose_name="Action Call for Cover page")
    introduction = models.TextField(verbose_name="Introduction")
    tagline = models.TextField(
        verbose_name="Tagline", null=True, default=None, blank=True
    )
    avatar = models.TextField(verbose_name="Avatar", null=True)
    icon = models.ImageField(verbose_name="Community Icon", null=True, blank=True)
    logo = models.ImageField(verbose_name="Community Logo", null=True, blank=True)
    posts = models.IntegerField(verbose_name="Post Count", default=0)
    profile = models.IntegerField(verbose_name="Profile Count", default=0)
    group = models.IntegerField(verbose_name="Group Count", default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG", default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG", default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG", default=False)
    restricted = models.BooleanField(
        verbose_name="Restricted Join Mode FLAG", default=False
    )
    system = models.BooleanField(verbose_name="System FLAG", default=False)
    backgroundItem = models.ForeignKey(
        "core.GalleryItem", blank=True, null=True, on_delete=models.RESTRICT
    )
    theme = models.TextField(
        verbose_name="Community Theme Class Name", blank=True, null=True
    )

    def __str__(self):
        return f"Community: {self.name}, hash: {self.hash}"


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


class VHost(models.Model):
    class Meta:
        db_table = "communities_community_vhost"

    community = models.ForeignKey(
        Community,
        verbose_name="Community to Apply to VHOST",
        on_delete=models.CASCADE,
        default=uuid.uuid4,
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="VHost Created"
    )
    updated = models.DateTimeField(verbose_name="VHost Updated", auto_now_add=True)
    hostname = models.TextField(
        max_length=200, null=True, verbose_name="VHost Hostname"
    )
    ipaddr = models.GenericIPAddressField(
        null=True, verbose_name="VHost IP address", blank=True
    )
    archived = models.BooleanField(verbose_name="Archived FLAG", default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG", default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG", default=False)
    system = models.BooleanField(verbose_name="System FLAG", default=False)
    restricted = models.BooleanField(
        verbose_name="Restricted Joining FLAG", default=False
    )

    def __str__(self):
        return f"VHost - Hostname: {self.hostname}. IPAddr: {self.ipaddr}: Community: {self.community.name}"


@admin.register(VHost)
class VHostAdmin(admin.ModelAdmin):
    pass


class CommunityProfile(models.Model):
    class Meta:
        db_table = "communities_community_profile"

    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, verbose_name="Profile", on_delete=models.RESTRICT, null=True
    )
    joined = models.DateTimeField(verbose_name="Joined")

    def __str__(self):
        return f"Community: {self.community.name}. Profile: {self.profile.name}. Joined: {self.joined}"


@admin.register(CommunityProfile)
class CommunityProfileAdmin(admin.ModelAdmin):
    pass


class CommunityGroup(models.Model):
    class Meta:
        db_table = "communities_community_community_group"

    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, verbose_name="Group", on_delete=models.RESTRICT, null=True
    )
    joined = models.DateTimeField(verbose_name="Joined")

    def __str__(self):
        return f"Community: {self.community.name}. Group: {self.group.name}. Joined: {self.joined}"


@admin.register(CommunityGroup)
class CommunityGroupAdmin(admin.ModelAdmin):
    pass


class CommunityDashboardType(models.Model):
    class Meta:
        db_table = "communities_community_community_dashboard_type"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField(max_length=200, verbose_name="Dashboard Type Tag")
    name = models.TextField(max_length=200, verbose_name="Dashboard Type Name")
    descr = models.TextField(max_length=200, verbose_name="Dashboard Type Descr")
    privileged = models.BooleanField(
        default=False, verbose_name="Dashboard type is privileged"
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created"
    )
    updated = models.DateTimeField(verbose_name="Updated", auto_now_add=True)

    def __str__(self):
        if not self.privileged:
            return f"Dashboard Type: {self.type} -  {self.name} Created: {self.created}"
        else:
            return f"PRIVILEGED Dashboard Type: {self.type} -  {self.name} Created: {self.created}"


@admin.register(CommunityDashboardType)
class CommunityDashboardTypeAdmin(admin.ModelAdmin):
    pass


class CommunityProfileDashboardRoles(models.Model):
    class Meta:
        db_table = "communities_community_community_profile_dashboard_roles"
        unique_together = ("community", "profile", "type")

    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, verbose_name="User", on_delete=models.RESTRICT, null=True
    )
    type = models.ForeignKey(
        CommunityDashboardType,
        verbose_name="Dashboard Type",
        on_delete=models.RESTRICT,
        null=True,
    )
    dynapage_landing = models.ForeignKey(
        Page,
        verbose_name="Dashboard Landing Page Dynawidget Node",
        on_delete=models.CASCADE,
        help_text="This page will be loaded as a landing page of the dashboard mode for the given profile. (If default profile; it will be set as default for all subsequent profiles.)",
        null=True,
    )
    active = models.BooleanField(verbose_name="Active FLAG", default=True)

    def __str__(self):
        return f"Community: {self.community.name}. Profile: {self.profile.name} Dashboard type: {self.type.type}"


@admin.register(CommunityProfileDashboardRoles)
class CommunityProfileDashboardRolesAdmin(admin.ModelAdmin):
    pass


class CommunityAdmins(models.Model):
    class Meta:
        db_table = "communities_community_community_admins"
        unique_together = ("community", "profile")

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, verbose_name="User", on_delete=models.RESTRICT, null=True
    )
    created = models.DateTimeField(verbose_name="Staff Created", auto_now=True)
    active = models.BooleanField(verbose_name="Active", default=True)

    def __str__(self):
        return f"Community ADMIN: {self.community.name}. Profile: {self.profile.name}."


@admin.register(CommunityAdmins)
class CommunityAdminsAdmin(admin.ModelAdmin):
    pass


class CommunityStaff(models.Model):
    class Meta:
        db_table = "communities_community_community_staff"
        unique_together = ("community", "profile")

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, verbose_name="Profile", on_delete=models.RESTRICT, null=True
    )
    created = models.DateTimeField(verbose_name="Created", auto_now=True)
    active = models.BooleanField(verbose_name="Active FLAG", default=True)

    def __str__(self):
        return f"CS: {self.community.name}. {self.profile.name} {self.profile.creator.email}"


@admin.register(CommunityStaff)
class CommunityStaffAdmin(admin.ModelAdmin):
    pass


class ProfilePerCoummunityView(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community_uuid = models.UUIDField(verbose_name="Community UUID")
    profile_creator = models.IntegerField(verbose_name="Owner ID", default=0)
    joined = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Profile Joined"
    )
    community_name = models.TextField(verbose_name="Community Name")
    profile_created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Profile Created"
    )
    dynapage = models.ForeignKey(Page, on_delete=models.RESTRICT, blank=True, null=True)
    profile_updated = models.DateTimeField(
        verbose_name="Profile Updated", auto_now_add=True
    )
    last_seen = models.DateTimeField(
        verbose_name="Profile Last Seen Online", auto_now_add=True
    )
    age = models.TextField(verbose_name="Current Age", default=1, blank=True)
    name = models.TextField(verbose_name="Name")
    status = models.TextField(verbose_name="status", default="CITIZEN", blank=True)
    species = models.TextField(verbose_name="Species", default="Sentient")
    introduction = models.TextField(verbose_name="Profile Intro")
    level = models.TextField(verbose_name="Current Level", default=1)
    max_HP = models.TextField(verbose_name="Max HP", default=10)
    HP = models.TextField(verbose_name="Current HP", default=10)
    max_MP = models.TextField(verbose_name="Max MP", default=6)
    STUN = models.TextField(verbose_name="Current STUN", default=10)
    max_STUN = models.TextField(verbose_name="Max STUN", default=6)
    SHIELD = models.TextField(verbose_name="Current SHIELD", default=10)
    max_SHIELD = models.TextField(verbose_name="Max SHIELD", default=6)
    MP = models.TextField(verbose_name="Current MP", default=6)
    max_STA = models.TextField(verbose_name="Max STA", default=10)
    STA = models.TextField(verbose_name="Current STA", default=10)
    views = models.IntegerField(verbose_name="Post Count", default=0)
    slug = models.TextField(verbose_name="Slugified Name")
    pronouns = models.TextField(max_length=200, verbose_name="Pronouns")
    gender = models.TextField(max_length=200, verbose_name="Gender")
    avatar = models.TextField(verbose_name="Avatar URL", null=True, blank=True)
    posts = models.IntegerField(verbose_name="Post Count", default=0)
    views = models.IntegerField(verbose_name="Post Count", default=0)
    nodes = models.IntegerField(verbose_name="Node Count", default=0)
    archived = models.BooleanField(verbose_name="Archived FLAG", default=False)
    blocked = models.BooleanField(verbose_name="Blocked FLAG", default=False)
    frozen = models.BooleanField(verbose_name="Frozen FLAG", default=False)
    system = models.BooleanField(verbose_name="System FLAG", default=False)
    profile = models.ForeignKey(
        Profile, verbose_name="Profile", on_delete=models.CASCADE
    )
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    creator = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    def __str__(self):
        return f"Profile '{self.profile_id}'-[as member of community]->{self.community.name}"

    class Meta:
        managed = False
        db_table = "community_profile_per_community_view"


# Followers Table:
class Follower(models.Model):
    class Meta:
        db_table = "communities_community_follower"

    source = models.ForeignKey(
        Profile,
        verbose_name="Source Profile",
        on_delete=models.RESTRICT,
        related_name="+",
    )
    dest = models.ForeignKey(
        Profile,
        verbose_name="Dest Profile",
        on_delete=models.RESTRICT,
        related_name="+",
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Relationship Created"
    )
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    archived = models.BooleanField(verbose_name="Archived FLAG", default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG", default=False)
    system = models.BooleanField(verbose_name="System FLAG", default=False)

    def __str__(self):
        return f"Follower: {self.source.uuid} -follows-> {self.dest.uuid} in community: {self.community.uuid}"


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass


# Friends Table:
class Friend(models.Model):
    class Meta:
        db_table = "communities_community_friend"

    friend1 = models.ForeignKey(
        Profile,
        verbose_name="Friend 1 Profile",
        on_delete=models.RESTRICT,
        related_name="+",
    )
    friend2 = models.ForeignKey(
        Profile,
        verbose_name="Friend 2 Profile",
        on_delete=models.RESTRICT,
        related_name="+",
    )
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Request Created"
    )
    approved = models.DateTimeField(verbose_name="Approved?", null=True)
    approved_flag = models.BooleanField(verbose_name="Approved FLAG", default=False)
    archived = models.BooleanField(verbose_name="Archived FLAG", default=False)
    hidden = models.BooleanField(verbose_name="Hidden FLAG", default=False)
    system = models.BooleanField(verbose_name="System FLAG", default=False)

    def __str__(self):
        return f"Friends: {self.friend1.uuid} <-> {self.friend2.uuid}  in community: {self.community.uuid}"


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass


class Friend_ExpLvl_View(models.Model):
    friend1_id = models.UUIDField(verbose_name="Friend 1 UUID")
    approved = models.DateTimeField(verbose_name="Approved?", null=True)
    approved_flag = models.BooleanField(verbose_name="Approved FLAG", default=False)
    friend2_id = models.UUIDField(verbose_name="Friend 2 UUID")
    community_id = models.UUIDField(verbose_name="Community  UUID")
    profile_id = models.CharField(verbose_name="Profile ID", max_length=200)
    updated = models.DateTimeField(verbose_name="Friendship Updated")
    age = models.IntegerField(verbose_name="Profile Age")
    name = models.CharField(verbose_name="Name", max_length=200)
    class_name = models.CharField(verbose_name="Class Name", max_length=200)
    status = models.CharField(verbose_name="Status", max_length=200)
    species = models.CharField(verbose_name="Species", max_length=200)
    introduction = models.TextField(verbose_name="Profile Intro")
    slug = models.TextField(verbose_name="Slugified Name")
    pronouns = models.TextField(max_length=200, verbose_name="Pronouns")
    gender = models.TextField(max_length=200, verbose_name="Gender")
    avatar = models.TextField(verbose_name="Avatar URL", null=True, blank=True)
    level_id = models.UUIDField(verbose_name="Level UUID")
    classtype_id = models.UUIDField(verbose_name="Classtype UUID")
    community_id = models.UUIDField(verbose_name="Community UUID")
    expr = models.IntegerField(verbose_name="Experience Points")
    current_level = models.IntegerField(verbose_name="Current Level")

    def __str__(self):
        return f"Friend ExpLevel View: Friend: [{self.friend1_id}]-with->[{self.friend2_id}]"

    class Meta:
        managed = False
        db_table = "community_friend_explvl_view"


class CommunityRegistry(models.Model):
    class Meta:
        db_table = "communities_community_registry"
        unique_together = ["community", "key"]
        indexes = [
            models.Index(fields=["grouping_key"]),
            models.Index(fields=["key"]),
            models.Index(fields=["grouping_key", "key"]),
            models.Index(fields=["community"]),
            models.Index(fields=["grouping_key", "key", "community"]),
            models.Index(fields=["community", "key"]),
        ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    key = models.TextField(max_length=400, verbose_name="Setting key")
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Setting Created"
    )
    grouping_key = models.TextField(
        max_length=200, verbose_name="Setting Grouping key", null=True, blank=True
    )
    updated = models.DateTimeField(verbose_name="Setting Updated", auto_now_add=True)
    name = models.TextField(verbose_name="Setting Name")
    foreign_key_ref = models.TextField(
        verbose_name="Foreign Key Reference (if used)", null=True, blank=True
    )
    text_value = models.TextField(verbose_name="Text Value", null=True, blank=True)
    int_value = models.IntegerField(verbose_name="Int Value", null=True, blank=True)
    json_value = models.JSONField(verbose_name="Json Value", null=True, blank=True)
    bin_value = models.BinaryField(verbose_name="Binary Value", null=True, blank=True)
    bool_value = models.BooleanField(verbose_name="Boolean Value", null=True, blank=True,default=False)
    uuid_value = models.UUIDField(verbose_name="UUID Value", null=True, blank=True)

    def clear_all(self,confirm=False):
        if confirm:
            self.text_value = None
            self.int_value = None
            self.json_value = None
            self.bin_value = None
            self.bool_value = False
            self.uuid_value = None
            self.save()

    def __str__(self):
        rstr = f"Community: {self.community.name} - Registry Setting {self.key}"
        if self.grouping_key:
            rstr += f" [Grouping Key: {self.grouping_key}]"
        return rstr


@admin.register(CommunityRegistry)
class CommunityRegistryAdmin(admin.ModelAdmin):
    pass


class CommunitySidebarMenu(models.Model):
    class Meta:
        db_table = "communities_community_sidebar"
        unique_together = ["community", "module", "sidebar_class"]
        ordering = ["community", "application_mode", "ordering"]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    application_mode = models.TextField(
        max_length=200,
        verbose_name="Application Mode:",
        choices=[(x, x) for x in settings.PLY_DASHBOARD_MODES],
        help_text="Dashboard Application Mode to create menu for",
    )
    module = models.TextField(
        max_length=200,
        verbose_name="Module/AppName:",
        choices=[
            (x, x) for x in settings.INSTALLED_APPS if get_ply_appinfo(x) is not None
        ],
        help_text="Application to Include in the Menus",
    )
    sidebar_class = models.TextField(
        max_length=200,
        verbose_name="Sidebar Class:",
        default="sidebar_menu",
        help_text="Sidebar class to load for menu",
    )
    ordering = models.IntegerField(
        verbose_name="Ordering Key:",
        help_text="Ordering Key to assemble menus",
        default=1,
    )
    active = models.BooleanField(verbose_name="Active", default=True)
    not_edited = models.BooleanField(
        verbose_name="Not Edited",
        help_text="IGNORE: Internal control flag",
        default=False,
    )

    def __str__(self):
        return f"Community: {self.community.name} - Sidebar Entry  {self.module}.{self.sidebar_class} for mode {self.application_mode}"


@admin.register(CommunitySidebarMenu)
class CommunitySidebarMenuAdmin(admin.ModelAdmin):
    pass


class CommunitySidebarMenuView(models.Model):
    class Meta:
        db_table = "communities_community_sidebar_view"
        managed = False
        ordering = ["community", "application_mode", "ordering"]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(
        Community, verbose_name="Community", on_delete=models.CASCADE
    )
    application_mode = models.TextField(max_length=200, verbose_name="Application Mode")
    module = models.TextField(
        max_length=200,
        verbose_name="Module",
        choices=[(x, x) for x in settings.INSTALLED_APPS],
    )
    sidebar_class = models.TextField(
        max_length=200, verbose_name="Sidebar Class", default="sidebar_menu"
    )
    ordering = models.IntegerField(verbose_name="Ordering Key", default=1)
    active = models.BooleanField(verbose_name="Entry Active", default=True)


class CommunityRegistryPageView(models.Model):
    class Meta:
        db_table = "communities_community_registry_page_view"
        managed = False

    key = models.TextField(max_length=300, verbose_name="Setting Key", unique=True)
    grouping_key = models.TextField(max_length=300, verbose_name="Setting Community Grouping", unique=True)
    community = models.ForeignKey(Community,verbose_name="Community",on_delete=models.CASCADE)
    slug = models.TextField(max_length=300, verbose_name="Page slug", unique=True)
    label = models.TextField(max_length=200, verbose_name="Page Label")
    template = models.ForeignKey(
        Templates, verbose_name="Dynapage Template", on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User, verbose_name="User", on_delete=models.CASCADE, null=True
    )
    system = models.BooleanField(verbose_name="System Page", default=False)
    page = models.ForeignKey(Page,verbose_name="Page",on_delete=models.CASCADE)
    def __str__(self):
        return f"Community: {self.community.name} - Setting Key   {self.key} - Page Node {self.page_id}"


