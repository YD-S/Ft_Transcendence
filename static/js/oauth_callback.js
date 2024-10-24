import {PageManager} from "./page-manager.js";
import {saveToken} from "./utils.js";
import {Notification} from "./notification.js";


PageManager.getInstance().setOnPageLoad('auth/oauth_callback', () => {
    const original_state = sessionStorage.getItem('oauth_state');
    sessionStorage.removeItem('oauth_state');
    const query = new URLSearchParams(window.location.search)
    const code = query.get('code');
    const state = query.get('state');
    if (!state || !code || state !== original_state) {
        Notification.error('AUTH.ERROR.INVALID_OAUTH_CALLBACK');
        PageManager.getInstance().load('auth/login', false);
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
            Notification.error('AUTH.ERROR.INVALID_OAUTH_CODE');
            PageManager.getInstance().load('auth/login', false);
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
                throw new Error("COMMON.ERROR.INVALID_ACTION");
        }
    })
})