import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class GalleryForgeDashboard extends AbstractDashboardApp {


        constructor(name) {
            super(name);
            this.urls = {
            "submit":"/dashboard/forge/api/media.gallery.core/settings/set"

            }
            this.elements = {
                "form":"#gallery_form"

            }
        }
 }
