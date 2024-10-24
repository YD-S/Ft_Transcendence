import {t} from "./translation.js";

export class Notification {
    constructor(message, color, time) {
        this.message = message;
        this.color = color;
        this.time = time;
        this.element = null;
        let element = document.createElement('div');
        element.className = "toast-notification position-absolute top-0 end-0 mx-3 rounded";
        this.element = element;
        let countElements = document.getElementsByClassName("toast-notification");

        element.style.marginTop = `${5 + countElements.length * 55}px`;
        element.style.opacity = 0.8;

        element.style.backgroundColor = this.color;

        const messageContainer = document.createElement("div");
        messageContainer.className = "message-container p-2 px-3";
        messageContainer.textContent = this.message;

        element.appendChild(messageContainer);

        const close = document.createElement("div");
        close.className = "close-notification";

        const icon = document.createElement("i");
        icon.className = "lni lni-close";


        close.appendChild(icon);


        element.append(close);

        document.body.appendChild(element);

        setTimeout(function () {
            element.remove();
        }, this.time);

        close.addEventListener("click", () => {
            element.remove();
        })
    }

    static success(message, time = 3000) {
        new Notification(t(message), NotificationType.Succes, time);
    }

    static warning(message, time = 3000) {
        new Notification(t(message), NotificationType.Warning, time);
    }

    static error(message, time = 3000) {
        new Notification(t(message), NotificationType.Danger, time);
    }
}

export const NotificationType = {
    Danger: "#eb3b5a",
    Warning: "#fdcb6e",
    Succes: "#00b894",
}
