window.create_community = Object ({
    settings: {
        "modal":"#progressModal",
        "upload_el":"#charImage",
        "upload_url":"/forge/api/upload/community/picture/",
        "update_url":"/forge/api/community/cover/update/",
        "preview_url":"/forge/edit/community/cover/preview/",
        "finish_url":"/forge/api/community/cover/finish/",
        "dashboard_url":"/dashboard/user/",
        "form_id":"#upload_image_form",
        "pform_id":"#profile_form" 
    }, 
    _handle_finish: function(data,s) {
        //$(create_community.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                location.href = create_community.settings.dashboard_url;
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
        //$(create_community.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                location.href = create_community.settings.preview_url;
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
        //$(create_community.settings.modal).modal('toggle');
        switch (data.res) {
            case "ok":
                $(create_community.settings.upload_el).attr('src',data.path);
                create_community.pic_set = false;
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
        //$(create_community.settings.modal).modal('show');
        var filename = $(create_community.settings.upload_el).val();
        var csrftoken = get_cookie('csrftoken');
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
        });
        
        $.ajax({
            type: "POST",
            url: create_community.settings.upload_url,
            data: new FormData($(create_community.settings.form_id)[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: window.create_community._handle_img
        });
        return false;
        
    },
    start: function(ev) {
        // $(create_community.settings.modal).modal('toggle');
        //create_community.img_upload();
         $.ajax({
            type: "POST",
            url: create_community.settings.update_url,
            data: new FormData($(create_community.settings.pform_id)[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: window.create_community._handle_form
        });
        return false;
    },
    finish: function(ev) {
        $.get(create_community.settings.finish_url,create_community._handle_finish);
        return false;
    }
});
