window.fof = Object({
    settings: {
        "modal":"#fof_modal",
        "ufol_modal":"#fof_unfollow_modal",
        "ufri_modal":"#fof_unfriend_modal",
        "fol_url":"/dashboard/user/community/api/follow/",
        "ufol_url":"/dashboard/user/community/api/unfollow/",
        "ufri_url":"/dashboard/user/community/api/unfriend/",
        "fri_url":"/dashboard/user/community/api/friend/",
        "fol_btn":"#fof_modal_follow",
        "fri_btn":"#fof_modal_friend",
        "ufol_btn":"#fof_modal_unfollow",
        "ufri_btn":"#fof_modal_unfriend",
        "fol_str":'<i class="fa-solid fa-magnifying-glass-plus"></i>&#160;Follow ',
        "fri_str":'<i class="fa-solid fa-user-plus"></i>&#160;Friend ',
        "fri_not":"Friend Request Sent to ",
        "fri_noti":"fa-solid fa-user-plus",
        "fol_not":"Now Following ",
        "fol_noti":"fa-solid fa-magnifying-glass-plus",
        "ufol_noti":"fa-solid fa-magnifying-glass-minus",
        "ufol_not":"Unfollowed ",
        "ufri_noti":"fa-solid fa-user-minus",
        "ufri_not":"Unfriended ",
        "error_i":"fa-solid fa-triangle-exclamation",
        "ufl_str":'<i class="fa-solid fa-magnifying-glass-minus"></i>&#160;Unfollow ',
        "ufr_str":'<i class="fa-solid fa-user-minus"></i>&#160;Unfriend ',
    },
    uuid: false,
    name: false,
    els: {
        sm: false,
        ufolm: false,
        ufrim: false,
        fob: false,
        frb: false,
        uflb: false,
        ufib: false,
    },

    _gfollow: function() {
        $.get(this.settings.fol_url+this.uuid,window.fof._gfollow_h);
    },
    _gfollow_h: function(e){
        if (e.res =="ok") {
            fof.els.sm.hide();
            window.notservices.success(window.fof.settings.fol_noti,window.fof.settings.fol_not+" "+decodeURI(window.fof.name)+"!",10);
        } else {
            window.notservices.danger(window.fof.settings.error_i,e.e,10);
            console.error(e.e);
        }
    },

    _gufol: function() {
        $.get(this.settings.ufol_url+this.uuid,window.fof._gufol_h);
    },
    _gufol_h: function(e){
        if (e.res =="ok") {
            fof.els.ufolm.hide();
            window.notservices.success(window.fof.settings.ufol_noti,window.fof.settings.ufol_not+" "+decodeURI(window.fof.name)+".",10);
        } else {
            window.notservices.danger(window.fof.settings.error_i,e.e,10);
            console.error(e.e);
        }
    },

    unfollow: function(uuid,name) {
        this.uuid = uuid;
        this.name = name;
        this.els.ufolm.show();
        window.fof.els.uflb.innerHTML = window.fof.settings.ufl_str+" "+decodeURI(name);
    },

    toggle: function(uuid,name) {
        this.uuid = uuid;
        this.name = name;
        this.els.sm.show();
        window.fof.els.fob.innerHTML = window.fof.settings.fol_str+" "+decodeURI(name);
        window.fof.els.frb.innerHTML = window.fof.settings.fri_str+" "+decodeURI(name);
    },

    _gufri_h: function(e){
        if (e.res =="ok") {
            fof.els.sm.hide();
            window.notservices.success(window.fof.settings.fri_noti,window.fof.settings.fri_not+" "+decodeURI(window.fof.name)+".",10);
        } else {
            window.notservices.danger(window.fof.settings.error_i,e.e,10);
            console.error(e.e);
        }
    },

    _gfriend: function() {
        $.get(this.settings.fri_url+this.uuid,window.fof._gufri_h);
    },

    friend: function(uuid,name) {
        this.uuid = uuid;
        this.name = name;
        window.fof._gfriend();
    },

    _gunfriend: function() {
        $.get(this.settings.ufri_url+this.uuid,window.fof._gufri_h);
    },
    _gufri_h: function(e){
        if (e.res =="ok") {
            fof.els.ufrim.hide();
            window.notservices.success(window.fof.settings.ufri_noti,window.fof.settings.ufri_not+" "+decodeURI(window.fof.name)+".",10);
        } else {
            window.notservices.danger(window.fof.settings.error_i,e.e,10);
            console.error(e.e);
        }
    },

    unfriend: function(uuid,name) {
        this.uuid = uuid;
        this.name = name;
        this.els.ufrim.show();
        window.fof.els.ufib.innerHTML = window.fof.settings.ufr_str+" "+decodeURI(name);
    },
    init: function() {
        //stats.els.form = $(stats.settings.form_id);
        window.fof.els.sm = new bootstrap.Modal($(fof.settings.modal)[0]);
        window.fof.els.ufolm = new bootstrap.Modal($(fof.settings.ufol_modal)[0]);
        window.fof.els.ufrim = new bootstrap.Modal($(fof.settings.ufri_modal)[0]);
        window.fof.els.fob = $(window.fof.settings.fol_btn)[0];
        window.fof.els.frb = $(window.fof.settings.fri_btn)[0];
        window.fof.els.uflb = $(window.fof.settings.ufol_btn)[0];
        window.fof.els.ufib = $(window.fof.settings.ufri_btn)[0];
    }
});
fof.init();



