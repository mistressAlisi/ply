window.publisher = Object({
    settings: {
        maxLen: 500,
        lwarn1: 10,
        lwarn1_class: "bg-danger",
        lwarn2: 50,
        lwarn2_class: "bg-warning",
        len_dclass: "bg-dark",
        postEl: "#streamPostBox",
        inputEl: "#contents_text",
        countEl: "#st-countdown",
        emoBtn: "#emoji-btn",
        form: "#stream_Form"
    },
    count: 0,
    els: {
        box: false,
        ofc: false,
        inputEl: false,
        countEl: false,
        emoBtn: false,
        form: false
    },
    onsubmit: function(e) {
        post_data = this.els.form.serialize();
        this.els.inputEl[0].value = "";
        return false;
    },
    emoji: false,
    _countChars: function() {
        window.publisher.count = window.publisher.settings.maxLen - window.publisher.els.inputEl[0].value.length;
          if ((window.publisher.count) < 0) {
              window.publisher.count = 0;
          };
          window.publisher.els.countEl.removeClass(window.publisher.settings.lwarn1_class);
          window.publisher.els.countEl.removeClass(window.publisher.settings.lwarn2_class);
          window.publisher.els.countEl.removeClass(window.publisher.settings.len_dclass);
          if (window.publisher.count <= window.publisher.settings.lwarn1) {
                window.publisher.els.countEl.addClass(window.publisher.settings.lwarn1_class);
          } else if (window.publisher.count <= window.publisher.settings.lwarn2) {
                window.publisher.els.countEl.addClass(window.publisher.settings.lwarn2_class);
          } else {
                window.publisher.els.countEl.addClass(window.publisher.settings.len_dclass);
          }
          window.publisher.els.countEl.text(window.publisher.count);
    },
    _emCallback: function(e,c) {
        window.publisher.els.inputEl[0].value = window.publisher.els.inputEl[0].value+" "+e.emoji;
        window.publisher._countChars();
    },
    init: function() {
        this.els.box = $(this.settings.postEl);
        this.els.ofc = new bootstrap.Offcanvas(this.els.box);
        this.els.inputEl = $(this.settings.inputEl);
        this.els.inputEl.attr('maxlength',this.settings.maxLen);
        this.els.inputEl.keyup(window.publisher._countChars);
        this.els.countEl = $(this.settings.countEl);
        this.els.emoBtn = $(this.settings.emoBtn);
        this.els.form = $(this.settings.form);
        this.emoji = new EmojiKeyboard;
        this.emoji.instantiate(this.els.inputEl);
        
        this.emoji.callback = this._emCallback;
        this.els.emoBtn.click(this.emoji.toggle_window);
        this._countChars();
        this.els.ofc.show();
        
    }
})


$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            
            xhr.setRequestHeader("X-CSRFToken",Cookies.get('csrftoken'));
        }
    }
});

$(document).ready(function(){
    publisher.init();
});
