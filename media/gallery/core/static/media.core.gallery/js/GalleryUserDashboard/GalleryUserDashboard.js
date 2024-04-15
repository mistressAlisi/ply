import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class GalleryUserDashboard extends AbstractDashboardApp {
        constructor(name) {
            super(name);

            this.urls = {
            "submit":"/dashboard/User/api/media.gallery.core/settings/set/plugin"

            }
            this.elements = {
                "form":"#upload_submission_form"

            }

            console.info("Gallery User Dashboard Ready.")
        }
 }
