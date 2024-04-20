import {PageManager} from "./page-manager.js";
import {saveToken} from "./utils.js";


export function login() {
    let username = document.getElementById('username').value.trim();
    let password = document.getElementById('password').value;
    let data = {
        username: username.trim(),
        password: password
    };
    fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => {
            if (response.status >= 400) {
                throw new Error("Invalid username or password");
            }
            return response.json();
        })
        .then(data => {
            if (data.action === '2fa') {
                PageManager.getInstance().load(`auth/2fa`, false, {args: [data.email2fa, data.user_id]})
            } else if (data.action === 'login') {
                saveToken(data);
                PageManager.getInstance().load('home');
            }
        })
        .catch((error) => {
            alert(error);
        });
}

function oauth() {
    fetch('/api/auth/oauth/')
        .then(response => {
            if (response.status >= 400) {
                throw new Error("There was an error with the OAuth request. Please try again.");
            }
            return response.json();
        })
        .then(data => {
            sessionStorage.setItem('oauth_state', data.state);
            window.location.href = data.url;
        })
        .catch((error) => {
            alert(error);
        });
}

PageManager.getInstance().setOnPageLoad('auth/login', () => {
    document.getElementById('submit').addEventListener('click', (event) => {
        login();
    });
    document.getElementById('oauth').addEventListener('click', (event) => {
        oauth();
    });
})