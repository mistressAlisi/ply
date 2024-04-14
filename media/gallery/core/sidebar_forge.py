from media.gallery.core.models import GalleryCoreSettings

sidebar = {
  "mname":"gallery",
  "label":"Galleries",
  "icon":"fa-solid fa-images",
  "url":"media/gallery/core",
  "js":"/static/js/forge_create-community.js",
  "menu":[
    {"url":"media.gallery.core/setup","label":"Gallery Settings",'icon':'fa-solid fa-gear','onclick':''}
    #{"url":"forge/script/studio","label":"PLYScript Studio",'icon':'fa-solid fa-star','onclick':''},
    #{"url":"community/inbox","label":"Messages",'icon':'fa-solid fa-inbox'},
    #{"url":"community/follow","label":"Follow[ers]",'icon':'fa-solid fa-magnifying-glass'},
    #{"url":"community/groups","label":"Groups",'icon':'fa-solid fa-people-line'}

    ]
  }

def dynamic(local_sidebar,community,app_mode):
  if "_dyn" not in local_sidebar:
    gallery_settings = GalleryCoreSettings.objects.get(community=community)
    plugins = gallery_settings.enabled_plugins.all()
    for plugin in plugins:
      local_sidebar["menu"].append({"url":f"media.gallery.core/setup/plugin/{plugin.app}","label":f"{plugin.name} Settings",'icon':'fa-solid fa-gear','onclick':''})
    local_sidebar["_dyn"] = True
  return local_sidebar
