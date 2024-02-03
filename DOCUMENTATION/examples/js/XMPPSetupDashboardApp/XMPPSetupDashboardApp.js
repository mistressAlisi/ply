import { AbstractDashboardApp } from "/static/dashboard/js/Dashboard/AbstractDashboardApp.js";
export class XMPPSetupDashboardApp extends AbstractDashboardApp {
    _submitHandle(data,stat) {
        xmpp_setup.modal.hide();
        super._submitHandle(data,stat);

    }
    submit() {
        this._getModal();
        $(this.elements["mh"]).hide();
        $(this.elements["mc"]).show();
        var jid = $(this.elements["uid_f"])[0].value + "@" + $(this.elements["fqdn_f"])[0].value;
        $(this.elements["jid"]).text(jid);
        $(this.elements["psw"]).text($(this.elements["pw_f"])[0].value);
        this.modal.show();

    }
    cancel() {
        this.modal.hide();
    }
    confirm() {
        $(this.elements["mh"]).show();
        $(this.elements["mc"]).hide();
        super.submit();
    }
    constructor(name) {
        super(name);
        this.urls = {
            "submit": "communities.stream/api/configure/xmpp/enroll"
        }
        this.elements = {
            "form": "#xmpp_form",
            "modal": "#XMPP_modal",
            "fqdn_f":"#fqdn",
            "pw_f":"#APW",
            "uid_f":"#UID",
            "jid":"#jid",
            "psw":"#psw",
            "mh":"#modal-progress",
            "mc":"#modal-confirm"
        }

    }
}
