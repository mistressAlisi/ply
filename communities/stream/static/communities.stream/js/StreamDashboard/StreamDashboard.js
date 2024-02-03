import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class StreamDashboard extends AbstractDashboardApp {


    constructor(name) {
        super(name);
        this.urls = {
            "submit":"api/communities.stream/config/xmpp/submit"
        }
        this.elements = {
            "form":"#xmpp_form"
        }
    }

}
