window.loginAgent = Object({
    settings: {
        loginurl:"api/auth/login/",
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
        aldiv = $(window.loginAgent.settings.alertid);
        aldiv.html(err);
        aldiv.css('display','block');
    },
    start: function(e) {
        console.info("LoginAgent: Starting Login...");
        if (e != undefined) {
            e.preventDefault();
        };
        $(window.loginAgent.settings.alertid).empty();
         $(window.loginAgent.settings.alertid).css('display',' none');
        if ($(window.loginAgent.settings.userfield)[0].value.length < 1) {
            window.loginAgent._showError(window.loginAgent.errors.user);
            console.error("LoginAgent: ",window.loginAgent.errors.user);
        
            
        };
        
        if ($(window.loginAgent.settings.pwfield)[0].value.length < 1) {
            window.loginAgent._showError(window.loginAgent.errors.pw);
            console.error("LoginAgent: ",window.loginAgent.errors.pw);
        
        };
        
        console.log("Login Transaction in progress...");
        $.post(window.loginAgent.settings.loginurl,$(window.loginAgent.settings.loginform).serialize(),window.loginAgent._handleReply);
    }
});

console.log("Window LoginAgent Ready");
