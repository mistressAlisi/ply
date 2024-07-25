import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class Preferences extends AbstractDashboardApp {


        constructor(name) {
            super(name);
            this.urls = {
            "_api_prefix":"communities.preferences/api/",
            "_prefix":"",
            "submit":"save/settings"

            }
            $.extend(this.settings,{
                "home_on_success": true,
                "success_hdr": "Preferences Updated!",
                "success_body": "Great Success; preferences updated!"
            })


            this.elements = {
                "form":"#system-pref-form",
                "modal":"#pref_savedModal",


            }
        }
 }
