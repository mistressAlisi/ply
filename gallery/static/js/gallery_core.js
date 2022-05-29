window.gallery_core = Object({
    settings: {
        form_upload_url: "gallery/api/upload/get_form/",
        upload_url: "gallery/api/upload/post_upload/",
        upload_thumb_url: "gallery/api/upload/post_upload_thumbs/",
        upload_lt_url: "gallery/upload/lighttable/",
        review_panel_url: "/dashboard/user/gallery/api/upload/review_panel/",
        publish_url: "gallery/api/upload/publish/",
        get_collection_url: "/dashboard/user/gallery/api/get/items/",
        view_count_url: "/dashboard/user/gallery/api/view_counter/item",
        share_count_url: "/dashboard/user/gallery/api/share_counter/item",
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
        viewer_modal: "#gallery-viewer",
        viewer_title: "#title-span",
        viewer_info: "#gallery-span",
        viewer_hdr: ".gallery-modal-header",
        like_btn: "#btn-like",
        share_btn: "#btn-share",
        dl_btn: "#btn-download",
        views_btn: "#btn-views",
        com_btn: "#btn-comments",
        date_btn: "#btn-created",
        back_btn: "#back-button",
        forw_btn: "#forw-button",
        share_url_ctrl: "#id_share_url",
        share_url_fb: "#share_url_fb",
        sh_twitter: "#sh_twitter",
        sh_twitter_url: "https://twitter.com/intent/tweet?text=",
        sh_disc: "#sh_disc",
        sh_fb: "#sh_fb",
        sh_fb_url:"https://www.facebook.com/sharer/sharer.php?u=",
        sh_li: "#sh_li",
        sh_li_url: "https://www.linkedin.com/sharing/share-offsite/?url=",
        sh_tele: "#sh_tele",
        sh_tele_url:"https://t.me/share/url?url=",
        sh_recast_url: "/dashboard/user/gallery/api/recast",
        confirm_pub_modal: "#confirmModal",
        collection_cat: ".dashboard-category",
        gallery_card_cls: ".gallery-card",
        in_col_str: " <i>in collection:</i> ", 
        share_fb_str: "Copied to clipboard!",
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
    
    /** COLLECTION objects: Each collection holds the set of FILE objects and CARDS that represent a view. This is used for the vieweing functions. **/
    /** COLLections In View (cols_iv): **/
    _cols_iv: [],
    /** keys: **/
    _cols_iv_k: [],
    /** Counters: item count and open at: **/
    _cols_iv_ic: [],
    _cols_iv_oa: [],
    
    /** Canvas object: **/
    canvas_element: false,
    /** And control: **/
    canvas_visible: false,
    /** Navigation controls: **/
    nav: {
        count: 0,
        first: "",
        last: "",
        cards: [],
        current: false,
        colid: false
    },

/** Callback function for loadPlugin: **/
    _loadPlugin: function(d) {
        if (d == false) { return false; };
        if (d.type != "gallery-plugin") { 
            console.error("Wrong Datatype for Plugin!!"); 
            alert("Gallery Core can't load: "+d.name+". plugin.json has wrong type.");
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

    },
    
/** loadPlugin: Loads a plugin from the assets/plugins/ directory from the gallery plugin the file specified: The plugin must include a gallery_plugin.json that describes the css and js files to be loaded. **/
    loadPlugin: function(name) {
        if (name == "") { return false; }
        if (gallery_core._pLoaded.indexOf(name) > -1) {
            $(gallery_core).trigger('plugin_ready',name);
            return  true; 
        };
        console.log("Loading Plugin: "+name);
        $.get("/static/plugins/"+name+"/gallery_plugin.json",false,this._loadPlugin);
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
    /** These function enable fast, efficient collection navigation for the viewer: **/
    _setup_nav: function(colid) {
        col = $("#col-"+colid)
        cards = col.find(".gallery-card");
        count = 0;
        this.nav.cards = [];
        this.nav.colid = colid;
        this.nav.first = ($(cards[0])[0].id);
        while (count < cards.length) {
            this.nav.cards.push($(cards[count])[0].id);
            $(cards[count]).data('colpos',count);
            count = count +1;
        };
        this.nav.last = ($(cards[count-1])[0].id);
        this.nav.count = count -1;
        this.nav.current = false;
    },
    _step_back: function(ev) {
        ncst = this.nav.current-1;
        if (ncst < 0) {
            return false;
        };
        
        return this.nav.cards[ncst];
    },
    
    _step_forw: function(ev) {
        ncst = this.nav.current+1;
        if (ncst > this.nav.count) {
            return false;
        };
        return this.nav.cards[ncst];        
    },
    
    
    
    /** These functions enable Collection operations: **/
    _setup_col: function(data) {
        coldata =   data[0];
        /** only init if it hasn't happened before: **/
        if (gallery_core._cols_iv_k.includes(coldata.uuid) == false) {
            console.info("Setting up Collection: "+coldata.uuid);
            // Initialise data structs: **/
            gallery_core._cols_iv_k.push(coldata.uuid);
            gallery_core._cols_iv[coldata.uuid] = [];
            gallery_core._cols_iv_ic[coldata.uuid] = 0;
            gallery_core._cols_iv_oa[coldata.uuid] = 0;
            /** Now begin setting up the collections: **/
            ilen = coldata.items.length;
            count = 0;
            while (count < ilen) {
                itm = data[0].items[count];
                // Find the card and pass it to the plugin:
                the_card = $("#card-"+coldata.uuid+"-"+itm.id);
                if (the_card.length == 1) {
                    console.info("Item: "+itm.id+" Found Card: setting up plugin viewer: "+itm.plugin);
                    card_contents = gallery_core.plugins[itm.plugin].setup_card_view(the_card[0],itm);
                    if (card_contents != false) {
                        // Add item to collection for full view:
                        gallery_core._cols_iv[coldata.uuid].push(card_contents);
                        gallery_core._cols_iv_ic[coldata.uuid] = gallery_core._cols_iv_ic[coldata.uuid] + 1;
                     
                        // Initialise collection FULL SCREEN view here:
                    
                        //$(gallery_core.settings.review_panel).offcanvas('show');
                    };
                
                }
                count = count+1;
            };
            /** Launch the item from the hash provided; if it matches the collection: **/
            if (location.hash.substr(6,36) == coldata.uuid) {
                gallery_core.launch_card_from_location();
            };
        };
    },
    /** Launch galleries AFTER plugins are loaded : **/
    _launch_gallery: function() {
         $(gallery_core).off('plugin_ready');
        items = $(this.settings.collection_cat);
        ilen = items.length;
        count = 0;
        while (count < ilen) {
            colid = ($(items[count]).data('col'));
            if (colid != undefined) {
                if (gallery_core._cols_iv_k.includes(colid) == false) {
                    console.log("Loading col_iv_k: "+colid);
                    $.get(gallery_core.settings.get_collection_url+colid,this._setup_col);            
                } else {
//                     console.log("Launch NAO");
                };
            }
        count = count +1;
        };

    },
   
    
     /** Init plugins then galleries (full init... ONLY CALL ONCE!): **/
     launch_gallery_init: function() { 
        
         cards = $(gallery_core.settings.gallery_card_cls);
         clen = cards.length;
         count = 0;
         plugs = []
         while (count < clen) {
             plugin = ($(cards[count]).data('plugin'));
             if (plugs.includes(plugin) == false) {
                if (plugin != undefined) {
                    gallery_core.loadPlugin(plugin);
                }; 
                plugs.push(plugin);
             };
         
         count = count + 1;
        };
        $(gallery_core).on('plugin_ready',gallery_core._launch_gallery);            
     },
    toggle_viewer: function(e) {
            if (this.canvas_visible == false) {
                this.canvas_visible = true;
                this.canvas_element.css('display','block');
                $(window).bind('keydown',window.gallery_core._kbk_evh);
            } else {
                this.canvas_visible = false;
                this.canvas_element.css('display','none');
                $(window).unbind('keydown',window.gallery_core._kbk_evh);
                location.hash = "";
            }
    },
    /** These function handles key bindings for the viewer: **/
    _kbk_evh: function(e) {
        if (e.key === "Escape") {
            
            window.gallery_core.toggle_viewer();
            return;
        };
        switch(e.which) {
        case 37: // left
            if ($(window.gallery_core.settings.viewer_hdr).hasClass('hover') == false) {
                $(window.gallery_core.settings.viewer_hdr).addClass('hover');
            }
            window.gallery_core.gallery_card_back();
        break;

        case 39: // right
            if ($(window.gallery_core.settings.viewer_hdr).hasClass('hover') == false) {
                $(window.gallery_core.settings.viewer_hdr).addClass('hover');
            }
            window.gallery_core.gallery_card_forw();
        break;

        case 40: // down
        break;

        default: 
            
            return; // exit this handler for other keys
        }
        if ($(window.gallery_core.settings.viewer_hdr).hasClass('hover') == true) {
            window.setTimeout(function(){$(window.gallery_core.settings.viewer_hdr).removeClass('hover')},100);
        }
        e.preventDefault();
    },
     /** This function _renders_ a gallery card's metadata: **/
     _gallery_card_meta: function(target_card,col,item) {
         /** Send metadata and metrics to server: **/
         $.get(this.settings.view_count_url+"/?itm="+item+"&col="+target_card.data("collection"));
          /** Update viewer data: **/
                /** Load Counts: **/
                    $(this.settings.com_btn).find('.count').html(target_card.data("comments"));
                    $(this.settings.like_btn).find('.count').html(target_card.data("likes"));
                    $(this.settings.share_btn).find('.count').html(target_card.data("shares"));
                    $(this.settings.dl_btn).find('.count').html(target_card.data("downloads"));
                    $(this.settings.views_btn).find('.count').html(target_card.data("views"));
                    /** Date: **/
                    $(this.settings.date_btn).find('.date').html(target_card.data("created"));
                    /** Now set title: **/
                    $(this.settings.viewer_title).html(target_card.data("title"));
                    /** And construct the info bar: **/
                    author_str = "by "+target_card.data("author")
                    collabel = target_card.data("collabel")
                    if (collabel != "") {
                        author_str = author_str +this.settings.in_col_str+collabel;
                    };
                    $(this.settings.viewer_info).html(author_str);
                    
                    /** Avatar: **/
                    avstr = target_card.data("avatar");
                    if (avstr !="") {
                        $(this.settings.viewer_modal).find('.avatar')[0].src=avstr;
                    };
                    /** Navigation controls: **/

                    this.nav.current = target_card.data('colpos');
//                     console.warn(this.nav);
                    if (this.nav.count >= 1) {
                        if (target_card[0].id == this.nav.first) {
                            $(this.settings.viewer_modal).find(this.settings.back_btn).css('display','none');
                        } else {
                            $(this.settings.viewer_modal).find(this.settings.back_btn).css('display','block');
                        };
                        if (target_card[0].id == this.nav.last) {
                            $(this.settings.viewer_modal).find(this.settings.forw_btn).css('display','none');
                        } else {
                            $(this.settings.viewer_modal).find(this.settings.forw_btn).css('display','block');
                        };
                    } else {
                        
                         $(this.settings.viewer_modal).find(this.settings.back_btn).css('display','none');
                         $(this.settings.viewer_modal).find(this.settings.forw_btn).css('display','none');
                    }
                    /** Share link: **/
                   share_str = location.origin+"/g/"+target_card.data("profile_id")+"/"+target_card.data("collection")+"/"+target_card.data("item");
                   $(this.settings.share_url_ctrl)[0].value = share_str;
                   $(this.settings.sh_twitter)[0].href = this.settings.sh_twitter_url+encodeURIComponent(share_str);
                   $(this.settings.sh_li)[0].href = this.settings.sh_li_url+encodeURIComponent(share_str);
                   $(this.settings.sh_fb)[0].href = this.settings.sh_fb_url+encodeURIComponent(share_str);
                   $(this.settings.sh_tele)[0].href = this.settings.sh_tele_url+encodeURIComponent(share_str);
                   $(this.settings.share_url_ctrl).data("i",target_card.data("item"));
                   $(this.settings.share_url_ctrl).data("c",target_card.data("collection"));
                    //this._set_page_meta(target_card.data("title"),location.toString(),target_card.find('.card-img-top')[0].src,target_card.data("title")+" "+author_str);
     },
    /** will copy the share url contents to clipboard; and create a 'shared' metric: **/
    share: function(e) {
        $(this.settings.share_url_ctrl).select();
        document.execCommand('copy');
        $(this.settings.share_url_fb).text(this.settings.share_fb_str);
        $.get(this.settings.share_count_url+"/?itm="+$(this.settings.share_url_ctrl).data("i")+"&col="+$(this.settings.share_url_ctrl).data("c"));
        
    },
    /** Recasting: will publish to the stream, "share to ply", and create a 'recast' metric: **/
     recast: function() {
         $.get(this.settings.sh_recast_url+"/"+$(this.settings.share_url_ctrl).data("c")+"/"+$(this.settings.share_url_ctrl).data("i"));
     },
     /** This function launches a gallery from a card: **/
     launch_gallery_card: function(e) {
         target_card = this._parent_walker(e.target,"DIV");
         col = target_card.data("collection");
         item = target_card.data("item");
         //console.warn(target_card,col,item);
        /** Find the Collection and Item, fetch the item: **/
        if (this._cols_iv_k.includes(col) == true) {
            itm_o = false;
            for (i in this._cols_iv[col]) {
                if (this._cols_iv[col][i].item == item) {
                    itm_o = this._cols_iv[col][i];
                    target_card.data("i",i);
                    //console.warn("IV@LOAD",col,i,item,itm_o);
                };
            };
                if (itm_o != false) {
                    console.info("Starting item: "+item+"in Collection: "+col+"...");
                    location.hash = "#card-"+col+"-"+item;
                    /** Now, call the plugin for the card and request a first the rendering of the canvas.. **/
                    if (this.canvas_element == false) {
                        this.canvas_element = $(this.settings.viewer_modal);
                    };
                    //console.warn(item);
                    this._setup_nav(col);
                    this._gallery_card_meta(target_card,col,item);

                    /** Now render the contents: **/
                    render_card = this.plugins[itm_o.plugin].render_view(itm_o);
                    if (render_card == true) {
                        /** UNLESS WE DISABLE THE VIEWER TOGGLE: **/
//                         if (dv != true) {
                            this.toggle_viewer();
//                         };
                    };
                };
        
        } else {
            console.warn("Unable to Start Collection: "+col+" for item card: "+item);
            return false;
        }
         
     },
     /** This function steps a card backward: **/
     gallery_card_back: function() {
         bk_crd = this._step_back();
//          console.log(bk_crd);
         target_card = $("#"+bk_crd);
         
         col = this.nav.colid;
         plugin = target_card.data("plugin");
         item = target_card.data("item");
         
         /** Find the Collection and Item, fetch the item: **/
         if (this._cols_iv_k.includes(col) == true) {
            itm_o = false;
            for (i in this._cols_iv[col]) {
                if (this._cols_iv[col][i].item == item) {
                    itm_o = this._cols_iv[col][i];
                    target_card.data("i",i);
                };
            };
        if (itm_o != false) {
//          console.warn(itm_o);
         this._gallery_card_meta(target_card,col,item);
        /** Now render the contents: **/
        location.hash = "#card-"+col+"-"+item;
        render_card = this.plugins[itm_o.plugin].render_view(itm_o);0
        if (render_card == false) {
            console.error("RenderCard went wrong!");
            console.error(render_card);
        }};
        } else {
            console.warn("Unable to Step Collection: "+col+" back into item card: "+item);
         };
     },
    
     /** This function steps a card forward: **/
     gallery_card_forw: function() {
         bk_crd = this._step_forw();
//          console.log(bk_crd);
         target_card = $("#"+bk_crd);
         
         col = this.nav.colid;
         plugin = target_card.data("plugin");
         item = target_card.data("item");
         
         /** Find the Collection and Item, fetch the item: **/
         if (this._cols_iv_k.includes(col) == true) {
            itm_o = false;
            for (i in this._cols_iv[col]) {
                if (this._cols_iv[col][i].item == item) {
                    itm_o = this._cols_iv[col][i];
                    target_card.data("i",i);
                };
            };
        if (itm_o != false) {
//          console.warn(itm_o);
         this._gallery_card_meta(target_card,col,item);
         location.hash = "#card-"+col+"-"+item;
        /** Now render the contents: **/
        render_card = this.plugins[itm_o.plugin].render_view(itm_o);
        if (render_card == false) {
            console.error("RenderCard went wrong!");
            console.error(render_card);
        }};
        } else {
            console.warn("Unable to Step Collection: "+col+" back into item card: "+item);
         };
     },
     /** Convenience function to handle #hash locations and open the viewer: **/
     launch_card_from_location: function() {
         lhash = location.hash;
         lhash_crd = $(lhash);
         if (lhash_crd['length'] > 0) {
             lhash_crd[0].click();
         }
     },


    /********************/
    /** These functions enable you to PUBLISH/edit items: **/
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
            gallery_core.editor.bound = true;
        };   

        gallery_core.loadPlugin(gallery_core.editor.plugin);
        
    },
    _trig_save_publish: function(e) {
        review_pub_ok = gallery_core.plugins[gallery_core.editor.plugin].prepare_publish();
                if (review_pub_ok == true) {
                    gallery_core._save_publish();
                } else {
                    $(gallery_core.settings.confirm_pub_modal).modal('hide');
                }
    },
    _save_publish: function(e) {
        data = $("#form-"+gallery_core.editor.file).serialize();
        if (data != false) {
        $.post(gallery_core.settings.publish_url+gallery_core.editor.file,data,function(){
            $(gallery_core.settings.confirm_pub_modal).modal('hide');
            $(gallery_core.settings.review_panel).offcanvas('hide');
            $("#card-"+gallery_core.editor.file).addClass('published');
            $("#card-"+gallery_core.editor.file).off('click');
        });
        }
    },
    save_publisher_changes: function(e) {
        review_pub_ok = gallery_core.plugins[gallery_core.editor.plugin].prepare_publish();
        if (review_pub_ok == true) {
            $(gallery_core.settings.confirm_pub_modal).modal('show');
        }
    }
});

