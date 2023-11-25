#!/usr/bin/env python3
# The Navigation component dotes the Console with the ability to auto-generate sidebar and top menus based on the installed and registered Ceres Modules.
from django.conf.urls import include
import logging
import ply
from communities.community.models import CommunitySidebarMenuView
log = logging.getLogger(__name__)
class SideBarBuilder():
  modules = {}
  
  def __init__(self,data=ply.settings.PLY_USER_DASHBOARD_MODULES,menu_module_name="sidebar_menu"):
    if (len(self.modules) == 0): self.register(data,menu_module_name)
  # Register a module to the sidebar, pass it's Module.Navigation class to this constructor: 
  def register(self,data,menu_module_name="sidebar_menu"):
    if data is False: raise ValueError('Register must receive a Navigation object from a module.')
    for mname in data:
      try:
        mod = include(f"{mname}.{menu_module_name}")[0]
        self.modules[mname] = mod.sidebar
        log.info(f"SidebarBuilder added module {mname}.{menu_module_name}!")
      except:
        self.modules[mname] = False
        log.info(f"SidebarBuilder could not add module {mname}.{menu_module_name} - not found!")


class SideBarBuilder_dynamic():
  modules = {}

  def __init__(self, community,application_mode):
    modules = CommunitySidebarMenuView.objects.filter(community=community,application_mode=application_mode,active=True)
    for modname in modules:
      try:
        mod = include(f"{modname.module}.{modname.sidebar_class}")[0]
        self.modules[modname.module] = mod.sidebar
        log.info(f"SidebarBuilder added module {modname.module}.{modname.sidebar_class}!")
      except:
        self.modules[modname.module] = False
        log.info(f"SidebarBuilder could not add module {modname.module}.{modname.sidebar_class} - not found!")


