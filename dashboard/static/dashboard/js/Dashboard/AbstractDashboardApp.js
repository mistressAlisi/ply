export class AbstractDashboardApp {
    _submitHandle(data,stat) {
            //console.log(data)
            if (data.responseJSON.res == "ok") {
                dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;Success!','Operation complete!');
                dashboard.panel_home();

            } else {
                dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Success!','An Error Occured! '+data.responseJSON.e);
                console.error("Unable to add Event: ",data.responseJSON.e)
            }
    }

    submit() {
            console.log("Submitting Dashboard App Data");
            $.ajax({
            url: this.urls["submit"],
            data:     $(this.elements["form"]).serialize(),
            complete: this._submitHandle,
            method: 'POST'
            })
    }

     constructor() {
        this.urls = {
            "submit":"/some/url"
        }
        this.elements = {
            "form":"#some_form"
        }
     }
}