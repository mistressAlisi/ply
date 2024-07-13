export class Dashboard {
    load_from_url() {
        var load = decodeURIComponent(location.hash).substr(1);
        var links = $(this.settings.sidebarElement).find("a"+this.settings.sidebarLinkClass);
        links.each(function(x,y,z=load) {
            if (z != "") {
                if ($(y).data('trgt') == z) {
                    $(y).trigger('click');
            }}
        });
    }
    constructor() {
        this.cmp =  false;
        this._pLoaded =  [];
        this.plugins = Object();
        this.settings = {
            notifyurl: "api/get/notifications/",
            sidebarurl: "api/get/sidebar/",
            notifyul: "#notificationqueue",
            notifycountul: "#notificationcount",
            systemMenudiv: "#_systemmenu",
            systemMenuOpen: false,
            systemMenuWidth: '250px',
            sidebar_rightdiv: "#_dashboard_offcanvas_right",
            toastSuccessCls: 'bg-outline-success text-success',
            toastErrorCls: 'bg-outline-warning text-warning',
            toastCls: 'bg-outline-white',
            sidebarElement: '#sidebarMenu',
            sidebarLinkClass :'.sidebar-submenu-link'

        }
        console.log("Dashboard Instance ready.");
    }

    setSelect(id,value) {
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
    }

    goToSettings() {
        $.get("/dashboard/settings",function(data){
            $("#dashboard-menu-toggle_mainPanel").html(data);
        });
    }
    gotoDeviceManager() {
        $.get("/accounts/devices",function(data){
            $("#dashboard-menu-toggle_mainPanel").html(data);
        });
    }

     // Toast API:
    successToast(header,body) {
        new bs5.Toast({
		body: body,
		header: header,
		className: this.settings.toastSuccessCls,

	}).show();
    }
    errorToast(header,body) {
        new bs5.Toast({
		body: body,
		header: header,
		className: this.settings.toastErrorCls,

	}).show();
    }

    normalToast(header,body) {
        new bs5.Toast({
		body: body,
		header: header,
		className: this.settings.toastCls,

	}).show();
    }
    handleNotify(data) {
        $(this.settings.notifyul).empty();
        $(this.settings.notifycountul).text(data.count);
        for (i in data.data) {
           noti = data.data[i];
           nli = $("<li></li>");
           h6 = $("<h6></h6>").text(noti.title);
           h6.prepend('<i class="fa fa-'+noti.icon+'" aria-hidden="true"></i>');
           h6.addClass('subheader');
           nli.append(h6);
           nli.addClass('not-item');
           nli.addClass(noti.css);
           $(this.settings.notifyul).append(nli);
        }
    }
    getNotifications() {
        $.get(this.settings.notifyurl,this.handleNotify);
    }

    toggleSystemMenu() {
        if (this.settings.systemMenuOpen == true) {
            this.closeSystemMenu();
        } else {
            this.openSystemMenu();
        };

    }

    openSystemMenu() {
        $(this.settings.systemMenudiv).css('width', this.settings.systemMenuWidth);
        this.settings.systemMenuOpen = true;
    }
    closeSystemMenu() {
        $(this.settings.systemMenudiv).css('width','0px');
        this.settings.systemMenuOpen = false;
    }
    startSidebar() {
        if (this.settings.currentSideBar != false) {

            $("#__sidebarModuleArea").load(this.settings.currentSideBar,false,dc_updateLinks);
        };
    }

    open_sidebarRight() {
        const bso = new bootstrap.Offcanvas(this.settings.sidebar_rightdiv);
        bso.show();
    }

    close_sidebarRight() {
        const bso = new bootstrap.Offcanvas(this.settings.sidebar_rightdiv);
        bso.hide();
    }
    /** Callback function for loadPlugin: **/
    _loadPlugin(d) {
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
              this.loadJS(jsp,'module');
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
        this._pLoaded.push(d.name);


    }
    /** loadPlugin: Loads a plugin from the assets/plugins/ directory from the dashboard contents. The plugin must include a plugin.json that describes the css and js files to be loaded. **/
    loadPlugin(name) {
        if (name == "") { return false; }
        if (this._pLoaded.indexOf(name) > -1) {return true; };
        console.log("Loading Plugin: "+name);
        $.get("/static/plugins/"+name+"/plugin.json",false,this._loadPlugin);
    }

    dc_updateLinks() {
        $(".sm_slink").click(function(a,e){this.handleLink(a,true)});
    }

    loadJS(src,type) {
          var script=document.createElement('script');
          script.type=type;
          script.src=src;
          $("body").append(script);

    }
    handleLink(a,sublink=false,link_class=".sm_") {
        //   console.log("AA",a)
        //   window.aaa = a;
        //a.preventDefault();
        $(link_class + "li").removeClass("active");
        $(link_class + "link").removeClass("active");
        $(link_class + "slink").removeClass("active");
        //$(a.currentTarget.parentNode).addClass("active");
        if ('currentTarget' in a) {
            var link = $(a.currentTarget);
            var modid = a.currentTarget.parentNode.id;
        } else {
            var link = $(a.target);
            var modid = "";
        }
        link.addClass('active');
        if (link.data('js')) {
            console.info("Link JS data", link.data('js'));
            if ($(document).data.modules.indexOf(link.data('js')) < 0) {
                console.info("Loading Script:" + link.data('js'));
                $(document).data.modules.push(link.data('js'));
                this.loadJS(link.data('js'),'module');
            }
        }
        if (sublink == true) {
            $(document).trigger('moduleUnload');
            try {
                $("#sidebarMenu").offcanvas('hide');
            } catch (error) {
                console.info("Trying to close #sidebarMenu's offcanvas: Not found.");
            }
        }
        if (link.data('onclick')) {
            console.info("Link OnClick data",link.data('onclick'));
            $(document).trigger(link.data('onclick'));
        }
        if (link.data('trgt')) {
            console.info("Link Target data",link.data('trgt'));
            this.cmp  = link.data('trgt');
            $("#dashboard_mainPanel").load(link.data('trgt'));
        }
    }

    handleMainLink(a) {
        this.handleLink(a,false,".mm_")
    }

    dc_reloadPanel() {
        $("#dashboard_mainPanel").load(this.cmp);
    }
    panel_home() {
        $("#dashboard_mainPanel").load("dashboard_panel_home");
    }
}