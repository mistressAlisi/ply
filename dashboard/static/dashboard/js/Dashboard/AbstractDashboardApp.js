import { WidgetFactory } from "/static/core.plyui/js/WidgetFactory/WidgetFactory.js";
export class AbstractDashboardApp {
    _appName = "app"
    settings = {
        "offcanvas":false,
        "offcanvas_body":"#ofccontents",
        "modal":"#some_modal",
        "form":"#some_form",
        "home_on_success":true,
        "success_hdr":"Success!",
        "success_body":"Operation Complete!"
    }
    urls = {
            "_api_prefix":"",
            "_prefix":"",
            "submit":"/some/url",
            "load_edit":"/some/url/"
    }
    modal = false
    offcanvas = false
    widget_factory =  false
    urls = []
    elements = []

    _is_uuid(uuid) {
        let s = "" + uuid;
        s = s.match('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$');
        if (s === null) {
          return false;
        }
        return true;
    }

    _parent_walker(parent,target_node) {
       if (target_node == undefined) { target_node = "DIV"};
       while (parent.nodeName != target_node) {
            parent = parent.parentElement;
        };
        return $(parent);

    }

    _parse_ajax_error(data) {
        var errStr="";
                var errors = data.e;
                for (var eks in errors) {
                    if (typeof(errors[eks][0]) != "string") {
                        errStr = errStr + " <em>" + eks + "</em>: " + errors[eks][0]["message"] + "<br/>";
                    } else {
                        errStr = errStr + " <em>" + eks + "</em>: " + errors[eks][0] + "<br/>";
                    }
                    $(this.elements["form"]).find("#id_"+eks).addClass('is-invalid');
                }
        return errStr;
    }
    _submitHandle(data,stat,home=true) {
        var msg = ""
        if ((data.res == "ok")||(data.res=="notice")) {
                if (data.res == "ok") {
                    msg = this.settings["success_body"];
                } else {
                    msg = data.msg;
                }
                dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;'+this.settings["success_hdr"],msg);
                if ((home == true) && (this.settings["home_on_success"] == true)) {
                    dashboard.panel_home();
                } else {
                    dashboard.dc_reloadPanel();
                }
                return true;

            } else {
                var errStr= this._parse_ajax_error(data);
                dashboard.errorToast('<h5 class="text-danger"><i class="fa-solid fa-xmark"></i>&#160;Error!','<strong>An Error Occurred:</strong><br/>'+errStr);
                console.error("Unable to execute Operation: ",errStr)
                return false;
            }
    }

    _getModal() {
        this.modal =  new bootstrap.Modal(this.elements["modal"]);
    }

    _showModal() {
        if (this.modal == false) {
            this._getModal();
        }
        this.modal.show();
    }
    _hideModal() {
        if (this.modal == false) {
            this._getModal();
        }
        this.modal.hide();
    }
    _clear_invalid() {
        $(this.elements["form"]).find("input").removeClass('is-invalid');
        $(this.elements["form"]).find("select").removeClass('is-invalid');
    }

    api_json_get(url,handle,data=false) {
        if (this.urls["_api_prefix"] != "") {
            url = this.urls["_api_prefix"] + url;
        }
         $.ajax({
            url:  url,
            data:     data,
            method: 'GET',
            context: this,
            dataType: 'json'
            }).done(handle);
    }
    api_fill_el_html(element,url,handle,data) {
        if (this.urls["_prefix"] != "") {
            url = this.urls["_prefix"] + url;
        }
        $(element).load(url,data,handle);
    }
    api_html_get(url,handle,data=false) {
        if (this.urls["_api_prefix"] != "") {
            url = this.urls["_api_prefix"] + url;
        }
         $.ajax({
            url:  url,
            data:     data,
            method: 'GET',
            context: this,
            dataType: 'html'
            }).done(handle);
    }

