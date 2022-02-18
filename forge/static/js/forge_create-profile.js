window.create_profile = Object ({
    settings: {
        "modal":"#progressModal",
        "upload_el":"#charImage",
        "upload_url":"/forge/api/upload/profile/picture/",
        "update_url":"/forge/api/profile/update/",
        "preview_url":"/forge/create/profile/preview/",
        "finish_url":"/forge/api/profile/finish/",
        "dashboard_url":"/dashboard/user/",
        "form_id":"#upload_image_form",
        "pform_id":"#profile_form" 
    }, 
    _handle_finish: function(data,s) {
        //$(create_profile.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                location.href = create_profile.settings.dashboard_url;
            break;
            case "err":
                alert("Error: \n"+data.e);
            break;
            case "except":
                alert("Error: \n"+data.e);
            break;
        }; 
    },
    _handle_form: function(data,s) {
        //$(create_profile.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                location.href = create_profile.settings.preview_url;
            break;
            case "err":
                alert("Error: \n"+data.e);
            break;
            case "except":
                alert("Error: \n"+data.e);
            break;
        }; 
    },
    _handle_img: function(data,s) {
        //$(create_profile.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                $(create_profile.settings.upload_el).attr('src',data.path);
                create_profile.pic_set = false;
            break;
            case "err":
                alert("Error: \n"+data.e);
            break;
            case "except":
                alert("Error: \n"+data.e);
            break;
        }; 
    },
    
    img_upload: function(e) {
        //$(create_profile.settings.modal).modal('show');
        var filename = $(create_profile.settings.upload_el).val();
        var csrftoken = get_cookie('csrftoken');
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        });
        
        $.ajax({
            type: "POST",
            url: create_profile.settings.upload_url,
            data: new FormData($(create_profile.settings.form_id)[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: window.create_profile._handle_img
        });
        return false;
        
    },
    start: function(ev) {
//         $(create_profile.settings.modal).modal('toggle');
        create_profile.img_upload();
         $.ajax({
            type: "POST",
            url: create_profile.settings.update_url,
            data: new FormData($(create_profile.settings.pform_id)[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: window.create_profile._handle_form
        });
        return false;
    },
    finish: function(ev) {
        $.get(create_profile.settings.finish_url,create_profile._handle_finish);
        return false;
    }
});
