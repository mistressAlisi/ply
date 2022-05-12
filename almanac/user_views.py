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
from almanac.forms import NewPageForm,NewCategoryForm,AddPageForm
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
    
    

@login_required
def edit_page(request,page_id):
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
    request.session['community'] = str(community.uuid)
    if (len(is_admin) == 0):
        return render(request,"error-403_access_denied.html",{'community':community,'vhost':vhost})
    if 'page_id' in request.POST:
        new_form = NewPageForm(request.POST)
        if (new_form.is_valid()):
            almanac_page = AlmanacPage.objects.get(page_id=page_id)
            almanac_page.title = new_form.cleaned_data['title']
            almanac_page.introduction = new_form.cleaned_data['introduction']
            dynaPage = Templates.objects.get(template_id=new_form.cleaned_data['dynaPage'])
            almanac_page.dynaPage = dynaPage
            # store the current page in history and create a new one:
            oldPages = AlmanacPageText.objects.filter(page=almanac_page)
            for oldPage in oldPages:
                oldPages.current = False
                almanac_page.nodes += 1
            page_text = AlmanacPageText.objects.get_or_create(page=almanac_page,archived=False,current=True)[0]
            almanac_page.nodes += 1
            almanac_page.creator = profile
            page_text.page_contents = new_form.cleaned_data['page_contents']
            page_text.save()
            almanac_page.save()
            context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'all_profiles':all_profiles,'is_admin':True,'url_path':request.path,"profiles":all_profiles,'new_page_form':new_form,'almanac_page':almanac_page,'page_text':page_text}
            return render(request,"almanac_edit_page-preview.html",context)    
    else:
        almanac_page = AlmanacPage.objects.get(page_id=page_id)
        almanac_page_text = AlmanacPageText.objects.get(page=almanac_page,current=True)
        new_form = NewPageForm(initial={'page_id':page_id,'title':almanac_page.title,'introduction':almanac_page.introduction,'page_contents':almanac_page_text.page_contents})
        context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'all_profiles':all_profiles,'is_admin':True,'url_path':request.path,"profiles":all_profiles,'new_page_form':new_form,'almanac_page':almanac_page}
        return render(request,"almanac_edit_page.html",context)    
    


@login_required
def edit_menu(request):
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
    request.session['community'] = str(community.uuid)
    if (len(is_admin) == 0):
        return render(request,"error-403_access_denied.html",{'community':community,'vhost':vhost})
    new_cat_form = NewCategoryForm()
    add_page_form = AddPageForm()
    context = {'community':community,'vhost':vhost,'sidebar':sideBar.modules.values(),'current_profile':profile,"av_path":settings.PLY_AVATAR_FILE_URL_BASE_URL,'all_profiles':all_profiles,'is_admin':True,'url_path':request.path,"profiles":all_profiles,'new_cat_form':new_cat_form,'add_page_form':add_page_form}
    return render(request,"almanac_edit_menu.html",context)    

