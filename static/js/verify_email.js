import {PageManager} from "./page-manager.js";


PageManager.getInstance().setOnPageLoad("auth/verify_email", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (!code) {
        alert("No verification code provided!");
        return;
    }

    fetch(`/api/auth/verify-email/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({code: code})
    }).then(response => {
        if (response.ok) {
            alert("Email verificado");
        } else {
            alert("El código de verificación no es válido o ha expirado.");
        }
        PageManager.getInstance().load("auth/login", false);
    })
})