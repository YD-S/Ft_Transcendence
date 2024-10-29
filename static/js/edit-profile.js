import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";

PageManager.getInstance().setOnPageLoad("edit-profile", () => {
    const button = document.getElementById("submit-button");

    button.addEventListener("click", async () => {
        // Get the form data
        const form = document.getElementById("edit-profile-form");
        const formData = new FormData(form);
        fetch("/edit-profile", {
            method: "POST",
            body: formData
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