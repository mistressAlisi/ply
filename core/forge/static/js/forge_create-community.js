    class CommunityCreator {
        settings = {
            "modal": "#progressModal",
            "upload_el": "#charImage",
            "upload_url": "/forge/api/upload/community/picture/",
            "update_url": "/forge/api/community/cover/update/",
            "preview_url": "/forge/edit/community/cover/preview/",
            "finish_url": "/forge/api/community/cover/finish/",
            "dashboard_url": "/dashboard/forge/",
            "reload_url": "/dashboard/forge/forge/edit/community/cover",
            "form_id": "#upload_image_form",
            "pform_id": "#community_form",
            "dashboard_container_id": "#dashboard_mainPanel",
            "dashboard_mode": false
        }

        apply_settings(new_settings) {
            if (new_settings == undefined) {
                return false;
            }
            this.new_settings = new_settings;
            let setting_keys = Object.keys(this.settings);
            setting_keys.forEach($.proxy(function (e, i) {
                if (this.new_settings[e] !== undefined) {
                    this.settings[e] = this.new_settings[e];
                }
            }, this));
            return true;


        }

        reset_form() {
            if (this.settings["dashboard_mode"] == false) {
                window.history.back();
            } else {
                $(this.settings["dashboard_container_id"]).load(this.settings["reload_url"]);
            }

        }

        _handle_finish(data, s) {
            //$(create_community.settings.modal).modal('toggle');
            switch (data.res) {
                case "ok":
                    if (this.settings["dashboard_mode"] == false) {
                        location.href = this.settings["dashboard_url"];
                    } else {
                        dashboard.successToast("<h6><i class=\"fa-solid fa-check\"></i>&#160;Community Updated!</h6>","Community Details updated.");
                        dc_panel_home()
                    }

                    break;
                case "err":
                    alert("Error: \n" + data.e);
                    break;
                case "except":
                    alert("Error: \n" + data.e);
                    break;
            }
            ;
        }

        _handle_form(data, s) {
            //$(create_community.settings.modal).modal('toggle');
            switch (data.res) {
                case "ok":
                    if (this.settings["dashboard_mode"] == false) {
                        location.href = this.settings["preview_url"];
                    } else {
                        $(this.settings["dashboard_container_id"]).load(this.settings["preview_url"]);
                    }
                    break;
                case "err":
                    alert("Error: \n" + data.e);
                    break;
                case "except":
                    alert("Error: \n" + data.e);
                    break;
            }
            ;
        }

        _handle_img(data, s) {
            //$(create_community.settings.modal).modal('toggle');
            switch (data.res) {
                case "ok":
                    $(this.settings.upload_el).attr('src', data.path);
                    this.pic_set = false;
                    break;
                case "err":
                    alert("Error: \n" + data.e);
                    break;
                case "except":
                    alert("Error: \n" + data.e);
                    break;
            }
            ;
        }

        img_upload(e) {
            //$(create_community.settings.modal).modal('show');
            var filename = $(this.settings["upload_el"]).val();
            var csrftoken = get_cookie('csrftoken');
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });

            $.ajax({
                type: "POST",
                url: this.settings["upload_url"],
                data: new FormData($(this.settings["form_id"])[0]),
                cache: false,
                contentType: false,
                processData: false,
                context: this,
                success: this._handle_img
            });
            return false;

        }

        start(ev) {
            // $(create_community.settings.modal).modal('toggle');
            //create_community.img_upload();
            $.ajax({
                type: "POST",
                url: this.settings["update_url"],
                data: new FormData($(this.settings["pform_id"])[0]),
                cache: false,
                contentType: false,
                processData: false,
                context: this,
                success: this._handle_form
            });
            return false;
        }

        finish(ev) {
            $.ajax({
                type: "GET",
                url: this.settings["finish_url"],
                context: this,
                cache: false,
                processData: false,
                success: this._handle_finish
            })
            return false;
        }

        constructor(new_settings) {
            this.apply_settings(new_settings);
            console.log("Community creator", this.settings["modal"]);
        }

    }

create_community = new CommunityCreator({'dashboard_mode':true});
