window.dynapage_editor = Object({
   settings: {
       "factory_url":"/dynapages/api/factory/widget",
       "setup_url":"/dynapages/api/setup/widget",
       "setup_post_url":"/dynapages/api/setup/save_widget",
       "widgets":"#dynapage-widgets",
       "modal":"#dynapage_savedModal",
       "editModal": "#widget_form_modal",
       "editForm": "#widget_editor_form",
       "dropzones": ".drop-accept",
       "hint_class":".widget-area-hint",
       "widget_btn": "#widget_btn",
       "loadstr":'<span class="spinner-border text-primary" role="status"><span class="visually-hidden">Starting Widget...</span></span><span class="h6 text-muted">Starting Widget...</span></span>'
   },
   els: {
       'widgets': false,
       'edit_modal':false,
       'wofc': false,
       'dt':false,
       'de': false
   },
   editing: false,
   modal: false,
   edit_modal: false,
   widgets: false,
   _success: function(d) {
       if (d.res == "err") {
           alert(d.e);
       } else if (d == "ok") {
           dynapage_editor.modal.show();
       };
   },
   _widget_setup: function(d) {
       if (d ==  "ok") {
           target = dynapage_editor.els.de.data("widget_id");
           dynapage_editor._widget_factory(target);
       } else {
            $(dynapage_editor.settings.editModal+" .modal-body").html(d);
            dynapage_editor.edit_modal.show();
       };
   },
   _widget_factory: function(widget) {
       if (dynapage_editor.els.dt  != false) {
        html_el = $("<div class='widget bg-light'>");
        wtype =  dynapage_editor.els.dt.data("widget_type");
        wcol = dynapage_editor.els.dt.data("widget_col");
        if (wcol != "") {
            wtype = wtype + "?col="+wcol;
        };
        dynapage_editor.els.dt.append(html_el);
        html_el.html(dynapage_editor.settings.loadstr);
        html_el.load(dynapage_editor.settings.factory_url+"/"+widget+"/"+wtype);
       };
   },
   _save_handle: function(d) {
       if (d.res == "err") {
             alert(d.e);
          } else {
            html_el = $("<div class='widget bg-light'>");
            dynapage_editor.els.dt.append(html_el);
            html_el.html(d);
            dynapage_editor.edit_modal.hide();
        }
   },
   save_and_init: function() {
        data = $(this.settings.editForm).serialize();
        // console.info("Save and init. Data is:"+data);
        $.post(this.settings.setup_post_url,data,this._save_handle);
   },
   drag_start: function(e) {
        e.dataTransfer.setData("text/plain", e.target.id);
        // console.info("Drag Start",e);
   },
   drag_end: function(e) {
//        console.warn("Drag End",e);
        window.dtt = $(e.target);
        dynapage_editor.els.de = $(e.target);
        target = dynapage_editor.els.de.data("widget_id");
        wtype =  dynapage_editor.els.dt.data("widget_type");
        wcol = dynapage_editor.els.dt.data("widget_col");
        if (wcol == undefined) {
            wtype = wtype + "?col=A"
        } else if (wcol != "") {
            wtype = wtype + "?col="+wcol;
        };
        // console.warn("Drag End for Widget. type: "+wtype," Column: "+wcol,"Type: "+wtype);
        $.get(this.settings.setup_url+"/"+target+"/"+wtype,this._widget_setup);

   },
   drag_drop: function(e) {
       // Set the Drop Target:
       dynapage_editor.els.dt = $(e.target);
   },
   drag_allow: function(e) {
//        console.warn("Drag Allow",e);
       e.preventDefault();
   },
   /** These three functions start, stop, and toggle the editor from the webpage: **/
   start_edit: function() {
        $(this.settings.dropzones).addClass('active');
        $(this.settings.dropzones).on('drop',dynapage_editor.drag_drop);
        $(this.settings.dropzones).on('dragover',dynapage_editor.drag_allow);
        $(this.settings.hint_class).show();
        this.els.wofc.show();
   },
   stop_edit: function() {
        $(this.settings.dropzones).remove('active');
        $(this.settings.dropzones).on('drop',dynapage_editor.drag_drop);
        $(this.settings.dropzones).on('dragover',dynapage_editor.drag_allow);
        $(this.settings.hint_class).hide();
        this.els.wofc.hide();
   },
   toggle_widget_bar: function() {
     this.els.wofc.toggle();
   },
   toggle_editor: function() {
       if (this.editing == false) {
           // Not editing, we can start edition now:
           this.editing = true;
           this.start_edit();
        } else {
           this.editing = false;
           this.stop_edit();
        }
   },
   goSave: function() {
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.cressDomain) {
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
            }
        }
        });
       data = $(this.settings.form).serialize();
       $.post(this.settings.url,data,this._success);
   },


   init: function() {
       this.els.widgets = $(this.settings.widgets);
       this.els.edit_modal = $(this.settings.editModal);
       this.els.wofc = new bootstrap.Offcanvas(this.els.widgets);
       console.log(this.els.edit_modal);
       this.edit_modal =  new bootstrap.Modal(this.els.edit_modal);
       //this.start_edit();
       // console.log("Editor ready");

   }
});


