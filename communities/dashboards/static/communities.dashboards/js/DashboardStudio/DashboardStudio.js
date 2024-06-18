import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
import {DynapageWidgetEditor} from "/static/core.dynapages/js/DynapageWidgetEditor/DynapageWidgetEditor.js";
export class DashboardStudio extends DynapageWidgetEditor {

        widgets = {}

        constructor(name,settings) {
            super(name,settings);
            this.page_uuid = false
            this.urls = {
                "submit": "/dashboard/forge/api/media.gallery.core/settings/set",
                "load_url":"/dashboard/forge/api/communities.dashboards/studio/load/",
                "load_widgets_url":"/dashboard/forge/api/communities.dashboards/studio/widgets/load/"

            }
            this.elements = {
                "modal": "#selectDashboardModal",
                "dashboardSelector":"#dashboardSelect",
                "container":"#dashboard_studio_container",
                "offcanvas":"#studio_offCanvas",
                "widget_container":"#widget_cards_bar"

            }
        }
        _load_widget_bar_h(data) {
            if (data.res == "ok") {
                this.widgets = JSON.parse(data.widgets);
                $(this.elements["widget_container"]).empty();
                for (var w in this.widgets) {
                    var widget = this.widgets[w];
                    var card = this._createWidgetCard(widget.pk,widget.fields);
                    $(this.elements["widget_container"]).append(card);
                    card.draggable = true;

                }

            }

        }
        load_widget_bar() {
            $.ajax({
                url: this.urls["load_widgets_url"] + this.page_uuid,
                context: this,
                success: this._load_widget_bar_h,
                dataType: "json"
            });

        }

        load_dashboard(event) {
            event.preventDefault();
            event.stopPropagation();
            this.page_uuid = $(this.elements["dashboardSelector"])[0].value;
            if (this.page_uuid != "") {
                this._hideModal();
                $(this.elements["container"]).load(this.urls["load_url"]+this.page_uuid,false,$.proxy(this.start_edit,this));
                this.load_widget_bar();
            } else {
                dashboard.normalToast("Select a Dashboard","Can't edit a blank dashboard!");
            }

        }
        showModal() {
                this._getModal();
                this._showModal();
        }
 }
