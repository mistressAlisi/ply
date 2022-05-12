window.loginAgent = Object({
    settings: {
        loginurl:"/api/auth/login/",
        loginform:"#plyloginform",
        userfield:"#plyuserid",
        pwfield:"#plypass",
        rmfield:"#plyremember",
        alertid:"#plyloginalert",
        alerticon:"fa-solid fa-triangle-exclamation"
        
    },
    
    errors: {
        "user":"Invalid User ID specified.",
        "pw":"Invalid Password specified",
        "auth":"Authentication Failure"
    },
    
    _handleReply: function(data,status) {
        console.log("Data handle",data,status);
        if (data.res.login == "ok" ) {
            window.location.reload(true);
        }
    },
    _showError: function(err) {
        aldiv = $(this.settings.alertid);
        aldiv.html(err);
        aldiv.css('display','block');
    },
    start: function(e) {
        console.info("LoginAgent: Starting Login...");
        if (e != undefined) {
            e.preventDefault();
        };
        $(this.settings.alertid).empty();
         $(this.settings.alertid).css('display',' none');
        if ($(this.settings.userfield)[0].value.length < 1) {
            this._showError(this.errors.user);
            console.error("LoginAgent: ",this.errors.user);
        
            
        };
        
        if ($(this.settings.pwfield)[0].value.length < 1) {
            this._showError(this.errors.pw);
            console.error("LoginAgent: ",this.errors.pw);
        
        };
        
        console.log("Login Transaction in progress...");
        
        $.post(this.settings.loginurl,$(this.settings.loginform).serialize(),this._handleReply);
    }
});
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
        }
    }
});
console.log("Window LoginAgent Ready");
