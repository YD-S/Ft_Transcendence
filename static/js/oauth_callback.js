import {PageManager} from "./page-manager.js";
import {saveToken} from "./utils.js";


PageManager.getInstance().setOnPageLoad('auth/oauth_callback', () => {
    const original_state = sessionStorage.getItem('oauth_state');
    sessionStorage.removeItem('oauth_state');
    const query = new URLSearchParams(window.location.search)
    const code = query.get('code');
    const state = query.get('state');
    if (!state || !code || state !== original_state) {
        alert('Invalid OAuth callback');
        PageManager.getInstance().load('auth/login');
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
            alert('Invalid OAuth code');
            PageManager.getInstance().load('auth/login');
        }
        return response.json();
    }).then(data => {
        localStorage.removeItem('oauth_state');
        switch (data.action) {
            case "2fa":
                PageManager.getInstance().load('auth/2fa', false, {args: [data.email2fa, data.user_id]})
                break;
            case "login":
                saveToken(data)
                PageManager.getInstance().load('home', false);
                break;
            default:
                throw new Error("Invalid action");
        }
    })
})