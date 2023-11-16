window.registrar = Object ({
    settings: {
        "modal":"#progressModal",
        "cart_container":"#cart_container",
        "submit_url":"/app/registrar/api/create",
        "submit_loot_url":"/app/registrar/api/create/loot",
        "rem_url":"/app/registrar/api/remCart",
        "rem_loot_url":"/app/registrar/api/remLoot",
        "checkout_url":"/forge/api/community/cover/update/",
        "cartdata_url":"/app/registrar/api/cartContentsHTML",
        "finish_url":"/forge/api/community/cover/finish/",
        "dashboard_url":"/dashboard/user/",
        "form_id":"#attendee_form",
        "pform_id":"#profile_form",
        "cart_count_id":"#current_count",
        "session_total":"#session_total",
        "total_upd_itms":".update_totals",
        "loot_total_div":"#totalDue",
        "loot_stotal_div":"#loot_stotal_div",
        "loot_form_id":"#loot_form"
    },
    current_total: 0,
    rem: function(itm) {
        if (confirm("Remove this Attendant?")) {
            $.ajax({
                'url':registrar.settings.rem_url+"/"+itm,
            }).done(function(res){
                $(registrar.settings.cart_container).load(registrar.settings.cartdata_url);
            });
        };
    },

    rem_loot: function(itm) {
        if (confirm("Remove this Loot?")) {
            $.ajax({
                'url':registrar.settings.rem_loot_url+"/"+itm,
            }).done(function(res){
                $(registrar.settings.cart_container).load(registrar.settings.cartdata_url);
            });
        };
    },
    updateLootTotal: function() {
        console.log("total loot update!");
        registrar.current_total = $(registrar.settings.session_total)[0].value*1;
        registrar.current_stotal = 0;
        $(registrar.settings.total_upd_itms).each(function(k,e){
           var ue = (e.value * $(e).data('cost'));
           registrar.current_stotal =  registrar.current_stotal + ue;
           registrar.current_total =  registrar.current_total + ue;
           console.log(k,ue);
        });
        $(registrar.settings.loot_stotal_div).html("$"+registrar.current_stotal.toFixed(2));
        $(registrar.settings.loot_total_div).html("$"+registrar.current_total.toFixed(2));
    },
    _handle_form: function(data,s) {
        //$(registrar.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                $(registrar.settings.form_id)[0].reset();
                $(registrar.settings.cart_container).load(registrar.settings.cartdata_url);
                $(registrar.settings.cart_count_id).html(($(registrar.settings.cart_count_id).html()*1)+1);
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

    _prep_checkout: function(data) {
        switch (data.res) {
            case "ok":
                location.href = "/app/registrar/checkout"
            break;
            case "err":
                alert("Error: \n"+data.e);
            break;
            case "except":
                alert("Error: \n"+data.e);
            break;
        };
    },

    start2: function(ev) {
        // $(registrar.settings.modal).modal('toggle');
         $.ajax({
            type: "POST",
            url: registrar.settings.submit_loot_url,
            data: new FormData($(registrar.settings.loot_form_id)[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: window.registrar._prep_checkout
        });
        return false;
    },
});