    add() {
        this._showModal();
    }
    submit(url=false,form=false,handle=false,disable_prefix=false) {
            if (url == false) {
                url = this.urls["submit"];
            }
            if (disable_prefix == false) {
                 if (this.urls["_api_prefix"] != "") {
                    url = this.urls["_api_prefix"] + url;
                }
            }
            if (form == false) {
                form = $(this.elements["form"]);
            }
            if (handle == false) {
                handle = this._submitHandle;
            }
            this._clear_invalid();
            console.info("Submitting Dashboard App Data: URL '"+url+"'");
            $.ajax({
            url:  url,
            data:     form.serialize(),
            method: 'POST',
            context: this
            }).done(handle);


    }


    _edit_form_loader(data) {
        var data_keys = Object.keys(data.data);
            for (var i in data_keys) {
                var dk = data_keys[i];
                var update_el = $(this.elements["form"]).find("#id_"+dk);
                if (update_el.length > 0) {
                    update_el[0].value = data.data[dk];
                }
           }
    }
    _edit_handle(data,edit_function=false) {
        if (data.res == "ok") {
            this._edit_form_loader(data);
            this._showModal();
        } else {
                var errStr= this._parse_ajax_error(data);
                dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!','An Error Occured! '+errStr);
                console.error("Unable to execute Operation: ",errStr)
                return false;
            }
    }
    edit(uuid,disable_prefix=false,edit_handle=this._edit_handle) {
          console.info("Loading Data for Edit Mode for '"+uuid+"'");
          var url = this.urls["load_edit"];
          if (disable_prefix == false) {
              console.warn("EP",this.urls["_api_prefix"],url);
              if (this.urls["_api_prefix"] !== "") {
                  url = this.urls["_api_prefix"] + url;
              }
            }
          this._clear_invalid();
          $.ajax({
              url:   url+uuid,
              method: 'GET',
              context: this
          }).done(edit_handle);

    }
    _getOffcanvas() {
            this.offcanvas = new bootstrap.Offcanvas(this.elements["offcanvas"]);

    }
    _showOffcanvas() {
        if (this.offcanvas == false) {
            this._getOffcanvas();
        }
        this.offcanvas.show();
    }

    _hideOffcanvas() {
        this.offcanvas.hide();
    }

    _toggleOffcanvas() {
        this.offcanvas.toggle();
    }

    _render_details_table(data) {
        var table = this.widget_factory.create_table(data.data.uuid);
        var data_keys = Object.keys(data.data);
            for (var i in data_keys) {
                var dk = data_keys[i];
                var tr = this.widget_factory.create_tr(data.data.uuid);
                table.append(tr);
                var lbl = dk;
                if (data.verbose_names[dk] != "") {
                    lbl = data.verbose_names[dk];
                }
                var th = this.widget_factory.create_th(data.data.uuid,dk+"th",lbl+":");
                tr.append(th);
                var txt = "&#160;";
                if (data.data[dk] != null) {
                    txt = data.data[dk];
                }
                var td = this.widget_factory.create_td(data.data.uuid, dk + "td", txt);
                var tr2 = this.widget_factory.create_tr(data.data.uuid);

                table.append(tr2);
                tr2.append(td);
            }
        return table;
    }

    _offcanvas_details(data) {
        if (data.res == "ok") {
            this._getOffcanvas();
            var container = $(this.offcanvas._element).find(this.settings["offcanvas_body"]);
            container.empty();
            var table = this._render_details_table(data);
            container.append(table);
            this._showOffcanvas();
        }
    }

    offcanvas_details(uuid) {
          console.info("Loading Data for Offcanvas Details for '"+uuid+"'");
            var url = this.urls["load_edit"];
            if (this.urls["_api_prefix"] != "") {
            url = this.urls["_api_prefix"] + url;
            }
            $.ajax({
            url:   url+uuid,
            method: 'GET',
            context: this
            }).done(this._offcanvas_details)
    }

     constructor(name="app",settings={},urls={}) {
        if (name != "app") {
            this._appName = name;
        }
        $.extend(this.settings,settings);
        $.extend(this.urls,urls);

        this.widget_factory = new WidgetFactory();
        this.elements = {
            "form":this.settings["form"],
            "modal":this.settings["modal"],
            "offcanvas":this.settings["offcanvas"]
        }

        console.info("Dashboard App ",this._appName," initialised!");
     }
}