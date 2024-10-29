import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";

PageManager.getInstance().setOnPageLoad("edit-profile", () => {
    const button = document.getElementById("submit-button");

    button.addEventListener("click", async () => {
        // Get the form data
        const avatarInput = document.getElementById("avatar");
        const emailInput = document.getElementById("email");
        const passwordInput = document.getElementById("password");
        const confirmPasswordInput = document.getElementById("confirm-password");

        const formData = new FormData();
        if (avatarInput.files.length !== 0) {
            formData.append("avatar", avatarInput.files[0]);
        }
        if (emailInput.value !== "") {
            formData.append("email", emailInput.value);
        }
        if (passwordInput.value !== "") {
            if (passwordInput.value !== confirmPasswordInput.value) {
                Notification.error("Passwords do not match");
                return;
            }
            formData.append("password", passwordInput.value);
        }

        fetch("/edit-profile", {
            method: "POST",
            body: formData,
        }).then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Failed to edit profile");
            }
        }).then((data) => {
            if (data.success) {
                PageManager.getInstance().load("me");
            } else {
                throw new Error("Failed to edit profile");
            }
        }).catch((error) => {
            Notification.error(error.message);
        });
    })
});