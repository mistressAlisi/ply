#!/usr/bin/env python3
# The Navigation component dotes the Console with the ability to auto-generate sidebar and top menus based on the installed and registered Ceres Modules.
from django.conf.urls import include
import ply
class SideBarBuilder():
  modules = {}
  
  def __init__(self):
    if (len(self.modules) == 0): self.register(ply.settings.PLY_USER_DASHBOARD_MODULES)
  # Register a module to the sidebar, pass it's Module.Navigation class to this constructor: 
  def register(self,data):
    if data is False: raise ValueError('Register must recieve a Navigation object from a module.')
    for mname in data:
      mod = include(mname+'.sidebar_menu')[0]
      self.modules[mname] = mod.sidebar
      

