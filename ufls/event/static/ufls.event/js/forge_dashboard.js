class EventDashboard {

        _qLink() {
            var epk = $(this.elements["community_select"])[0].value;
            if (epk != "") {
                $(this.elements["query_container"]).load(this.urls["community_link"]+epk);
            }
        }
        _query() {
            var epk = $(this.elements["event_select"])[0].value;
            if (epk != "") {
                $(this.elements["query_container"]).load(this.urls["query_event"]+epk);
            }
        }

        _mod() {
            var epk = $(this.elements["event_select"])[0].value;
            // if (epk != "") {
                $(this.elements["query_container"]).load(this.urls["modify_event"]+epk);
            // } else {
            //     console.warn("WARN",epk);
            //}
        }

        _submitHandle(data,stat) {
            //console.log(data)
            if (data.responseJSON.res == "ok") {
                dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;Success!','The Event '+data.responseJSON.pk+' has been created successfully!');
                dc_panel_home();

            } else {
                dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Success!','An Error Occured! '+data.responseJSON.e);
                console.error("Unable to add Event: ",data.responseJSON.e)
            }
        }
        submit() {
            console.log("Submitting Event Data");
            $.ajax({
            url: this.urls["submit_create_event"],
            data:     $(this.elements["event_form"]).serialize(),
            complete: this._submitHandle,

            method: 'POST'
            })
        }
        _submitLinkHandle(data,stat) {
            //console.log(data)
            if (data.responseJSON.res == "ok") {
                dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;Success!','Link Created!');
                dc_panel_home();

            } else {
                dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!',data.responseJSON.e.__all__[0]);
                console.error("Unable to add Event: ",data.responseJSON.e.__all__[0]);
            }
        }
        submitLink() {
            console.log("Submitting Link Data");
            $.ajax({
            url: this.urls["submit_create_link"],
            data:     $(this.elements["link_form"]).serialize(),
            complete: this._submitLinkHandle,

            method: 'POST'
            })
        }
        constructor() {
            this.urls = {
            "submit_create_event":"/dashboard/forge/ufls.event/api/create/",
            "query_event":"/dashboard/forge/ufls.event/api/query/",
            "community_link":"/dashboard/forge/ufls.event/api/link/",
            "submit_create_link":"/dashboard/forge/ufls.event/api/link/create/",
            "modify_event":"/dashboard/forge/ufls.event/api/modify/",

            }
            this.elements = {
                "event_form":"#event_form",
                "event_select":"#event_id",
                "query_container":"#event_query_div",
                "community_select":"#community_id",
                "link_form":"#link_form"

            }
            // console.log("Event Dashboard Loaded.");

        }
 }


events = new EventDashboard();