import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";


PageManager.getInstance().setOnPageLoad("auth/verify_email", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const user = urlParams.get("user");
    if (!code) {
        Notification.error("No verification code provided!");
        return;
    }
    if (!user) {
        Notification.error("No user provided!");
        return;
    }

    fetch(`/api/auth/verify-email/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({code: code, user: user})
    }).then(response => {
        if (response.ok) {
            Notification.success("Email verificado");
        } else {
            Notification.error("El código de verificación no es válido o ha expirado.");
        }
        PageManager.getInstance().load("auth/login", false);
    })
})