import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class GalleryForgeDashboard extends AbstractDashboardApp {


        constructor(name) {
            super(name);
            this.urls = {
            "_api_prefix":"/dashboard/forge/api/media.gallery.core/",
            "_prefix":"/dashboard/forge/media.gallery.core/",
            "submit":"settings/set"

            }
            this.elements = {
                "form":"#gallery_form"

            }
        }
 }
