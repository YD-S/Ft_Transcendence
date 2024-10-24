import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";


PageManager.getInstance().setOnPageLoad("auth/verify_email", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const user = urlParams.get("user");
    if (!code) {
        Notification.error("AUTH.ERROR.NO_2FA_CODE");
        return;
    }
    if (!user) {
        Notification.error("AUTH.ERROR.NO_2FA_USER");
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
            Notification.success("AUTH.TFA.EMAIL_VERIFIED");
        } else {
            Notification.error("AUTH.ERROR.INVALID_2FA_CODE");
        }
        PageManager.getInstance().load("auth/login", false);
    })
})