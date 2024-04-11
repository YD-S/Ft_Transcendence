import {PageManager} from "./page-manager.js";


PageManager.getInstance().setOnPageLoad("2fa", (email2fa, user_id) => {
    if (!email2fa) {
        window.global.pageManager.load('login')
    }
    localStorage.setItem('user_id', user_id);
    document.getElementById('email-message').innerText = `Se ha enviado un correo con el código de verificación a ${email2fa}`;

    document.getElementById('submit')
        .addEventListener('click', (event) => {
            let code = document.getElementById('code').value;
            let data = {
                code: code,
                user_id: localStorage.getItem('user_id')
            };
            localStorage.removeItem('user_id');
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
                    alert(error);
                });
        })
})

