from core.dynapages.models import Page, PageWidget
from communities.profiles.models import ProfilePageNode
from ply import system_uuids
def profile_initDynaPage(user,profile):
    """
    @brief Initialise an empty DynaPage node and apply it to the Specified profile. This method copies the DynaPage structures from the global system default dynapage node.
    :param user: p_user:User that owns the Profile.
    :type user: t_user:User Object
    :param user: p_profile:The Profile in question.
    :type user: t_profile:The Profile object.
    :returns: r: The NEW Profile Page Node Object.
    """
  # Create a new DynaPage node of a specified type.
    page = Page.objects.get(page_id=system_uuids.profile_dynapage_uuid)
    page.pk = None
    page.slug = f"profile||{user}||{profile.profile_id}"
    page.label = f"Profile page for {profile.name}"
    page.save()
    widgets = PageWidget.objects.filter(page_id=system_uuids.profile_dynapage_uuid)
    for widget in widgets:
        widget.pk = None
        widget.page_id = page.page_id
        widget.save()
    # Create Page Nodes in the Dynapage System, or update an older node:
    profile_node = ProfilePageNode.objects.get_or_create(profile=profile,node_type="profile")[0]
    profile_node.dynapage=page
    profile_node.save()
    return profile_node


def dashboard_initDynaPage(user,profile):
    """
    @brief Initialise an empty DynaPage node and apply it to the Specified Profile's DASHBOARD. This method copies the DynaPage structures from the global system default dynapage node.
    :param user: p_user:User that owns the Profile.
    :type user: t_user:User Object
    :param user: p_profile:The Profile in question.
    :type user: t_profile:The Profile object.
    :returns: r: The NEW Profile Page Node Object.
    """
  # Create a new DynaPage node of a specified type.
    page = Page.objects.get(page_id=system_uuids.pdashboard_dynapage_uuid)
    page.pk = None
    page.slug = f"profile||{user}||{profile.profile_id}"
    page.label = f"Profile page for {profile.name}"
    page.save()
    widgets = PageWidget.objects.filter(page_id=system_uuids.pdashboard_dynapage_uuid)
    for widget in widgets:
        widget.pk = None
        widget.page_id = page.page_id
        widget.save()
    # Create Page Nodes in the Dynapage System, or update an older node:
    profile_node = ProfilePageNode.objects.get_or_create(profile=profile,node_type="dashboard")[0]
    profile_node.dynapage=page
    profile_node.save()
    return profile_node

def get_or_create_dynapage_node(slug,label,system,mode,template):
    page = Page.objects.get_or_create(slug=slug,widget_mode=mode)
    if page[1] == True:
        page[0].label = label
        page[0].system = system
        page[0].widget_mode = mode
        page[0].template = template
        page[0].save()
    widgets = PageWidget.objects.filter(page=page[0])
    return page, widgets
