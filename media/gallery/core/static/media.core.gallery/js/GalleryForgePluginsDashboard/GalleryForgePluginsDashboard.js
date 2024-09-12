import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class GalleryForgePluginsDashboard extends AbstractDashboardApp {


        constructor(name) {
            super(name);
            this.urls = {
            "_api_prefix":"/dashboard/forge/api/media.gallery.core/settings/",
            "_prefix":"/dashboard/forge/media.gallery.core/settings/",
            "submit":"set/plugin"

            }
            this.elements = {
                "form":"#gallery_form"

            }
        }
 }
