import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class DashboardStudio extends AbstractDashboardApp {


        constructor(name) {
            super(name);
            this.urls = {
                "submit": "/dashboard/forge/api/media.gallery.core/settings/set"

            }
            this.elements = {
                "modal": "#selectDashboardModal",
                "dashboardSelector":"#dashboardSelect"

            }
        }

        load_dashboard(event) {
            event.preventDefault();
            event.stopPropagation();
        }
        showModal() {
                this._getModal();
                this._showModal();
        }
 }
