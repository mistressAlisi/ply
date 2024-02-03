class Login {
    constructor() {
        this.settings = {
            "modal":"#ssoModal"
        }
        this.modal = $(this.settings["modal"])
    }

    showsso() {
        this.modal.modal('show');
    }
}
login = new Login();
