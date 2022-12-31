window.friends = Object({
    settings: {
        "form_id":"#friend_form",
        "rm_url":"/dashboard/user/community/api/friend/remove/",
        "rf_modal":"#rfriend_modal"
    },
    uuid: false,
    els: {
        form: false,
    },
    go_remove: function() {
//         $.ajaxSetup({
//         beforeSend: function(xhr, settings) {
//         if (!this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
//             }
//         }
//         });
//         post_data = this.els.form.serialize();
        $.get(this.settings.rm_url+this.uuid,window.friends._grm_h);
    },
    _grm_h: function(e){
        if (e.res =="ok") {
            friends.els.sm.hide();
            dc_reloadPanel();
        } else {
            alert(e.e);
        }
    },
    remove: function(uuid) {
        this.uuid = uuid;
        this.els.sm.show();
    },
    init: function() {
        //stats.els.form = $(stats.settings.form_id);
        window.friends.els.sm = new bootstrap.Modal($(friends.settings.rf_modal)[0]);
    }
})

