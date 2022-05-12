window.menu_editor = Object({
    settings: {
        "root_div":"#menu_editor",
        "cat_class":"list-group-item item sortable-class",
        "page_class": "list-group-item subitem",
    },
    root_el: false,
    
    create_category: function() {
        icon_cls = $("#id_icon")[0].value;
        ca_ttl =  $("#id_title")[0].value;
        ca_tip = $("#id_tooltip")[0].value;
        new_cat = $('<ul/>').addClass(this.settings["cat_class"]);
        new_icon = $("<i/>").addClass(icon_cls);
        new_cat.append(new_icon);
        new_title = $("<span>").addClass('h6').html("&#160;"+ca_ttl);
        new_cat.append(new_title);
//         new_tip = $("<p>").addClass('text-muted').html("&#160;"+ca_tip);
//         new_cat.append(new_tip);
        this.root_el.append(new_cat);
        new_cat.data('title',ca_ttl);
        new_cat.data('tooltip',ca_tip);
        new_cat.data('icon',icon_cls);
        sortable(new_cat,{acceptFrom: '.sortable-class, .list-group-item, #menu_editor'});
    },
    add_page: function() {
        pg_ttl = $("#id_almanac_page").find(":selected").text();
        pg_id = $("#id_almanac_page")[0].value;
        new_page = $('<li/>').addClass(this.settings["page_class"]);
        this.root_el.append(new_page);
        new_title = $("<span>").html("&#160;"+pg_ttl);
        new_page.append(new_title);
        new_page.data('page',pg_id);
        sortable(this.root_el,'reload');
    },
    
    init: function() {
        this.root_el = $(this.settings["root_div"]);
        sortable(this.root_el,);
    }
})

menu_editor.init();
