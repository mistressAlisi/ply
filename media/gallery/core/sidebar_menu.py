sidebar = {}

sidebar_core_not_implemented_yet = {
  "mname":"core",
  "label":"Galleries and Collections",
  "icon":"far fa-images",
  "url":"core",
  "js":"/static/js/gallery_core.js",
  "sidebar":"/console/devices/get/sidebar",
  "menu":[
    {"url":"core/collections","label":"All Galleries",'icon':'fas fa-photo-video','onclick':'gallery_list_init'},
    {"url":"core/likes","label":"My Liked Pieces",'icon':'fas fa-heart'},
    {"url":"core/collections","label":"All Collections",'icon':'fas fa-icons'},
    {"url":"core/manage","label":"Manage Galleries",'icon':'fa-solid fa-pen-to-square'},
    {"url":"core/upload","label":"Upload Submission(s)",'icon':'fas fa-upload'},
    {"url":"core/upload/lighttable/","label":"Submission Light Table",'icon':'fas fa-th'}
    ]
  }

