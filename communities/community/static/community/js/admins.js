class Admin {

    add() {
        this.modal.show();
        $(this.elements["admin_select"]).selectize();

    }
    _handleTask(data,stat) {

        if (data.responseJSON.res == "ok") {
            dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;Success!','Admin Operation Complete');
            this.modal.hide();
            $(this.elements["dashboard"]).load(this.urls["table_url"]);


        } else {
            dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!',data.responseJSON.e.__all__[0]);
            console.error("Unable to add Event: ",data.responseJSON.e)
        }
    }
    _del() {
        $.ajax({
            url: this.urls["delete_url"]+"/"+this.dtarget,
            complete: this._handleTask,
            method: 'GET',
            context: this
            })
    }
    del(uuid) {
        this.dtarget = uuid;
        this.dmodal.show();

    }
    create() {

        var uuid = $(this.elements["admin_select"])[0].value;
        if (uuid == "") {
            dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!','Specify a Profile to continue!');
            return false;
        }
        $.ajax({
            url: this.urls["submit_url"],
            data:     $(this.elements["admin_form"]).serialize(),
            complete: this._handleTask,
            method: 'POST',
            context: this
            })

    }

    constructor() {
        this.elements = {
            "admin_modal":"#newAdmin_modal",
            "dadmin_modal":"#delAdmin_modal",
            "admin_select":"#id_profile",
            "admin_form":"#admin_form",
            "dashboard":"#dashboard_mainPanel"

        }
        this.urls = {
            "submit_url":"api/communities.community/admin/create",
            "table_url":"communities.community/admins",
            "delete_url":"api/communities.community/admin/delete"
        }

        this.modal = new bootstrap.Modal($(this.elements.admin_modal)[0]);
        this.dmodal = new bootstrap.Modal($(this.elements.dadmin_modal)[0]);

    }
}
admin = new Admin();