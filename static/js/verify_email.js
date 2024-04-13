import {PageManager} from "./page-manager.js";


PageManager.getInstance().setOnPageLoad("auth/verify_email", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const user = urlParams.get("user");
    if (!code) {
        alert("No verification code provided!");
        return;
    }
    if (!user) {
        alert("No user provided!");
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
            alert("Email verificado");
        } else {
            alert("El código de verificación no es válido o ha expirado.");
        }
        PageManager.getInstance().load("auth/login", false);
    })
})