import {PageManager} from "./page-manager.js";
import {Notification} from "./notification.js";


PageManager.getInstance().setOnPageLoad("auth/2fa", (email2fa, user_id) => {
    if (!email2fa) {
        window.global.pageManager.load('auth/login')
    }
    document.getElementById('email-message').innerText = `Se ha enviado un correo con el código de verificación a su cuenta de correo`;

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
                        throw new Error("Invalid code");
                    }
                    return response.json();
                })
                .then(data => {
                    window.global.saveToken(data);
                    PageManager.getInstance().load('home');
                })
                .catch((error) => {
                    Notification.error(error);
                });
        })

    document.getElementById('resend')
        .addEventListener('click', (event) => {
            console.log('resend', user_id)
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
                        throw new Error("There was an error resending the email");
                    }
                    return response.json();
                })
                .then(data => {
                    Notification.success('Nuevo código enviado')
                })
                .catch((error) => {
                    Notification.error(error);
                });
        })
})

