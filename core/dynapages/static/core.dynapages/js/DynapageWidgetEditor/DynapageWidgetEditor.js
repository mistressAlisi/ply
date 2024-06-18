import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class DynapageWidgetEditor extends AbstractDashboardApp {
   editing= false;
   modal= false;
   edit_modal= false;
   widgets = false;
   page_uuid = false;
   settings=  {
       "factory_url":"/dynapages/api/factory/widget",
       "setup_url":"/dynapages/api/setup/widget",
       "setup_post_url":"/dynapages/api/setup/save_widget",
       "widgets":"#dynapage-widgets",
       "widget_card_class":"card widget-card badge bg-primary text-wrap",
       "widget_card_selclass":".widget-card",
       "modal":"#dynapage_savedModal",
       "editModal": "#widget_form_modal",
       "editForm": "#widget_editor_form",
       "dropzones": ".drop-accept",
       "hint_class":".widget-area-hint",
       "widget_btn": "#widget_btn",
       "loadstr":'<span class="spinner-border text-primary" role="status"><span class="visually-hidden">Starting Widget...</span></span><span class="h6 text-muted">Starting Widget...</span></span>'
   }

   els = {
           'widgets': false,
           'edit_modal': false,
           'wofc': false,
           'dt': false,
           'de': false
   }

   _success(d) {
       if (d.res == "err") {
           alert(d.e);
       } else if (d == "ok") {
           this.modal.show();
       }
   }
   _widget_setup(d) {
       if (d ==  "ok") {
           var target = this.els.de.data("widget_id");
           this._widget_factory(target);
       } else {
            $(this.settings.editModal+" .modal-body").html(d);
            this.edit_modal.show();
       }
   }
    _enableWidgetDrag() {
       $(this.settings["widget_card_selclass"]).each(function(i,e){e.draggable=true});
    }
    _disableWidgetDrag() {
       $(this.settings["widget_card_selclass"]).each(function(i,e){e.draggable=false});
    }
   _createWidgetCard(uuid,widget) {
        var card = this.widget_factory.create_generic_card("widget_card_",uuid,widget.icon,widget.label,widget.descr,this.settings["widget_card_class"]);
        card.data("widget_id",widget.widget_id);
        card.data("widget_uuid",uuid);
        card.data("widget_type",widget.widget_name);
        card.on('dragstart',$.proxy(this.drag_start,this));
        card.on('dragend',$.proxy(this.drag_end,this));
        // Don't forget to enable draggable after adoption!
        //         card.draggable = true;

        return card;

   }
   _widget_factory(widget) {
       if (this.els.dt  != false) {
        var html_el = $("<div class='widget bg-light'>");
        var wtype =  this.els.dt.data("widget_type");
        var wcol = this.els.dt.data("widget_col");
        if (wcol != undefined) {
            var wtype = wtype + "?col="+wcol;
        };
        this.els.dt.append(html_el);
        html_el.html(this.settings.loadstr);
        html_el.load(this.settings.factory_url+"/"+this.page_uuid+"/"+widget+"/"+wtype);
       }
   }
   _save_handle(d) {
       if (d.res == "err") {
             alert(d.e);
          } else {
            var html_el = $("<div class='widget bg-light'>");
            this.els.dt.append(html_el);
            html_el.html(d);
            this.edit_modal.hide();
        }
   }
   save_and_init() {
        var data = $(this.settings.editForm).serialize();
        // console.info("Save and init. Data is:"+data);
        $.post(this.settings.setup_post_url+"/"+this.page_uuid,data,this._save_handle);
   }
   drag_start(e) {
         //e.dataTransfer.setData("text/plain", e.target.id);
         //console.info("Drag Start",e);
   }
   drag_end(e) {
        //console.warn("Drag End",e);

        this.els.de = $(e.target);
        var target = this.els.de.data("widget_id");
        var wtype =  this.els.dt.data("widget_type");
        var wcol = this.els.dt.data("widget_col");
        if (wcol == undefined) {
            var wtype = wtype + "?col=A";
        } else if (wcol != "") {
            var wtype = wtype + "?col="+wcol;
        }
        // console.warn("Drag End for Widget. type: "+wtype," Column: "+wcol,"Type: "+wtype);
        $.get(this.settings["setup_url"]+"/"+target+"/"+wtype,$.proxy(this._widget_setup,this));

   }
   drag_drop(e) {
       // Set the Drop Target:
       //console.warn('Drag Drop!',e);
       var trgt = $(e.target);
       if (trgt.hasClass("drop-accept") == true) {
        this.els.dt = trgt;
       } else {
        this.els.dt = trgt.parent(".drop-accept");
       }

   }
   drag_allow(e) {
       //console.log("Drag Allow",e);
       e.preventDefault();
   }
   /** These three functions start, stop, and toggle the editor from the webpage: **/
   start_edit() {
        $(this.settings["dropzones"]).addClass('active');
        $(this.settings["dropzones"]).on('drop',$.proxy(this.drag_drop,this));
        $(this.settings["dropzones"]).on('dragover',$.proxy(this.drag_allow,this));
        $(this.settings["hint_class"]).show();
        this._showOffcanvas();
        this._enableWidgetDrag();
   }
   stop_edit() {
        $(this.settings["dropzones"]).removeClass('active');
        $(this.settings["dropzones"]).off('drop');
        $(this.settings["dropzones"]).off('dragover');
        $(this.settings["hint_class"]).hide();
        this._disableWidgetDrag();
        this._hideOffcanvas();

   }
   toggle_widget_bar() {
     this._toggleOffcanvas();
   }
   toggle_editor() {
       if (this.editing == false) {
           // Not editing, we can start edition now:
           this.editing = true;
           this.start_edit();
        } else {
           this.editing = false;
           this.stop_edit();
        }
   }
   goSave() {
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.cressDomain) {
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
            }
        }
        });
       var data = $(this.settings.form).serialize();
       $.post(this.settings.url,data,this._success);
   }


   constructor(name,settings={}) {
       super('DynapageWidgetEditor',settings);
       $.extend(this.settings,settings);
       //this.els.widgets = $(this.settings.widgets);
       //this.els.edit_modal = $(this.settings.editModal);
       //this.els.wofc = new bootstrap.Offcanvas(this.els.widgets);
       //console.log(this.els.edit_modal);
       //this.edit_modal =  new bootstrap.Modal(this.els.edit_modal);
       //this.start_edit();

   }
}