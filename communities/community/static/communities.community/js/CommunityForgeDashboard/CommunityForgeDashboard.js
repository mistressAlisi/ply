import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class CommunityForgeDashboard extends AbstractDashboardApp {
        menu_del_target = false;
        showMenuModal() {
            $(this.elements["menu_modal"]).modal('show');
        }
        hideMenuModal() {
            $(this.elements["menu_modal"]).modal('hide');
        }

        _submitMenuHandle(data,stat,home=true) {
            //console.log(data)
            if (data.res == "ok") {
                dashboard.successToast('<h6><i class="fa-solid fa-check"></i>&#160;Success!','Operation complete!');
                    this.hideMenuModal();
                    dashboard.dc_reloadPanel();

                return true;

            } else {
                dashboard.errorToast('<h6><i class="fa-solid fa-xmark"></i>&#160;Error!','An Error Occured! '+data.e.__all__);
                console.error("Unable to execute Operation: ",data.e.__all__)
                return false;
            }
    }
        submitMenu(event) {
            event.stopPropagation();
            event.preventDefault();
            this.submit(this.urls["submit_menu"],$(this.elements["menu_form"]),this._submitMenuHandle.bind(this));

        }

        edit_menu(uuid) {
            $(this.elements["menu_modal"]).load(this.urls["load_menu_item"]+uuid);
            this.showMenuModal();
        }
        delete_menu(uuid) {
             this.menu_del_target = uuid;
             $(this.elements["confirm_medel_modal"]).modal('show');
        }

        _del_menu() {
            $.ajax({
            url:  this.urls["delete_menu_item"]+this.menu_del_target,
            complete: this._submitMenuHandle,
            method: 'GET',
            context: this
            })
           this.menu_del_target = false;
           $(this.elements["confirm_medel_modal"]).modal('hide');

        }
        constructor(name) {
            super(name);

            this.urls = {
            "_api_prefix":"",
            "_prefix":"",
            "submit_menu":"/dashboard/forge/api/communities.community/menu/create",
            "load_menu_item":"/dashboard/forge/api/communities.community/menu/edit/",
            "delete_menu_item":"/dashboard/forge/api/communities.community/menu/delete/",

            }
            this.elements = {
                "menu_form":"#menu_form",
                "menu_modal":"#newMenu_modal",
                "confirm_medel_modal":"#delMenu_modal"
            }
        }
 }
