import {PageManager} from "./page-manager.js";

PageManager.getInstance().setOnPageLoad("auth/register", () => {
    document.getElementById("submit").addEventListener("click", (event) => {
        event.preventDefault();
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
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
                alert("Registration successful!");
                PageManager.getInstance().load('auth/login');
            } else {
                alert("Registration failed!");
            }
        });
    });
});