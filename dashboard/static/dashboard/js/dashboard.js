import { Dashboard } from "./Dashboard/Dashboard.js";
window.dashboard= new Dashboard();
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
$(document).ready(function(){
  $(document).data.modules = [];
  $(".nav-link").click(function(a,e){window.dashboard.handleMainLink(a);});
  $(".sm_link").click(function(a,e){window.dashboard.handleLink(a,true);});
  $("#dashboard-menu-toggle").click();
  
});

