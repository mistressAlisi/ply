import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
import { WidgetFactory } from "/static/core.plyui/js/WidgetFactory/WidgetFactory.js";
export class GalleryUserUploader extends AbstractDashboardApp {


        _uploadFile() {

        }
        _first_stage_scan(i,file) {
           console.log('... Found File:'+ file.name);
           //
           var card = this.widget_factory.create_generic_card("file_",i,'<i class="fa-regular fa-file"></i>','',file.name,this.settings.lighttable_item_class);
           $(this.elements.upload_items_cntr).append(card);
           this.uploads.push(file);
        }

        _progressHandle(e) {
           if (e.lengthComputable) {
               //calculate the percentage loaded

               //log percentage loaded
                   var pct = (e.loaded / e.total) * 100;
                   this.widget_factory.set_progressbar(this.upload_pbar,pct);


           }
        }

        _progressUpHandle(e) {
           if (e.lengthComputable) {
               //calculate the percentage loaded

               //log percentage loaded
                   var pct = Math.round((e.loaded / e.total) * 100);
                   this.widget_factory.set_progressbar(this.upload_pbar,pct);



           }
        }
        _uploadDoneHandle(e) {
           if (e.responseJSON == "ok") {
            dashboard.successToast(" Files uploaded!", "Files have been uploaded and are being processed!");
            gallery_dashboard.load_lighttable();
            this.reset();
           } else {
               var errStr= this._parse_ajax_error(e.responseJSON);
               dashboard.errorToast("File Upload Error!",errStr);
           }

        }
        upload_handle(ev) {
           console.log("Uploading files...");
           ev.preventDefault();
           this.upload_pbar = this.widget_factory.create_progressbar("upload",100,0,"success",false);
           $(this.elements.upload_pbar_area).append(this.upload_pbar);
           $(this.elements.upload_pbar_bttns).addClass('animate__animated animate__fadeOut');
           var formData = new FormData();
           var index="";
           for (var fi in this.uploads) {
               index += "file_" + fi+","
               formData.append("original_"+fi,this.uploads[fi].name);
               formData.append("size_"+fi,this.uploads[fi].size);
               formData.append("file_" + fi, this.uploads[fi]);
           }


           var uploadInst = $.ajax({
                   type: 'POST',
                   data: formData,
                   processData: false,
                   contentType: false,
                   uploadProgress: this._progressUpHandle.bind(this),
                   progress: this._progressHandle.bind(this),
                   complete: this._uploadDoneHandle.bind(this),
                   url: this.urls["file_upload"],
                    xhrFields: {
                    withCredentials: true
                   }

           });
           console.log("Started Upload.");



        }

        _stop_event_handler(ev) {
            ev.preventDefault();
            ev.stopPropagation();
        }

        drop_handler(ev) {
            console.log("Starting Drop Processing...",ev.dataTransfer.items);
            ev.preventDefault();
            if(this.uploads.length ==0) {
                $(this.elements.upload_items_cntr_splsh).addClass('animate__animated animate__fadeOut');
            }
            if (ev.dataTransfer.items) {
                for (var i = 0;  i < ev.dataTransfer.items.length; i++) {
                    // We only want files:
                    if (ev.dataTransfer.items[i].kind === 'file') {
                        var file = ev.dataTransfer.items[i].getAsFile();
                        this._first_stage_scan(i,file);
                    } else {
                        console.warn("Rejecting Data transfer of kind: "+ev.dataTransfer.items[i].kind+" full Item below:")
                        console.warn(ev.dataTransfer.items[i]);
                    }
                }

            }
            if (this.uploads.length >= 2) {
                dashboard.successToast(this.uploads.length+" Files queued!", "Files are ready to be uploaded.");
           } else {
               dashboard.successToast(" File queued!", "File is ready to be uploaded.");
           }
        }
        drag_handler(e) {

        }



        reset() {
           $(this.elements.upload_pbar_bttns).removeClass('animate__fadeOut');
           $(this.elements.upload_pbar_bttns).addClass('animate__fadeIn');
           $(this.elements.upload_items_cntr_splsh).removeClass('animate__fadeOut');
           $(this.elements.upload_items_cntr_splsh).addClass('animate__fadeIn');
           $(this.elements.upload_items_cntr).empty();
           $(this.elements.upload_pbar_area).empty();
           this.upload_pbar = false;
           this.uploads = [];
           $(this.elements.upload_modal).modal('hide');





        }
        constructor(name) {
            super(name);
            this.widget_factory = new WidgetFactory();
            this.uploads = [];

            this.settings = {
                "button_active_class":"btn-primary",
                "button_inactive_class":"btn-secondary",
                "lighttable_item_class":"card ltable_upload_card animate__animated  animate__fadeInRight ",

            }
            this.urls = {
            "_api_prefix":"",
            "_prefix":"",
            "file_upload":"media.gallery.core/api/upload/file_ingest",
            "submit":"media.gallery.core/api/settings/set/plugin",
            "form_upload_url":"media.gallery.core/api/upload/get_form/"


            }
            this.elements = {
                "form":"#upload_submission_form",
                "all_buttons":".core-content-button",
                "desc_div":"#content_submission_type_desc",
                "create_start_btn":"#create_start_btn",
                "lighttable_items_cntr":"#lighttable_items_container",
                "upload_items_cntr":"#upload_files_zone",
                "upload_items_cntr_splsh":"#drop_zone_splash",
                "upload_pbar_area":"#upprogressbar_area",
                "upload_pbar_bttns":"#upctl_btns",
                "upload_modal":"#uploadModal"

            }
            console.info("Gallery User Uploader Ready.")
        }
 }
