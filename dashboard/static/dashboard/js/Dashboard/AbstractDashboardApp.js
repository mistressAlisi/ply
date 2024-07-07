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
            "submit":"/some/url",
            "load_edit":"/some/url/"
    }
    modal = false
    offcanvas = false
    widget_factory =  false
    urls = []
    elements = []
    _parent_walker(parent,target_node) {
       if (target_node == undefined) { target_node = "DIV"};
       while (parent.nodeName != target_node) {
            parent = parent.parentElement;
        };
        return $(parent);

    }

    _submitHandle(data,stat,home=true) {
            //console.log(data)
            if (data.responseJSON.res == "ok") {
                dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;'+this.settings["success_hdr"],this.settings["success_body"]);
                if ((home == true) && (this.settings["home_on_success"] == true)) {
                    dashboard.panel_home();
                } else {
                    dashboard.dc_reloadPanel();
                }
                return true;

            } else {
                var errStr="";
                var objks = Object.keys(data.responseJSON.e);
                for (var okin in objks) {
                    var ok = objks[okin];
                    errStr = errStr +" <em>"+ok+"</em>: "+data.responseJSON.e[ok]+"<br/>";
                }
                dashboard.errorToast('<h5 class="text-danger"><i class="fa-solid fa-xmark"></i>&#160;Error!','<strong>An Error Occurred:</strong><br/>'+errStr);
                console.error("Unable to execute Operation: ",errStr)
                return false;
            }
    }

    _getModal() {
        this.modal =  new bootstrap.Modal(this.elements["modal"]);
    }

    _showModal() {
        this._getModal();
        this.modal.show();
    }
    _hideModal() {
        this._getModal();
        this.modal.hide();
    }

    add() {
        this._showModal();
    }
    submit(url=false,form=false,handle=false) {
            if (url == false) {
                url = this.urls["submit"];
            }
            if (form == false) {
                form = $(this.elements["form"]);
            }
            if (handle == false) {
                handle = this._submitHandle;
            }
            console.info("Submitting Dashboard App Data: URL '"+url+"'");
            $.ajax({
            url:  url,
            data:     form.serialize(),
            complete: handle,
            method: 'POST',
            context: this
            })


    }
    _edit_handle(data) {
        if (data.res == "ok") {
            var data_keys = Object.keys(data.data);
            for (var i in data_keys) {
                var dk = data_keys[i];
                var update_el = $(this.elements["form"]).find("#id_"+dk);
                if (update_el.length > 0) {
                    update_el[0].value = data.data[dk];
                }
            }
            this._showModal();
        } else {
                dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!','An Error Occured! '+data.e.__all__[0]);
                console.error("Unable to execute Operation: ",data.e)
                return false;
            }
    }
    edit(uuid) {
          console.info("Loading Data for Edit Mode for '"+uuid+"'");
            $.ajax({
            url:   this.urls["load_edit"]+uuid,
            success: this._edit_handle,
            method: 'GET',
            context: this
            })
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

    _offcanvas_details(data) {
        if (data.res == "ok") {
            this._getOffcanvas();
            var container = $(this.offcanvas._element).find(this.settings["offcanvas_body"]);
            container.empty();
            var table = this.widget_factory.create_table(data.data.uuid);
            container.append(table);
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

            this._showOffcanvas();
        }
    }

    offcanvas_details(uuid) {
          console.info("Loading Data for Offcanvas Details for '"+uuid+"'");
            $.ajax({
            url:   this.urls["load_edit"]+uuid,
            success: this._offcanvas_details,
            method: 'GET',
            context: this
            })
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