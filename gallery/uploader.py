#!/usr/bin/env python3
# The Navigation component dotes the Console with the ability to auto-generate sidebar and top menus based on the installed and registered Ceres Modules.
from django.conf.urls import include
import ply
class upload_plugins_builder():
  modules = {}
  
  def __init__(self):
    if (len(self.modules) is 0): self.register(ply.settings.PLY_GALLERY_PLUGINS)
  # Register a module to the sidebar, pass it's Module.Navigation class to this constructor: 
  def register(self,data):
    if data is False: raise ValueError('UploadButtonBuilder must recieve a PLY_GALLERY_PLUGINS object!')
    for mname in data:
      mod = include(mname+'.upload')[0]
      self.modules[mname] = mod.gallery_upload_plugin
      


