import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";

PageManager.getInstance().setOnPageLoad("auth/register", () => {
    document.getElementById("submit").addEventListener("click", (event) => {
        event.preventDefault();
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;
        if (password !== confirmPassword) {
            Notification.warning("USER.REGISTER.PASSWORD_MISMATCH");
            return;
        }
        fetch("/api/auth/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({username, email, password})
        }).then(response => {
            if (response.ok) {
                Notification.success("USER.REGISTER.SUCCESS");
                PageManager.getInstance().load('auth/login');
                return response.json();
            } else {
                Notification.error("USER.REGISTER.FAILED");
                return response.json();
            }
        }).then(data => {
            if (data.message) {
                Notification.success(data.message);
            }
            else if (data.errors) {
                for (const message of data.errors) {
                    Notification.error(message);
                }
            }
        });
    });
});