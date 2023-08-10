from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ply.toolkit import logger as plylog
from django.http import JsonResponse
import ply
import importlib
from ply.toolkit import profiles, reqtools
from core.dynapages.models import Widget,PageWidget
from communities.profiles.models import ProfilePageNode

log = plylog.getLogger('dynapages.api_views',name='dynapages.api_views')
#queue = GalleryPublisher(ply.settings.PLY_MSG_BROKER_URL,log)
#queue.start()


@login_required
def widget_setup(request,widget_id,mode):
    """
    @brief SETUP a new widget for a given profile reference.
    ===============================
    :param request: p_request:Django Request Object
    :type request: t_request:str
    :param request: p_widget_id:Widget ID from the request
    :type request: t_request:str
    :param request: p_mode:Mode to start and configure the widget in
    :type request: t_request:str
    :returns: r:HTML Rendered Widget, ready to start on the page.
    """
    community = reqtools.vhost_community_or_404(request)
    widget = Widget.objects.get(widget_id=widget_id)
    profile = profiles.get_active_profile(request)
    if "col" in request.GET:
        col = request.GET["col"]
    else:
        col = False
    if (widget.setup_required is False):
            return JsonResponse("ok",safe=False)
    else:
            form_module = importlib.import_module(widget.setup_form)
            setup_form = form_module.WidgetForm(request=request)
            context = {'widget':widget,'mode':mode,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL,'setup_form':setup_form,'widget_col':col}
            return render(request,'dynapages_tools/widget_editor/widget_setup.html',context)


@login_required
def widget_setup_factory(request,node_type='profile'):
    community = reqtools.vhost_community_or_404(request)
    w_id = request.POST["widget_id"]
    mode = request.POST["widget_mode"]
    if 'widget_col' in request.POST:
        col = request.POST["widget_col"]
    else:
        col = False
    widget = Widget.objects.get(widget_id=w_id)
    if (widget.setup_required is False):
            return JsonResponse({'res':"err"},safe=False)
    form_module = importlib.import_module(widget.setup_form)
    setup_form = form_module.WidgetForm(request.POST,request=request)
    if  not setup_form.is_valid():
        return JsonResponse({'res':"err",'err':setup_form.errors.items},safe=False)
    #print(setup_form.cleaned_data)
    profile = profiles.get_active_profile(request)
    profilePage = ProfilePageNode.objects.get(profile=profile,node_type=node_type)
    pageWidget = PageWidget(widget=widget,page=profilePage.dynapage,plugin_data=setup_form.cleaned_data)
    if (mode == "banner"):
        pageWidget.banner = True
    elif (mode == "mainbody"):
        pageWidget.mainbody = True
    elif (mode == "sidecol"):
        pageWidget.sidecol = True
    elif (mode == "footer"):
        pageWidget.footer = True
    pageWidget.pos = col
    pageWidget.save()
    context = {'widget':pageWidget,'mode':mode,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,'dynapages_api/widget_container.html',context)

@login_required
def widget_factory(request,widget_id,mode,node_type='profile'):
    community = reqtools.vhost_community_or_404(request)
    widget = Widget.objects.get(widget_id=widget_id)
    profile = profiles.get_active_profile(request)
    profilePage = ProfilePageNode.objects.get(profile=profile,node_type=node_type)
    pageWidget = PageWidget(widget=widget,page=profilePage.dynapage)
    if (mode == "banner"):
        pageWidget.banner = True
    elif (mode == "mainbody"):
        pageWidget.mainbody = True
    elif (mode == "sidecol"):
        pageWidget.sidecol = True
    elif (mode == "footer"):
        pageWidget.footer = True
    if ('col' in request.GET):
        pageWidget.pos = request.GET['col']
    pageWidget.save()
    context = {'widget':pageWidget,'mode':mode,'profile':profile,"av_path":ply.settings.PLY_AVATAR_FILE_URL_BASE_URL}
    return render(request,'dynapages_api/widget_container.html',context)
