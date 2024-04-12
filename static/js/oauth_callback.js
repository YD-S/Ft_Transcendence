import {PageManager} from "./page-manager.js";
import {saveToken} from "./utils.js";


PageManager.getInstance().setOnPageLoad('oauth_callback', () => {
    const original_state = sessionStorage.getItem('oauth_state');
    sessionStorage.removeItem('oauth_state');
    const query = new URLSearchParams(window.location.search)
    const code = query.get('code');
    const state = query.get('state');
    if (!state || !code || state !== original_state) {
        alert('Invalid OAuth callback');
        PageManager.getInstance().load('login');
        return;
    }

    fetch('/api/auth/oauth_login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({code: code})
    }).then(response => {
        if (response.status >= 400) {
            throw new Error("Invalid OAuth code");
        }
        return response.json();
    }).then(data => {
        localStorage.removeItem('oauth_state');
        saveToken(data)
        PageManager.getInstance().load('home', false);
    })
})