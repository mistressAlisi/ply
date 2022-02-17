window.create_profile = Object ({
    settings: {
        "modal":"#progressModal",
        "upload_el":"#charImage",
        "upload_url":"/forge/api/upload/profile/picture/",
        "form_id":"#upload_image_form",
    },
    _handle_img: function(data,s) {
        console.log("Uploaded",data,s);
        $(create_profile.settings.modal).modal('hide');
        
    },
    
    img_upload: function(e) {
        $(create_profile.settings.modal).modal('show');
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
        alert("Started");
    }
});
