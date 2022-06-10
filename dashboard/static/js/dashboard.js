window.dashboard = Object({
    settings: {
        notifyurl:"api/get/notifications/",
        sidebarurl:"api/get/sidebar/",
        notifyul: "#notificationqueue",
        notifycountul:"#notificationcount",
        systemMenudiv:"#_systemmenu",
        systemMenuOpen:false,
        systemMenuWidth:'250px',
    },
    /** Current main panel: **/
    cmp: false,
    /** Plugin Control: _pLoaded keeps track of loaded plugins by name to prevent reinitialisation. Plugins that need to extend dashboard can register themselves into the plugins object below: **/
    _pLoaded: [],
    plugins: Object (),
    setSelect: function(id,value) {
        options = $("#"+id+" option");
        options.prop('selected',false);
        len = $("#"+id+" option").length;
        i = 0;
        
        while(i<len) {
            if (options[i].value == value) {
                $(options[i]).prop('selected',true);
            }
            i = i+1;
        }
        $("#"+id).selectpicker('refresh');
    },
    goToSettings: function() {
        $.get("/dashboard/settings",function(data){
            $("#dashboard-menu-toggle_mainPanel").html(data);
        });
    },
    gotoDeviceManager: function() {
        $.get("/accounts/devices",function(data){
            $("#dashboard-menu-toggle_mainPanel").html(data);
        });
    },
    handleNotify: function(data) {
        $(dashboard.settings.notifyul).empty();
        $(dashboard.settings.notifycountul).text(data.count);
        for (i in data.data) {
           noti = data.data[i];
           nli = $("<li></li>");
           h6 = $("<h6></h6>").text(noti.title);
           h6.prepend('<i class="fa fa-'+noti.icon+'" aria-hidden="true"></i>');
           h6.addClass('subheader');
           nli.append(h6);
           nli.addClass('not-item');
           nli.addClass(noti.css);
           $(dashboard.settings.notifyul).append(nli);
        }
    },
    getNotifications: function() {
        $.get(dashboard.settings.notifyurl,window.dashboard.handleNotify);
    },
    
    toggleSystemMenu: function() {
        if (dashboard.settings.systemMenuOpen == true) {
            dashboard.closeSystemMenu();
        } else {
            dashboard.openSystemMenu();
        };
        
    },

    openSystemMenu: function() {
        $(dashboard.settings.systemMenudiv).css('width', dashboard.settings.systemMenuWidth);
        dashboard.settings.systemMenuOpen = true;
    },
    closeSystemMenu: function() {
        $(dashboard.settings.systemMenudiv).css('width','0px');
        dashboard.settings.systemMenuOpen = false;
    },
    startSidebar: function() {
        if (dashboard.settings.currentSideBar != false) {
            
            $("#__sidebarModuleArea").load(dashboard.settings.currentSideBar,false,dc_updateLinks);
        };
    },
    /** Callback function for loadPlugin: **/
    _loadPlugin: function(d) {
        if (d == false) { return false; };
        if (d.type != "db-plugin") { 
            console.error("Wrong Datatype for Plugin!!"); 
            alert("Dashboard can't load: "+plugin+". plugin.json has wrong type.");
            return false;
        }
        /** load javascript: **/
        jsl = d.js.length;
        if (jsl > 0) {
          count = 0;
          while (count < jsl) {
              jsp = "/static/plugins/"+d.name+"/js/"+d.js[count];
              console.debug("Loading Plugin JS: "+jsp);
              $.getScript(jsp);
              count++;
        }};
        /** load css: **/
        csl = d.css.length;
        if (csl > 0) {
          count = 0;
          while (count < csl) {
              csp = "/static/plugins/"+d.name+"/css/"+d.css[count];
              console.debug("Loading Plugin CSS: "+csp);
              $('head').append( $('<link rel="stylesheet" type="text/css" />').attr('href', csp));
              count++;
        }};
        dashboard._pLoaded.push(d.name);
                          
        
    },
    /** loadPlugin: Loads a plugin from the assets/plugins/ directory from the dashboard contents. The plugin must include a plugin.json that describes the css and js files to be loaded. **/
    loadPlugin: function(name) {
        if (name == "") { return false; }
        if (dashboard._pLoaded.indexOf(name) > -1) {return true; };
        console.log("Loading Plugin: "+name);
        $.get("/static/plugins/"+name+"/plugin.json",false,window.dashboard._loadPlugin);
    }
});


function dc_updateLinks() {

    $(".sm_slink").click(function(a,e){dc_handleLink(a,true)});
};
function dc_handleMainLink(a){ 

    dc_handleLink(a,false,".mm_");
    
};

function dc_handleLink(a,sublink=false,link_class=".sm_"){
//   console.log("AA",a)
//   window.aaa = a;
  //a.preventDefault();
  $(link_class+"li").removeClass("active");
  $(link_class+"link").removeClass("active");
  $(link_class+"slink").removeClass("active");  
  //$(a.currentTarget.parentNode).addClass("active");
  link =  $(a.currentTarget);
  modid = a.currentTarget.parentNode.id;
  link.addClass('active');
  if (link.data('js')) {
    console.info("Link JS data",link.data('js'));
    if ($(document).data.modules.indexOf(link.data('js')) < 0) {
        console.info("Loading Script:"+link.data('js'));
        $(document).data.modules.push(link.data('js'));
        $.getScript(link.data('js'));
    } 
   
  }

  if (sublink == true) {
    $(document).trigger('moduleUnload');
    $("#sidebarMenu").offcanvas('hide');

  }
  if (link.data('onclick')) {
    console.info("Link OnClick data",link.data('onclick'));
    $(document).trigger(link.data('onclick'));
  }
  if (link.data('trgt')) {
    console.info("Link Target data",link.data('trgt'));
    dashboard.cmp  = link.data('trgt');
    $("#dashboard_mainPanel").load(link.data('trgt'));
  }
  
};

function dc_reloadPanel() {
    $("#dashboard_mainPanel").load(dashboard.cmp);
};

$(document).ready(function(){
  $(document).data.modules = [];
  $(".nav-link").click(function(a,e){dc_handleMainLink(a);});
  $(".sm_link").click(function(a,e){dc_handleLink(a,true);});
  $("#dashboard-menu-toggle").click();
  
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

// window.setInterval(dashboard.getNotifications,10000);





