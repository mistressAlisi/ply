from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import datetime
# Create your views here.
#PLY:
from ply import settings
from ply.toolkit import vhosts,profiles
from dashboard.navigation import SideBarBuilder
from profiles.models import Profile
from almanac.models import AlmanacMenuCategory,AlmanacMenuCategoryEntry,AlmanacPage,AlmanacPageText
from dynapages.models import Templates,Page
from almanac.forms import NewPageForm
from community.models import CommunityAdmins
# Render the User Dashboard Home page:

@login_required
def create_page(request):
    #  Ignore port:
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    #Almanac menu builder:
    almanac_cats = AlmanacMenuCategory.objects.filter(blocked=False,frozen=False)
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    all_profiles = profiles.get_all_profiles(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) == 0):
        return render(request,"error-403_access_denied.html",{'community':community,'vhost':vhost}) 
    new_form = NewPageForm()
    request.session['community'] = str(community.uuid)
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'all_profiles':all_profiles,'is_admin':True,'url_path':request.path,"profiles":all_profiles,'new_page_form':new_form}
    return render(request,"almanac_create_page.html",context)

@login_required
def create_page_preview(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    dt = datetime.datetime.now()
    almanac_cats = AlmanacMenuCategory.objects.filter(blocked=False,frozen=False)
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    all_profiles = profiles.get_all_profiles(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) == 0):
        return render(request,"error-403_access_denied.html",{'community':community,'vhost':vhost}) 
    request.session['community'] = str(community.uuid)
    
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'all_profiles':all_profiles,'is_admin':True,'url_path':request.path,"profiles":all_profiles,'title':request.POST["title"],'introduction':request.POST["introduction"],'content':request.POST['page_contents'],'dynapage':request.POST['dynaPage'],'timestamp':dt}
    return render(request,"almanac_create_page-preview.html",context)


@login_required
def create_page_commit(request):
    vhost = request.META["HTTP_HOST"].split(":")[0];
    community = (vhosts.get_vhost_community(hostname=vhost))
    if community is None:
        return render(request,"error-no_vhost_configured.html",{})
    dt = datetime.datetime.now()
    almanac_cats = AlmanacMenuCategory.objects.filter(blocked=False,frozen=False)
    sideBar = SideBarBuilder()
    profile = profiles.get_active_profile(request)
    all_profiles = profiles.get_all_profiles(request)
    is_admin = CommunityAdmins.objects.filter(community=community,profile=profile,active=True)
    if (len(is_admin) == 0):
        return render(request,"error-403_access_denied.html",{'community':community,'vhost':vhost}) 
    request.session['community'] = str(community.uuid)
    # Commit and save the page Node and then the page contents:
    page_id = slugify(request.POST["title"])
    title = request.POST["title"]
    dynaPage_id = request.POST["dynaPage"]
    dynaPage = Templates.objects.get(template_id=dynaPage_id)
    contents = request.POST["page_contents"]
    introduction = request.POST["introduction"]
    almanacPage = AlmanacPage.objects.get_or_create(page_id=page_id,creator=profile,owner=request.user,community=community)[0];
    almanacPage.title = title;
    almanacPage.community = community;
    almanacPage.dynaPage = dynaPage;
    almanacPage.introduction = introduction;
    # Move all previous pages to history:
    oldPages = AlmanacPageText.objects.filter(page=almanacPage)
    for oldPage in oldPages:
        oldPages.current = False
        almanacPage.nodes += 1
        
    pageText = AlmanacPageText.objects.get_or_create(page=almanacPage,archived=False,current=True)[0]
    almanacPage.nodes += 1
    almanacPage.creator = profile
    pageText.page_contents = contents
    pageText.save()
    almanacPage.save()
    return redirect('/almanac/page/'+page_id)
    #return JsonResponse("ok",safe=False)
    
    
    
