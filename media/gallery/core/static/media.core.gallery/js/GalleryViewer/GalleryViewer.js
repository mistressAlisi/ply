import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class GalleryViewer extends AbstractDashboardApp {
    _appName = "GalleryViewer";

    /** COLLECTION objects: Each collection holds the set of FILE objects and CARDS that represent a view. This is used for the vieweing functions. **/
    /** COLLections In View (cols_iv): **/
    cols_iv= [];
    /** keys: **/
    cols_iv_k= [];
    cols_iv_oa= [];
     /** Navigation and UI/UX controls: **/
    nav = {
        count: 0,
        first: "",
        last: "",
        cards: [],
        current: false,
        colid: false,
        pageX: 0,
        pageY: 0,
    }

    /** Plugins registry: **/
    plugins= {
        names: [],
        modules: {}
    }
    /** Callback function for loadPlugin: **/
    _loadPlugin(d) {
        if (d == false) { return false; };
        if (d.type != "gallery-plugin") {
            console.error("Wrong Datatype for Plugin!!"); 
            alert("Gallery Core can't load: "+d.name+". plugin.json has wrong type.");
            return false;
        };
        /** load module javascripts if available: **/
        var jml = d.module.length;
        if (jml > 0) {
            var count = 0;
            while (count < jml) {
                console.debug("Gallery Core Loading Plugin Module: "+d.module[count]);
                import(this.urls["_plugin_prefix"]+d.name+"/js/"+d.module[count]).then((module)=> {
                    this.plugins.modules[d.id] = new module.GalleryPlugin();
                })
                count = count+1;
            }
        };
        /** load javascript: **/
        var jsl = d.js.length;
        if (jsl > 0) {
          count = 0;
          while (count < jsl) {
              var jsp = this.urls["_plugin_prefix"]+d.name+"/js/"+d.js[count];
              console.debug("Gallery Core Loading Plugin JS: "+jsp);
              $.getScript(jsp);
              count++;
        }};
        /** load css: **/
        var csl = d.css.length;
        if (csl > 0) {
          count = 0;
          while (count < csl) {
              var csp = this.urls["_plugin_prefix"]+d.name+"/css/"+d.css[count];
              console.debug("Gallery Core Loading Plugin CSS: "+csp);
              $('head').append( $('<link rel="stylesheet" type="text/css" />').attr('href', csp));
              count++;
        }};
        


    }


    /**
     * loadPlugin: Loads a plugin from the specified _plugin_prefix dir, for the given gallery plugin.
     *  The plugin must include a gallery_plugin.json that describes the css and js files to be loaded.
     *  See example: Images plugin defines gallery_plugin.json...
     **/
    loadPlugin(name) {
        if (name == "") { return false; }
        if (this.plugins.names.indexOf(name) > -1) {
            $(this).trigger('plugin_ready',name);
            return  true; 
        };
        console.info("Loading Plugin: "+name);
        var url = this.urls["_plugin_prefix"]+name+"/gallery_plugin.json"
        $.ajax({
            url:  url,
            method: 'GET',
            context: this,
            dataType: 'json'
            }).done(this._loadPlugin);
    }

    constructor() {
        super("GalleryViewer",{
                "offcanvas": "#offcanvasReview",
                "modal": "#newEntry_modal",
                "form": "#create_form",
                "home_on_success":false,
                "gallery_card_cls": ".gallery-card",


            },
            {
                "_api_prefix":"/gallery/api/",
                "_plugin_prefix":"/static/gallery/plugins/",
                "get_collection": "get/collection/",
                "get_all_collections": "get/all_collections/"
            }
        );
        //this.api_json_get(this.urls["get_all_collections"],this.load_all_collections_handle);
        var cards = $(this.settings["gallery_card_cls"]);
        var plugins = [];
        var count = 0;
        while (count < cards.length) {
            var pname = $(cards[count]).data('plugin');
            if (plugins.includes(pname) == false) {
                plugins.push(pname);
                this.loadPlugin(pname);
            };
            count = count+1;
        };
    }
}