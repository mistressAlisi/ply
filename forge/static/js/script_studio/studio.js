window.script_studio = Object({
    settings: {
        "form_id":"#script_studio_form",
        "create_id":"#create_script_form",
        "eval_url":"/forge/api/script/eval/",
        "save_url":"/forge/api/script/save/",
        "get_url":"/forge/api/script/get/",
        "eval_btn":"#rnbtn",
        "eval_out":"#run_output",
        "body_el":"#code_body",
        "bsave_el":"#id_body",
        "se_modal":"#save_ScriptModal",
        "cr_modal":"#new_ScriptModal",
        "lsel":"#id_load_script"
    },
    els: {
        form: false,
        cform: false,
        ebtn: false,
        eout: false,
        bsave: false,
        body: false,
        sm: false,
        lsel: false,
        cm: false
    },
    _eval_h: function(e,i){
        script_studio.els.eout.html(e.out);
    },
    eval: function() {
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
            }
        }
        });
        post_data = this.els.form.serialize();
        $.post(this.settings.eval_url,post_data,window.script_studio._eval_h);
    },
    _save_h: function(e){
        if (e =="ok") {
            script_studio.els.eout.html("<strong>Save Complete!</strong>");
            script_studio.els.sm.hide();
        } else {
            alert(e);
        }
    },
    save: function() {
        $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
            }
        }
        });
        post_data = this.els.cform.serialize();
        $.post(this.settings.save_url,post_data,window.script_studio._save_h);
    },
    mksave: function() {
        script_studio.els.bsave[0].value = script_studio.els.body[0].value;

    },
    _create_h: function (e) {
        if (e.res == "ok") {
            script_studio.els.body[0].value = e.data;
            script_studio.els.cm.hide();
            let evt = new InputEvent("input", {bubbles: true});
            script_studio.els.body[0].dispatchEvent(evt);
        } else {
            alert(e);
        }
    },
    create: function() {
        if (script_studio.els.lsel[0].value == -1) {
            script_studio.els.body[0].value = "";
            script_studio.els.cm.hide();
            let evt = new InputEvent("input", {bubbles: true});
            script_studio.els.body[0].dispatchEvent(evt);
        } else {
            $.get(this.settings.get_url+script_studio.els.lsel[0].value,window.script_studio._create_h);
        };
    },
    init: function() {
        script_studio.els.form = $(script_studio.settings.form_id);
        script_studio.els.cform = $(script_studio.settings.create_id);
        script_studio.els.ebtn = $(script_studio.settings.eval_btn);
        script_studio.els.eout = $(script_studio.settings.eval_out);
        script_studio.els.bsave = $(script_studio.settings.bsave_el);
        script_studio.els.body = $(script_studio.settings.body_el);
        script_studio.els.lsel = $(script_studio.settings.lsel);
        script_studio.els.sm = new bootstrap.Modal($(script_studio.settings.se_modal)[0]);
        script_studio.els.cm = new bootstrap.Modal($(script_studio.settings.cr_modal)[0]);
    }
})
script_studio.init();
