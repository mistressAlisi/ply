window.gallery_core_editor = Object({
    settings: {
        manage_modal: "#manageModal",
        invis_class: "archived",
        invis_url: "/dashboard/user/gallery/api/toggle/invis",
        copymove_url:"/dashboard/user/gallery/api/copymove/form",
        copymove_exec_url:"/dashboard/user/gallery/api/copymove/form/exec",
        copymove_form: "#copy_move_form",
        remove_url:"/dashboard/user/gallery/api/remove/item/form",
        remove_exec_url:"/dashboard/user/gallery/api/remove/item/form/exec",
        remove_form: "#remove_form",
        set_url:"/dashboard/user/gallery/api/settings/item/form",
        set_exec_url:"/dashboard/user/gallery/api/settings/item/form/exec",
        set_form: "#settings_form",
        meta_url: "/dashboard/user/gallery/api/metadata/item",
        det_url:"/dashboard/user/gallery/api/details/item/form",
        det_exec_url:"/dashboard/user/gallery/api/details/item/form/exec",
        det_form: "#settings_form",
    },
    /** The management Modal: **/
    mod: false,
    mod_bs: false,
    target_crd: false,
    /** Toggle an item visible/publish: **/

    _m_invis_h: function(d) {
        if (d == "invis") {
            window.gallery_core_editor.target_crd.addClass(gallery_core_editor.settings.invis_class);
        } else if (d == "vis") {
            window.gallery_core_editor.target_crd.removeClass(gallery_core_editor.settings.invis_class);
        } else {
            if (d.res == "err") {
                alert(d.err);
            }
        };
        this.target_crd = false;
    },
    t_visible: function(cid,id) {
        this.target_crd = $("#card-"+cid+"-"+id);
        $.get(this.settings.invis_url+"/"+id,this._m_invis_h);
    },
    /** Show an item's metadata: **/
    metadata: function(cid,id) {
        this.mod_bs.show();
    },


    _cpmv_h: function(d) {
        if (d=="ok") {
            gallery_core_editor.mod_bs.hide();
            dc_reloadPanel();
        } else {
             if (d.res == "err") {
                alert(d.err);
            }
        };
    },
    /** exec copy/move: **/
    _exec_cpmv: function(e) {
        data = $(this.settings.copymove_form).serialize();
        $.post(this.settings.copymove_exec_url,data,this._cpmv_h);
        return false;
    },
     /** (The callback to; and) Show the copy/move dialogue: **/
    _copy_move_h: function(d) {
            gallery_core_editor.mod_bs.show();
    },

    copy_move: function(cid,id) {
        this.target_crd = $("#card-"+cid+"-"+id);
        this.mod.find('.modal-title').html('Copy/move to Collection');
        mod_body = this.mod.find('.modal-body');
        mod_body.load(this.settings.copymove_url+"/"+id+"/"+cid,false,this._copy_move_h);

    },
    /** exec remove handle: **/
    _rm_h: function(d) {
        if (d=="ok") {
            gallery_core_editor.mod_bs.hide();
            dc_reloadPanel();
        } else {
             if (d.res == "err") {
                alert(d.err);
            }
        };
    },
    /** exec copy/move: **/
    _exec_rm: function(e) {
        data = $(this.settings.remove_form).serialize();
        $.post(this.settings.remove_exec_url,data,this._rm_h);
        return false;
    },
    /** (The callback to; and) Show the remove dialogue: **/
    _remove_h: function(d) {
            gallery_core_editor.mod_bs.show();
    },

    remove: function(cid,id) {
        this.target_crd = $("#card-"+cid+"-"+id);
        this.mod.find('.modal-title').html('Remove Item?');
        mod_body = this.mod.find('.modal-body');
        mod_body.load(this.settings.remove_url+"/"+id+"/"+cid,false,this._remove_h);

    },


    /** exec settings handle: **/
    _set_h: function(d) {
        if (d=="ok") {
            gallery_core_editor.mod_bs.hide();
            dc_reloadPanel();
        } else {
             if (d.res == "err") {
                alert(d.err);
            }
        };
    },
    /** exec settings: **/
    _exec_set: function(e) {
        data = $(this.settings.set_form).serialize();
        $.post(this.settings.set_exec_url,data,this._set_h);
        return false;
    },
    /** (The callback to; and) Show the settings dialogue: **/
    _settings_h: function(d) {
            gallery_core_editor.mod_bs.show();
    },

    itm_settings: function(cid,id) {
        this.target_crd = $("#card-"+cid+"-"+id);
        this.mod.find('.modal-title').html('Item Settings');
        mod_body = this.mod.find('.modal-body');
        mod_body.load(this.settings.set_url+"/"+id+"/"+cid,false,this._settings_h);

    },

    /** (The callback to; and) Show the Metadata dialogue: **/
    _metadata_h: function(d) {
            gallery_core_editor.mod_bs.show();
    },

    metadata: function(cid,id) {
        this.target_crd = $("#card-"+cid+"-"+id);
        this.mod.find('.modal-title').html('Item Metadata');
        mod_body = this.mod.find('.modal-body');
        mod_body.load(this.settings.meta_url+"/"+id+"/"+cid,false,this._metadata_h);

    },


    /** (The callback to; and) Show the details dialogue: **/
    _det_h: function(d) {
        /** Smart Select for Categories: */
            sse = new smart_select('#gr_keywords',
            {
                f_option_load: function(query,callback) {
                    if (!query.length) return callback();
                        $.ajax({
                            url: '/keywords/api/get/' + encodeURIComponent(query),
                            type: 'GET',
                            error: function() {
                            callback();
                            },
                        success: function(res) {

                            callback(res);
                            }});
                },


            });
            gallery_core_editor.mod_bs.show();
    },

    /** exec details save handle: **/
    _dt_h: function(d) {
        if (d=="ok") {
            gallery_core_editor.mod_bs.hide();
            dc_reloadPanel();
        } else {
             if (d.res == "err") {
                alert(d.err);
            }
        };
    },
    /** exec details save: **/
    _exec_dt: function(e) {
        data = $(this.settings.remove_form).serialize();
        $.post(this.settings.det_exec_url,data,this._dt_h);
        return false;
    },
    details: function(cid,id) {
        this.target_crd = $("#card-"+cid+"-"+id);
        this.mod.find('.modal-title').html('Item Details');
        mod_body = this.mod.find('.modal-body');
        mod_body.load(this.settings.det_url+"/"+id+"/"+cid,false,this._det_h);

    },

    /** Init management UI elements: ONLY CALL ONCE! **/
    manage_init: function() {
        this.mod = $(this.settings.manage_modal);
        this.mod_bs = new bootstrap.Modal(this.mod);
    }
});

