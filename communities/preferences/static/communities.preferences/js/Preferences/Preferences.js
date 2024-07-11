import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class Preferences extends AbstractDashboardApp {


        constructor(name) {
            super(name);
            this.urls = {
            "submit":"communities.preferences/api/save/settings"

            }
            $.extend(this.settings,{
                "home_on_success": false,
                "success_hdr": "Preferences Updated!",
                "success_body": "Great Success; preferences updated!"
            })


            this.elements = {
                "form":"#system-pref-form",
                "modal":"#pref_savedModal",


            }
        }
 }
