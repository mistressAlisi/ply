window.registrar = Object ({
    settings: {
        "modal":"#progressModal",
        "cart_container":"#cart_container",
        "submit_url":"/app/registrar/api/create",
        "rem_url":"/app/registrar/api/remCart",
        "checkout_url":"/forge/api/community/cover/update/",
        "cartdata_url":"/app/registrar/api/cartContentsHTML",
        "finish_url":"/forge/api/community/cover/finish/",
        "dashboard_url":"/dashboard/user/",
        "form_id":"#attendee_form",
        "pform_id":"#profile_form"
    },

    rem: function(itm) {
        if (confirm("Remove this Attendant?")) {
            $.ajax({
                'url':registrar.settings.rem_url+"/"+itm,
            }).done(function(res){
                $(registrar.settings.cart_container).load(registrar.settings.cartdata_url);
            });
        };
    },

    _handle_form: function(data,s) {
        //$(registrar.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                $(registrar.settings.form_id)[0].reset();
                $(registrar.settings.cart_container).load(registrar.settings.cartdata_url);
                window.scrollTo(0,0);
            break;
            case "err":
                alert("Error: \n"+data.e);
            break;
            case "except":
                alert("Error: \n"+data.e);
            break;
        };
    },


    start1: function(ev) {
        // $(registrar.settings.modal).modal('toggle');
         $.ajax({
            type: "POST",
            url: registrar.settings.submit_url,
            data: new FormData($(registrar.settings.form_id)[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: window.registrar._handle_form
        });
        return false;
    },
});
