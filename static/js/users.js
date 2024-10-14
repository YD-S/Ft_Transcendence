import {PageManager} from "./page-manager.js";


PageManager.getInstance().setOnPageLoad("user", function() {
    document.getElementById('block-user').addEventListener('click', function() {
        fetch("/api/auth/me/", {
            method: "GET"
        }).then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch user data!");
            }
            return response.json();
        }).then(data => {
            return fetch(`/api/user/blocked/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({user: data.id, blocked_user: +document.getElementById("user_id").innerHTML})
            });
        }).then(response => {
            if (response.ok) {
                alert("Blocked User!");
                PageManager.getInstance().load("user", true)
            } else {
                alert("Failed to block User!");
            }
        });
    })});