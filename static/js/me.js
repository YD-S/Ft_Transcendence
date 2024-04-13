import {PageManager} from "./page-manager.js";


PageManager.getInstance().setOnPageLoad("me", () => {
    document.getElementById("toggle-2fa").addEventListener("click", (event) => {
        event.preventDefault();
        fetch("/api/auth/me/", {
            method: "GET"
        }).then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch user data!");
            }
            return response.json();
        }).then(data => {
            return fetch(`/api/user/${data.id}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({has_2fa: !data.has_2fa})
            });
        }).then(response => {
            if (response.ok) {
                alert("2FA status updated!");
                PageManager.getInstance().load("me")
            } else {
                alert("Failed to update 2FA status!");
            }
        });
    })

    const resend_verification = document.getElementById("resend-verification")
    resend_verification ? resend_verification.addEventListener("click", (event) => {
        fetch("/api/auth/send-verification/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({user_id: document.getElementById("user_id").innerHTML})
        }).then(response => {
            if (response.ok) {
                alert("Verification email sent!");
            } else {
                alert("Failed to send verification email!");
            }
        })
    }) : null;
})