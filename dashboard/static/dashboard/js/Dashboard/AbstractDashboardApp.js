import { WidgetFactory } from "/static/core.plyui/js/WidgetFactory/WidgetFactory.js";
export class AbstractDashboardApp {
    modal = false
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
                dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;Success!','Operation complete!');
                if (home == true) {
                    dashboard.panel_home();
                } else {
                    dashboard.dc_reloadPanel();
                }
                return true;

            } else {
                dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!','An Error Occured! '+data.responseJSON.e.__all__[0]);
                console.error("Unable to execute Operation: ",data.responseJSON.e)
                return false;
            }
    }

    _getModal() {
        this.modal =  new bootstrap.Modal($(this.elements["modal"])[0]);
    }

    _showModal() {
        this.modal.show();
    }
    _hideModal() {
        this.modal.show();
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
            console.log("Submitting Dashboard App Data: URL '"+url+"'");
            $.ajax({
            url:  url,
            data:     form.serialize(),
            complete: handle,
            method: 'POST',
            context: this
            })


    }

     constructor() {
        this.widget_factory = new WidgetFactory();
        this.urls = {
            "submit":"/some/url"
        }
        this.elements = {
            "form":"#some_form",
            "modal":"#some_modal"
        }
     }
}