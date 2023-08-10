window.stream_create = Object({
   settings: {
       "url":"stream/api/create",
       "form":"#stream-form",
       "modal":"#stream_modal",
   },
   modal: false,
   nuuid: false,
   _success: function(d) {
       if (d.res == "err") {
           alert(d.e);
       } else if (d.res == "ok") {
           stream_create.modal.show();
           stream_create.uuid = d.uuid;
       };
   },

   join_created: function() {
           stream_create.modal.hide();
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

