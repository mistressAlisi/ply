window.gallery_core.plugins["gallery_photos"] = Object({
    metadata: false,
    _set_res: function() {
        width =   window.gallery_core.plugins["gallery_photos"].metadata.metadata.width;
        height =   window.gallery_core.plugins["gallery_photos"].metadata.metadata.height;
        $("#review-resolution").empty();
        scale = 1.0;
        while (scale >= 0.1) {
            swi = Math.round(width * scale);
            she = Math.round(height * scale);
            $("#review-resolution").append(new Option("["+swi+" x "+she+"]", scale));
            scale = scale - 0.1;
        };
        
    },
    _selectize: function(e,o) {
        e.removeClass('form-select');
        e.selectize(o);
    },
    _serialise: function(e) {
        if ($(e)[0].selectize != undefined) {
            return $(e)[0].selectize.items.join(",");
        } else {
            return false;
        }
    },

    _updateCard: function(e) {
        //console.log("Update Card",e,gallery_core.editor);
        title = $("#review-title")[0].value;
        $(".rounded-pill.fade").removeClass('show');
        if (title == "") {
          title = $("#form-"+gallery_core.editor.file+" #title")[0].value;  
        };
        $("#card-"+gallery_core.editor.file).children('section').children('section').children('h5')[0].innerHTML = title;
        $("#form-"+gallery_core.editor.file+" #title")[0].value = title;
        descr = $("#review-descr")[0].value;
        if (descr != "") { 
            $("#card-"+gallery_core.editor.file).children('section').children('section')[1].children[0].innerHTML =  descr;
            $("#form-"+gallery_core.editor.file+" #descr")[0].value = descr;
            $("#descr_alert").removeClass('show');
        } else {
            $("#descr_alert").addClass('show');
        };
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-resolution");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #res")[0].value = res;
        };
        $("#form-"+gallery_core.editor.file+" #display")[0].value = $("#review-display_details")[0].value;
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-nsfw");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #nsfw")[0].value = res;
        } else {
               $("#nsfw_alert").addClass('show');
        }
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-raiting");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #raiting")[0].value = res;
        } else {
            $("#rating_alert").addClass('show');
        }
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-display_details");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #det")[0].value = res;
        };
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-display_style");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #style")[0].value = res;
        };
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-display_sizing");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #sizing")[0].value = res;
        };

        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-display_details");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #det")[0].value = res;
        };        
        res =  $("#review-publish_category")[0].value;
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #cat")[0].value = res;
        };
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-publish_keywords");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #kw")[0].value = res;
        } else {
            $("#kw_alert").addClass('show');
        }
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-publish_collections");
        if (res == "") {
            $("#collection_alert").addClass('show');
        } else {
            $("#form-"+gallery_core.editor.file+" #col")[0].value = res;
        };
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-publish_notify");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #not")[0].value = res;
        }; 
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-publish_keywords");
        if (res != "") {
            $("#form-"+gallery_core.editor.file+" #kw")[0].value = res;
        }; 
        
    
    },
    prepare_publish: function(e) {
        /** Validate certain entries before we publish! **/
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-publish_collections");
        if (res == "") {
            
            return false;
        };
        
        if ($("#review-descr")[0].value == "") {
            return false;
        };
        res =  window.gallery_core.plugins["gallery_photos"]._serialise("#review-raiting");
        if (res == "") {
            
            return false;
        };
        /** only true allows publishing: **/
        return true;
    },
    prepare_review: function() {
        /** Setup Widgets: **/
        window.gallery_core.plugins["gallery_photos"].metadata = JSON.parse($("#form-"+gallery_core.editor.file+" #meta")[0].value);
        window.gallery_core.plugins["gallery_photos"]._set_res();
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-resolution"));
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-raiting"));
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-nsfw"));
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-resolution"));
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-display"));
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-display_details"),{'maxItems':null});
        /** Load Categories and setup widget asynchronously: **/
        $.get("gallery/api/upload/get_categories",function(cats,e){    
            
            for (c in cats) {
                for (j in cats[c]) {  
                    if (j == "__label") {
                        label = cats[c]["__label"];
                } else {
                        $("#review-publish_category").append(new Option(label+"/"+cats[c][j], j,false,false));
                    }
                }
            };
//             window.gallery_core.plugins["gallery_photos"]._selectize($("#review-publish_category"),{'maxItems':null});
//             if ($("#form-"+gallery_core.editor.file+" #cat")[0].value != "") {
//                 $("#review-publish_category")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #cat")[0].value.split(","));
//             };
        });
        /** Load Collections and setup widget asynchronously: **/
         $.get("gallery/api/upload/get_collections/w+",function(cols,e){    
            
             for (c in cols['cols']) {
               
                $("#review-publish_collections").append(new Option(cols['cols'][c],c,false,false));
            }
            
            window.gallery_core.plugins["gallery_photos"]._selectize($("#review-publish_collections"),{'maxItems':null,'create':true});
            if ($("#form-"+gallery_core.editor.file+" #col")[0].value != "") {
                $("#review-publish_collections")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #col")[0].value.split(","));
            };
        });
        /** Dynamic Widget for Keywords: **/
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-publish_keywords"),{
            'create':true,
            'maxItems':null,
            'valueField':'h',
            'labelField':'n',
            'searchField':'n',
            'options':[],
            render: {
                option: function(item, escape) {
                    return '<div>' +
                    '<span class="title">' +
                    '<span class="name"><strong>'+ escape(item.n) +'</strong><em> ('+escape(item.h)+')</em></span>' +
                    '</span>'+
					'<p class="meta">' +
                    '<span class="items"><i class="fas fa-sitemap"></i> Items: ' + escape(item.i) + ' </span>' +
					'<span class="spankes"><i class="fas fa-heart"></i> Likes:' + escape(item.l) + ' </span>' +
					'<span class="watchers"><i class="fas fa-share-alt"></i> Shares:' + escape(item.s) + ' </span>' +
					'<span class="forks"><i class="far fa-comments"></i> Comments:' + escape(item.c) + ' </span>' +
					'</p>' +
					'</div>';
                    }
            },
            score: function(search) {
						var score = this.getScoreFunction(search);
						return function(item) {
							return score(item) * (1 + Math.min(item.i / 100, 1));
						};
					},
            load: function(query, callback) {
                    if (!query.length) return callback();
					$.ajax({
						url: '/keywords/api/get/' + encodeURIComponent(query),
						type: 'GET',
						error: function() {
						callback();
					},
						success: function(res) {
						callback(res);
					}
					});
            },
            onLoad: function(data) {
            if ($("#form-"+gallery_core.editor.file+" #kw")[0].value != "") {
                $("#review-publish_keywords")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #kw")[0].value.split(","));
            };
            }
            
            
        });
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-publish_notify"),{"allowEmptyOption":true,'maxItems':null});
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-display_style"));
        window.gallery_core.plugins["gallery_photos"]._selectize($("#review-display_sizing"));
        /** Setup Data: **/
        $("#review-title")[0].value = $("#form-"+gallery_core.editor.file+" #title")[0].value;
        $("#review-descr")[0].value = $("#form-"+gallery_core.editor.file+" #descr")[0].value;
        
        if ($("#form-"+gallery_core.editor.file+" #res")[0].value != "") {
            $("#review-resolution")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #res")[0].value);
        };
        
        if ($("#form-"+gallery_core.editor.file+" #display")[0].value != "") {
            $("#review-display_details")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #display")[0].value);
        };
        
        if ($("#form-"+gallery_core.editor.file+" #nsfw")[0].value != "") {
            $("#review-nsfw")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #nsfw")[0].value);
        }; 
        
        if ($("#form-"+gallery_core.editor.file+" #raiting")[0].value != " ") {
            $("#review-raiting")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #raiting")[0].value);
        } else {
            // FIXME: HAAACK!!
            $("#review-raiting")[0].selectize.setValue('e');
        };
         
        if ($("#form-"+gallery_core.editor.file+" #det")[0].value != "") {
            $("#review-display_details")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #det")[0].value.split(","));
        };
        
        if ($("#form-"+gallery_core.editor.file+" #style")[0].value != "") {
            $("#review-display_style")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #style")[0].value);
        };
        
        if ($("#form-"+gallery_core.editor.file+" #sizing")[0].value != "") {
            $("#review-display_sizing")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #sizing")[0].value);
        };
        
      
        if ($("#form-"+gallery_core.editor.file+" #not")[0].value != "") {
            $("#review-publish_notify")[0].selectize.setValue($("#form-"+gallery_core.editor.file+" #not")[0].value.split(","));
        };
        /** Setup Events: **/
        $("#review-title").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard);
        $("#review-descr").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard);
        $("#review-display_details").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard); 
        $("#review-nsfw").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard);
        $("#review-raiting").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard); 
        $("#review-display_style").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard);
        $("#reviewopoen-display_details").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard); 
        $("#review-display_sizing").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard);
        $("#review-publish_category").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard);
        $("#review-publish_keywords").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard); 
        $("#review-publish_notify").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard); 
        $("#review-publish_collections").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard); 
        $("#review-publish_keywords").on('change',window.gallery_core.plugins["gallery_photos"]._updateCard); 
        
        return true;
    },
    
     /** Viewer functions: **/
     /** Handle the click function:**/
     _on_click: function(ev,data) {
        if (window.gallery_core.canvas_element.css('background-size') == 'contain') {
            size = window.gallery_core.canvas_element.data('meta').meta.width+"px, "+window.gallery_core.canvas_element.data('meta').meta.height+"px";
            window.gallery_core.canvas_element.css('background-size',size);
            bpos = ((gallery_core.nav.pageX*-(gallery_core.canvas_element.data('meta').meta.width) / window.innerWidth)/2)+"px "+(gallery_core.nav.pageY*-((gallery_core.canvas_element.data('meta').meta.height-(window.innerHeight/2)) / window.innerHeight)/2)+"px";
            console.log("BPos",bpos);
            window.gallery_core.canvas_element.css('background-position',bpos);
        } else {
            window.gallery_core.canvas_element.css('background-position','center center');
            window.gallery_core.canvas_element.css('background-size','contain');
        };
     },
     /** Setup the cards after the gallery plugin pulls them from the server for full view: **/
    setup_card_view: function(card_div,data) {
        /** For set up, we just need to specify the actual file people will view in full view for now: **/
        /** Select the largest item in the heap that isn't a thumbnail, and return it. ***/
        fn = false;
        for (f in data.files) {
            if (data.files[f].thumbnail == false) {
                if (fn == false) {
                    fn = data.files[f];
                } else if (data.files[f].size > fn.size) {
                    fn = data.files[f].size;
                }
            };
        };
        return fn;
    },
    
    /** Render a view for the Gallery Canvas: **/
    render_view: function(data) {
         window.gallery_core.canvas_element.css('background-image',"url('"+data.path+"')");
         window.gallery_core.canvas_element.data('meta',data);
         window.gallery_core.canvas_element.data("id",data.id);
        $(window.gallery_core).off("canvas-click");
//         $(window.gallery_core).on("canvas-click",window.gallery_core.plugins["gallery_photos"]._on_click);

        return true;
    }
});
console.log("Gallery Photos Plugin ready.");
$(gallery_core).trigger('plugin_ready','gallery_photos');

