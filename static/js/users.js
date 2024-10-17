import {PageManager} from "./page-manager.js";


PageManager.getInstance().setOnPageLoad("user", function() {
    const block_button = document.getElementById('block-user')
      if (block_button) block_button.addEventListener('click', function() {
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
                body: JSON.stringify({
                    user: data.id,
                    blocked_user: +document.getElementById("user_id").innerHTML
                })
            });
        }).then(response => {
            if (response.ok) {
                alert("Blocked User!");
                PageManager.getInstance().load("user", true)
            } else {
                alert("Failed to block User!");
            }
        });
    })

    const unblock_button = document.getElementById('unblock-user')
    if (unblock_button) unblock_button.addEventListener('click', function() {
        fetch(`/api/user/blocked/${document.getElementById("block_id").innerHTML}`, {
            method: "DELETE"
        }).then(response => {
            if (response.ok) {
                alert("Unblocked User!");
                PageManager.getInstance().load("user", true)
            } else {
                alert("Failed to unblock User!");
            }
        });
    });


    const friend_button = document.getElementById('friend-user')
      if (friend_button) friend_button.addEventListener('click', function() {
        fetch("/api/auth/me/", {
            method: "GET"
        }).then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch user data!");
            }
            return response.json();
        }).then(data => {
            return fetch(`/api/user/friendship/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user: data.id,
                    friend: +document.getElementById("user_id").innerHTML
                })
            });
        }).then(response => {
            if (response.ok) {
                alert("Added user to friend list!");
                PageManager.getInstance().load("user", true)
            } else {
                alert("Failed to add user to friend list!");
            }
        });
    })

    const unfriend_button = document.getElementById('unfriend-user')
    if (unfriend_button) unfriend_button.addEventListener('click', function() {
        fetch(`/api/user/friendship/${document.getElementById("friendship_id").innerHTML}`, {
            method: "DELETE"
        }).then(response => {
            if (response.ok) {
                alert("Added user from friend list!");
                PageManager.getInstance().load("user", true)
            } else {
                alert("Failed to remove user from friend list!");
            }
        });
    });

    const invite_button = document.getElementById('game-invite')
    invite_button.addEventListener('click', function() {
        fetch('api/invite/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user: +document.getElementById("user_id").innerHTML
            })
        }).then(response => {
            if (response.ok) {
                alert("Invitation sent!");
                PageManager.getInstance().load("pong/3dGame", false)
            } else {
                alert("Failed to send invitation!");
            }
        })
    });
});