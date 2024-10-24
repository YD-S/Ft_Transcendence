import { PageManager } from "./page-manager.js";
import {Notification} from "./notification.js";

export function changeLanguage(language) {
	setCookie("django_language", language, { path: "/", Domain: window.location.hostname });
	document.getElementById(language).checked = true;
	location.reload();
}

export function logout() {
	fetch("/api/auth/logout/", { method: "POST" })
		.then((response) => {
			if (response.status !== 200) {
				throw new Error("Logout failed");
			}
			deleteCookie("Authorization");
			sessionStorage.removeItem("refresh_token");
			sessionStorage.removeItem("access_token");
		})
		.catch((error) => {
			Notification.error(error.message);
		});
	PageManager.getInstance().load("auth/login");
}

export function setCookie(name, value, attributes) {
	let cookie = `${name}=${value};`;
	Object.keys(attributes).forEach((key) => {
		cookie += typeof attributes[key] === "boolean" ? `${key};` : `${key}=${attributes[key]}; `;
	});
	document.cookie = cookie;
}

export function getCookie(name) {
	let cookie = document.cookie.split(";").find((cookie) => cookie.trim().startsWith(name + "="));
	return cookie ? cookie.split("=")[1] : null;
}

export function deleteCookie(name) {
	document.cookie = `${name}=; Max-Age=-99999999;`;
}

function refreshToken() {
	let refresh_token = sessionStorage.getItem("refresh_token");
	fetch("/api/auth/refresh/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ refresh_token: refresh_token }),
	})
		.then((response) => {
			if (response.status !== 200) {
				throw new Error("Refresh failed");
			}
			return response.json();
		})
		.then((data) => {
			saveToken(data);
		})
		.catch((error) => {
			Notification.error(error.message);
		});
}

export function saveToken(data) {
	setCookie("Authorization", `${data.access_token}`, {
		path: "/",
		expires: new Date(data.access_expiration * 1000),
		SameSite: "None",
		Secure: true,
	});
	setCookie("refresh_token", data.refresh_token, {
		path: "/",
		expires: new Date(data.refresh_expiration * 1000),
		SameSite: "None",
		Secure: true,
	});
	setTimeout(() => refreshToken(), data.access_expiration * 1000 - Date.now() - 1000); // Refresh token 1 second before expiration
}
