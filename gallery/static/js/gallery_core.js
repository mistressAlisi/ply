window.gallery_core = Object({
    settings: {
        form_upload_url: "gallery/api/upload/get_form/",
        upload_url: "gallery/api/upload/post_upload/",
        upload_thumb_url: "gallery/api/upload/post_upload_thumbs/",
        upload_lt_url: "gallery/upload/lighttable/",
        review_panel_url: "gallery/api/upload/review_panel/",
        publish_url: "gallery/api/upload/publish/",
        desc_div: "#content_submission_type_desc",
        create_start_btn: "#create_start_btn",
        all_buttons: ".gallery-content-button",
        button_active_class:'btn-primary',
        button_inactive_class:'btn-secondary',
        form_id: "#upload_submission_form",
        upload_id: "#upload-files-widget",
        main_panel: "#dashboard_mainPanel",
        review_panel: "#review_controls",
        sidebar_panel: "#nav",
        confirm_pub_modal: "#confirmModal",
        max_upload_size: 25600,
    },
    editor: {
        file:"",
        plugin:"",
        url:"",
        bound: false
    },
    /** Plugin Control: _pLoaded keeps track of loaded plugins by name to prevent reinitialisation. Plugins that need to extend dashboard can register themselves into the plugins object below: **/
    _pLoaded: [],
    plugins: [],
/** Callback function for loadPlugin: **/
    _loadPlugin: function(d) {
        if (d == false) { return false; };
        if (d.type != "gallery-plugin") { 
            console.error("Wrong Datatype for Plugin!!"); 
            alert("Gallery Core can't load: "+plugin+". plugin.json has wrong type.");
            return false;
        };
        /** load javascript: **/
        jsl = d.js.length;
        if (jsl > 0) {
          count = 0;
          while (count < jsl) {
              jsp = "/static/plugins/"+d.name+"/js/"+d.js[count];
              console.info("Gallery Core Loading Plugin JS: "+jsp);
              $.getScript(jsp);
              count++;
        }};
        /** load css: **/
        csl = d.css.length;
        if (csl > 0) {
          count = 0;
          while (count < csl) {
              csp = "/static/plugins/"+d.name+"/css/"+d.css[count];
              console.info("Gallery Core Loading Plugin CSS: "+csp);
              $('head').append( $('<link rel="stylesheet" type="text/css" />').attr('href', csp));
              count++;
        }};
        gallery_core._pLoaded.push(d.name);
        $(gallery_core).trigger('plugin_ready',d.name);
    },
    
/** loadPlugin: Loads a plugin from the assets/plugins/ directory from the gallery plugin the file specified: The plugin must include a gallery_plugin.json that describes the css and js files to be loaded. **/
    loadPlugin: function(name) {
        if (name == "") { return false; }
        if (gallery_core._pLoaded.indexOf(name) > -1) {
            $(gallery_core).trigger('plugin_ready',name);
            return  true; 
        };
        console.log("Loading Plugin: "+name);
        $.get("/static/plugins/"+name+"/gallery_plugin.json",false,window.gallery_core._loadPlugin);
    },
    _parent_walker: function(parent,target_node) {
       if (target_node == undefined) { target_node = "DIV"};
       while (parent.nodeName != target_node) {
            parent = parent.parentElement;
        };
        return $(parent);
        
    },
    set_type_desc: function(e) {
        target = gallery_core._parent_walker($(e.target)[0],"BUTTON");
        $(gallery_core.settings.all_buttons).addClass(gallery_core.settings.button_active_class);
        target.addClass(gallery_core.settings.button_active_class);
        target.removeClass(gallery_core.settings.button_inactive_class);
        $(gallery_core.settings.desc_div)[0].innerHTML = target.data('desc');
        $(gallery_core.settings.create_start_btn)[0].disabled = null;
        gallery_core.content_plugin = target.data("plugin");
    },

    load_upload_form: function(e) {
        e.preventDefault();
        $(gallery_core.settings.form_id).load(gallery_core.settings.form_upload_url+gallery_core.content_plugin);
    },
    start_file_upload_wdgt: function(extensions,csrf,plugin,max_size=0) {
        if (max_size != 0) {
            size =  max_size;
        } else {
            size = gallery_core.settings.max_upload_size;
        };
        $(gallery_core.settings.upload_id).fileinput({
            allowedFileExtensions: extensions,
            maxFileSize: size,
            uploadUrl: gallery_core.settings.upload_url,
            uploadExtraData: { "csrfmiddlewaretoken": csrf, "plugin": plugin }
            
        });
       $(gallery_core.settings.upload_id).on('filebatchuploadcomplete', function(event, preview, config, tags, extraData) {
         $(gallery_core.settings.form_id).empty()
         $(gallery_core.settings.main_panel).load(gallery_core.settings.upload_lt_url);
        });
    },
    _launch_publisher: function() {
        $(gallery_core.settings.review_panel).load(gallery_core.editor.url,function(e){
                review_setup_ok = gallery_core.plugins[gallery_core.editor.plugin].prepare_review();
                if (review_setup_ok == true) {
                    $(gallery_core.settings.review_panel).offcanvas('show');
                };
        });
        
    },
    launch_publisher: function(e) {
        $(gallery_core.settings.sidebar_panel).offcanvas('hide');
        target = gallery_core._parent_walker($(e.target)[0],"DIV");
        //console.log(target);
        //window.ttt = target;
        gallery_core.editor.file = target.data('file');
        gallery_core.editor.plugin = target.data('plugin');
        gallery_core.editor.url = gallery_core.settings.review_panel_url+target.data('file');
        if (gallery_core.editor.bound == false) {
            $(gallery_core).on('plugin_ready',gallery_core._launch_publisher);            
            gallery_core.editor.bound =true;
        };   

        gallery_core.loadPlugin(gallery_core.editor.plugin);
        
    },
    _save_publish: function(e) {
        data = $("#form-"+gallery_core.editor.file).serialize();
        $.post(gallery_core.settings.publish_url+gallery_core.editor.file,data,function(){
            $(gallery_core.settings.confirm_pub_modal).modal('hide');
            $(gallery_core.settings.review_panel).offcanvas('hide');
            $("#card-"+gallery_core.editor.file).addClass('published');
            $("#card-"+gallery_core.editor.file).off('click');
        });
         
    },
    save_publisher_changes: function(e) {
        $(gallery_core.settings.confirm_pub_modal).modal('show');
    },
});
