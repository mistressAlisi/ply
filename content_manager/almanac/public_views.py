from django.shortcuts import render
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from content_manager.almanac.models import AlmanacMenuCategory
from communities.community.models import CommunityAdmins
from content_manager.almanac.models import AlmanacPage,AlmanacPageText
# Render the User Dashboard Home page:

def almanac_home(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    #Almanac menu builder:
    almanac_cats = AlmanacMenuCategory.objects.filter(blocked=False,frozen=False)
    sideBar = SideBarBuilder()
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
        is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
        if (len(is_admin) == 0):
            enable_admin = False
        else:
            enable_admin = True
    else:
        profile = False
        all_profiles = False
        enable_admin = False
    request.session['community'] = str(community.uuid)
    try:
        almanac_page = AlmanacPage.objects.get(page_id='community_index_page',community=community)
        almanac_page_text = AlmanacPageText.objects.get(page=almanac_page,current=True)
    except AlmanacPage.DoesNotExist as e:
        almanac_page = False
        almanac_page_text = False
    all_pages = AlmanacPage.objects.filter(community=community).order_by('page_id')
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'enable_admin':enable_admin,'url_path':request.path,"profiles":all_profiles,'all_pages':all_pages,'content':almanac_page_text,'almanac_page':almanac_page,'ply_version':settings.PLY_VERSION}
    return render(request,"almanac_dashboard.html",context)


def almanac_page(request,page_id):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    #Almanac menu builder:
    almanac_cats = AlmanacMenuCategory.objects.filter(blocked=False,frozen=False)
    sideBar = SideBarBuilder()
    if request.user.is_authenticated:
        profile = profiles.get_active_profile(request)
        all_profiles = profiles.get_all_profiles(request)
        is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
        if (len(is_admin) == 0):
            enable_admin = False
        else:
            enable_admin = True
    else:
        profile = False
        all_profiles = False
        enable_admin = False

    request.session['community'] = str(community.uuid)
    almanac_page = AlmanacPage.objects.get(page_id=page_id)
    almanac_page_text = AlmanacPageText.objects.get(page=almanac_page,current=True)
    all_pages = AlmanacPage.objects.filter(community=community).order_by('page_id')
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'enable_admin':enable_admin,'url_path':request.path,"profiles":all_profiles,'almanac_page':almanac_page,'content':almanac_page_text,'all_pages':all_pages,'ply_version':settings.PLY_VERSION}
    return render(request,"almanac_dashboard.html",context)
