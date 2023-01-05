window.notservices = Object({
    settings: {
        "container":"#_notservices",
    },

    els: {
        container: false,
    },
    /** notification counter: **/
    notcou: 1,
    /** internal functions to automagically close notifications: **/
    _dismiss1: function(id) {
        $(id).removeClass('show');
        window.setTimeout(window.notservices._dismiss2,500,id);
    },
    _dismiss2: function(id) {
        $(id).remove()
    },
    /** Generic builder: **/
    _notBuilder: function(type,icon,msg) {
        notify = $('<div/>',{'id':'not_'+this.notcou});
        window.notservices.els.container.append(notify);
        notify.addClass('alert alert-'+type+' alert-dismissable fade show');
        notify[0].innerHTML = '<i class="'+icon+'"></i>&#160;'+msg+'<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
        return notify;
    },
    success: function(icon,msg,timeout=10) {
        /** Create and inject a notification into the ui **/
        notify = window.notservices._notBuilder('success',icon,msg);
        window.setTimeout(window.notservices._dismiss1,timeout*1000,'#not_'+this.notcou);
        window.notservices.notcou++;
    },
    info: function(icon,msg,timeout=10) {
        /** Create and inject a notification into the ui **/
        notify = window.notservices._notBuilder('info',icon,msg);
        window.setTimeout(window.notservices._dismiss1,timeout*1000,'#not_'+this.notcou);
        window.notservices.notcou++;
    },
    warn: function(icon,msg,timeout=10) {
        /** Create and inject a notification into the ui **/
        notify = window.notservices._notBuilder('warning',icon,msg);
        window.setTimeout(window.notservices._dismiss1,timeout*1000,'#not_'+this.notcou);
        window.notservices.notcou++;
    },
    danger: function(icon,msg,timeout=10) {
        /** Create and inject a notification into the ui **/
        notify = window.notservices._notBuilder('danger',icon,msg);
        window.setTimeout(window.notservices._dismiss1,timeout*1000,'#not_'+this.notcou);
        window.notservices.notcou++;
    },
    primary: function(icon,msg,timeout=10) {
        /** Create and inject a notification into the ui **/
        notify = window.notservices._notBuilder('primary',icon,msg);
        window.setTimeout(window.notservices._dismiss1,timeout*1000,'#not_'+this.notcou);
        window.notservices.notcou++;
    },
    init: function() {
        //stats.els.form = $(stats.settings.form_id);
        window.notservices.els.container = $(window.notservices.settings.container);

        console.log("Started");
    }
});

notservices.init();


