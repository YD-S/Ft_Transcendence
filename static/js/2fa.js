import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";
import {t} from "./translation.js";


PageManager.getInstance().setOnPageLoad("auth/2fa", (email2fa, user_id) => {
    if (!email2fa) {
        window.global.pageManager.load('auth/login')
    }
    document.getElementById('email-message').innerText = t(`AUTH.TFA.EMAIL_SENT_MESSAGE`);

    document.getElementById('submit')
        .addEventListener('click', (event) => {
            let code = document.getElementById('code').value;
            let data = {
                code: code,
                user_id: user_id
            };
            fetch('/api/auth/2fa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then(response => {
                    if (response.status >= 400) {
                        throw new Error("AUTH.ERROR.INVALID_2FA_CODE");
                    }
                    return response.json();
                })
                .then(data => {
                    window.global.saveToken(data);
                    PageManager.getInstance().load('home');
                })
                .catch((error) => {
                    Notification.error(error.message);
                });
        })

    document.getElementById('resend')
        .addEventListener('click', (event) => {
            let data = {
                user_id: user_id
            };
            fetch('/api/auth/resend-2fa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then(response => {
                    if (response.status >= 400) {
                        throw new Error("AUTH.ERROR.RESEND_2FA_CODE");
                    }
                    return response.json();
                })
                .then(data => {
                    Notification.success('AUTH.TFA.EMAIL_RESENT_MESSAGE');
                })
                .catch((error) => {
                    Notification.error(error.message);
                });
        })
})

