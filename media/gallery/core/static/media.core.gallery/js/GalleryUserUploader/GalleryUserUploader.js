import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class GalleryUserUploader extends AbstractDashboardApp {
        _parent_walker(parent,target_node) {
       if (target_node == undefined) { target_node = "DIV"};
       while (parent.nodeName != target_node) {
            parent = parent.parentElement;
        };
        return $(parent);

        }
        on_plugin_select(e) {
            var target = this._parent_walker($(e.target)[0],"BUTTON");
            $(this.elements.all_buttons).addClass(this.settings.button_active_class);
            target.addClass(this.settings.button_active_class);
            target.removeClass(this.settings.button_inactive_class);
            $(this.elements.desc_div)[0].innerHTML = target.data('desc');
            $(this.elements.create_start_btn)[0].disabled = null;
            this.content_plugin = target.data("plugin");
        }

        load_upload_form(e) {
            e.preventDefault();
            $(this.elements.form).load(this.urls.form_upload_url+this.content_plugin)
        }
        constructor(name) {
            super(name);
            this.content_plugin = false;

            this.settings = {
                "button_active_class":"btn-primary",
                "button_inactive_class":"btn-secondary"

            }
            this.urls = {
            "submit":"media.gallery.core/api/settings/set/plugin",
            "form_upload_url":"media.gallery.core/api/upload/get_form/"


            }
            this.elements = {
                "form":"#upload_submission_form",
                "all_buttons":".core-content-button",
                "desc_div":"#content_submission_type_desc",
                "create_start_btn":"#create_start_btn"

            }
            console.info("Gallery User Uploader Ready.")
        }
 }
