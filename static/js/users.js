import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";


export function blockUser() {
    const block_button = document.getElementById('block-user')
    if (block_button) block_button.addEventListener('click', function () {
        fetch("/api/auth/me/", {
            method: "GET"
        }).then(response => {
            if (!response.ok) {
                throw new Error("COMMON.ERROR.FETCH.USER_DATA");
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
                Notification.success("USER.ACTIONS.BLOCK.SUCCESS");
                PageManager.getInstance().load("user", true)
            } else {
                Notification.error("USER.ACTIONS.BLOCK.FAILED");
            }
        });
    });
}

export function unblockUser() {
    const unblock_button = document.getElementById('unblock-user')
    if (unblock_button) unblock_button.addEventListener('click', function () {
        fetch(`/api/user/blocked/${document.getElementById("block_id").innerHTML}`, {
            method: "DELETE"
        }).then(response => {
            if (response.ok) {
                Notification.success("USER.ACTIONS.UNBLOCK.SUCCESS");
                PageManager.getInstance().load("user", true)
            } else {
                Notification.error("USER.ACTIONS.UNBLOCK.FAILED");
            }
        });
    });
}

export function friendUser() {
    const friend_button = document.getElementById('friend-user')
    if (friend_button) friend_button.addEventListener('click', function () {
        fetch("/api/auth/me/", {
            method: "GET"
        }).then(response => {
            if (!response.ok) {
                throw new Error("COMMON.ERROR.FETCH.USER_DATA");
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
                Notification.success("USER.ACTIONS.FRIEND.SUCCESS");
                PageManager.getInstance().load("user", true)
            } else {
                Notification.error("USER.ACTIONS.FRIEND.FAILED");
            }
        }).catch(error => {
            Notification.error(error.message);
        })
    })
}

export function unfriendUser(userId, page) {
    fetch(`/api/user/friendship/${userId}`, {
        method: "DELETE"
    }).then(response => {
        if (response.ok) {
            Notification.success("USER.ACTIONS.UNFRIEND.SUCCESS");
            PageManager.getInstance().load(page, true);
        } else {
            Notification.error("USER.ACTIONS.UNFRIEND.FAILED");
        }
    });
}

export function inviteUser() {
    const invite_button = document.getElementById('game-invite')
    invite_button.addEventListener('click', function () {
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
                Notification.success('USER.ACTIONS.INVITE.SUCCESS');
                PageManager.getInstance().load("pong/3dGame", false)
            } else {
                Notification.error("USER.ACTIONS.INVITE.FAILED");
            }
        })
    });
}

PageManager.getInstance().setOnPageLoad("user", function () {
    blockUser();
    unblockUser();
    friendUser();
    const unfriend_button = document.getElementById('unfriend-user')
    if (unfriend_button) unfriend_button.addEventListener('click', function () {
        unfriendUser(document.getElementById("friendship_id").innerHTML, "user", true);
    });
    inviteUser();
});