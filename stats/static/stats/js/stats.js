window.stats = Object({
    settings: {
        "form_id":"#stats_form",
        "assign_url":"/stats/api/assign/profile",
        "se_modal":"#skill_modal"
    },
    els: {
        form: false,
    },
    assign: function() {
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
            }
        }
        });
        post_data = this.els.form.serialize();
        $.post(this.settings.assign_url,post_data,window.stats._assign_h);
    },
    _assign_h: function(e){
        if (e =="ok") {
            stats.els.sm.hide();
            dc_reloadPanel();
        } else {
            alert(e.e);
        }
    },
    assign_start: function() {
        this.els.sm.show();
    },
    init: function() {
        stats.els.form = $(stats.settings.form_id);
        stats.els.sm = new bootstrap.Modal($(stats.settings.se_modal)[0]);
    }
})


