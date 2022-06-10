window.preferences = Object({
   settings: {
       "url":"preferences/api/save/settings",
       "form":"#system-pref-form",
       "modal":"#pref_savedModal",
   },
   modal: false,
   _success: function(d) {
       if (d.res == "err") {
           alert(d.e);
       } else if (d == "ok") {
           preferences.modal.show();
       };
   },
   goSave: function() {
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
            }
        }
        });
       data = $(this.settings.form).serialize();
       $.post(this.settings.url,data,this._success);
   },
   init: function() {
       this.modal = new bootstrap.Modal($(this.settings.modal)[0]);
   }
});

