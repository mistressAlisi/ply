import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
import { SmartSelect } from "/static/core.plyui/js/SmartSelect/SmartSelect.js";
export class GalleryUserDashboard extends AbstractDashboardApp {

    keywords_selectize = false
    collections_selectize = false
    current_card = false
    _renderCategories(res) {
        for (var colid in res.cols) {
            var col_label = res.cols[colid];
            this.collections_selectize.addOption(colid,col_label);
        }
    }

    _update_card_form(event) {

        var new_title = $(this.elements["form"]).find("#review-title")[0].value;
        var new_descr = $(this.elements["form"]).find("#review-descr")[0].value;
        var new_cat =   $(this.elements["form"]).find("#review-publish_category option:selected").text();
        this.current_card.find("#card-title").text(new_title);
        this.current_card.find("#card-body").text(new_descr);
        this.current_card.find("#card-category").text(new_cat);
        var file = this.current_card.data('fileid');
        var data = $(this.elements["form"]).serialize();
        $.ajax({
            url:  this.urls.update+file,
            data:  data,
            method:'POST',
        });
    }
    _initCardElements() {
        this.keywords_selectize = new SmartSelect(this.elements.keywords_selector,
            {
                input_class: 'form-select',
                create: true,
                maxItems: null,
                valueField: 'h',
                searchField: 'n',
                labelField:'n',
                options: [],
                query_url: '/keywords/api/get/',
                f_option_load: function(query,callback) {
                    if (!query.length) return callback();
                        $.ajax({
                            url: window.gallery_dashboard.urls.keywords_get_url + encodeURIComponent(query),
                            type: 'GET',
                            error: function() {
                            callback();
                            },
                        success: function(res) {
                            callback(res);
                            }});
                },

                f_option_render: function(item, escape) {
                    return '<div>' +
                    '<span class="title">' +
                    '<span class="name"><strong>'+ escape(item.n) +'</strong><em> ('+escape(item.h)+')</em></span>' +
                    '</span>' +
					'</div>';
                    },

            });
        this.collections_selectize = new SmartSelect(this.elements.collection_selector,
            { });
        $.get(this.urls.collections_get_url,this._renderCategories.bind(this));
        $(this.elements["form"]).on("change",this._update_card_form.bind(this));
    }
    _cardClickHandle(event) {
      event.preventDefault();
      event.stopPropagation();
      var card = this._parent_walker(event.target);
      var fileid = card.data('fileid');
      this.current_card = card;
      $(this.elements.offcanvas_editor).offcanvas('show');
      $(this.elements.offcanvas_editor).load(this.urls.lighttable_review_panel+fileid,this._initCardElements.bind(this));
      card.removeClass('animate__fadeIn');
      card.addClass('animate__pulse');
    }

    _renderCard(id,filedata) {
        this.widget_factory.hideEl(filedata["card"]);
        filedata["card"].empty()
        filedata["card"].append(this.widget_factory.create_img("thumb_"+id,filedata["file"].thumbnail,"Thumbnail for "+filedata["file"].file,'card-img-top card-header-img'));
        filedata["card"].append(this.widget_factory.create_block("h5","card-title",filedata['file'].file.split(".")[0]));
        filedata["card"].append(this.widget_factory.create_block("h6","card-date","<i class=\"fa-solid fa-calendar-xmark\"></i> "+filedata['file'].created));
        filedata["card"].append(this.widget_factory.create_block("p","card-category",""));
        filedata["card"].append(this.widget_factory.create_block("p","card-body",filedata['file'].descr));
        this.widget_factory.fadeInEl(filedata["card"]);
    }
     _loadHandle(data) {
         if (data.res != "ok") {
             dashboard.errorToast("Lighttable Load Error!",e.res.data);
             return false;
         }
         for (var fi in data.files) {
             if (this.cIndex.indexOf(fi) == -1) {
                 this.cIndex.push(fi);
                 var file = data.files[fi];
                 var filedata = [];
                 var card = this.widget_factory.create_generic_card("file_",fi,false,'Loading....','<p class="text-center">'+file.file+'</p>','card lighttable-card');
                 $(this.elements.lighttable_cnt).append(card);
                 card.data('fileid',fi);
                 card.data('file',file.file);
                 card.data('size',file.file_size);
                 card.data('plugin',file.plugin);
                 card.data('type',file.type);
                 filedata["card"] = card
                 filedata["file"] = file
                 this.contents[fi] = filedata;
                 if (file.thumbnail != false) {
                     this._renderCard(fi,filedata);
                 }
                 card.on('click',this._cardClickHandle.bind(this));

             } else {
                 // Update card here.
             }
         }
     }
      _publish_selected_item_handle(data) {
        $(this.elements["offcanvas_editor"]).offcanvas('hide');
      }

      confirm_publish_selected(e) {
        var bsm = new bootstrap.Modal($(this.elements["confirm_publish"]));
        bsm.show();
      }

      publish_selected_item(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this.settings.confirm_pub_modal).modal('hide');
        console.info("Saving Data...",e);
        var data = $(this.elements["form"]).serialize();
        if (data != false) {
            var file = this.current_card.data('fileid');
            $.ajax({
            url:  this.urls.publish+file,
            data:     data,
            complete: this._publish_selected_item_handle,
            method: 'POST',
            context: this
            });
        }

      }
      load_lighttable() {
         $.get(this.urls["lighttable_contents"],false,this._loadHandle.bind(this),'json');
      }

        constructor(name) {
            super(name);
            this.cIndex = []
            this.contents = [];
            this.collections_selectize = false;
            this.keywords_selectize = false;
            this.urls = {
            "submit":"media.gallery.core/api/settings/set/plugin",
            "update":"media.gallery.core/api/upload/update/",
            "publish":"media.gallery.core/api/upload/publish/",
            "lighttable_contents":"media.gallery.core/api/get/lighttable/",
            "lighttable_review_panel":"media.gallery.core/api/upload/review_panel/",
            "keywords_get_url":"/keywords/api/get/",
            "collections_get_url":"media.gallery.core/api/upload/get_collections/w+"

            }


            this.elements = {
                "form":"#gallery_review_form",
                "review_file_el":"#review_file_id",
                "lighttable_cnt":"#lighttable_items_container",
                "offcanvas_editor":"#uploaderOffCanvas",
                "keywords_selector":"#review-publish_keywords",
                "collection_selector":"#review-publish_collections",
                "confirm_publish":"#confirmModal"

            }

            console.info("Gallery User Dashboard Ready.")

        }
 }
