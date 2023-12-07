class Staff {

    add() {
        this.modal.show();
        $(this.elements["staff_select"]).selectize();

    }
    _handleTask(data,stat) {

        if (data.responseJSON.res == "ok") {
            dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;Success!','Staff Operation Complete');
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

        var uuid = $(this.elements["staff_select"])[0].value;
        if (uuid == "") {
            dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!','Specify a Profile to continue!');
            return false;
        }
        $.ajax({
            url: this.urls["submit_url"],
            data:     $(this.elements["staff_form"]).serialize(),
            complete: this._handleTask,
            method: 'POST',
            context: this
            })

    }

    constructor() {
        this.elements = {
            "staff_modal":"#newStaff_modal",
            "dstaff_modal":"#delStaff_modal",
            "staff_select":"#id_profile",
            "staff_form":"#staff_form",
            "dashboard":"#dashboard_mainPanel"

        }
        this.urls = {
            "submit_url":"api/communities.community/staff/create",
            "table_url":"communities.community/staff",
            "delete_url":"api/communities.community/staff/delete"
        }

        this.modal = new bootstrap.Modal($(this.elements.staff_modal)[0]);
        this.dmodal = new bootstrap.Modal($(this.elements.dstaff_modal)[0]);

    }
}
staff = new Staff();