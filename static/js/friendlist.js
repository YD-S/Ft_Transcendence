
import {unfriendUser} from "./users.js";
import {PageManager} from "./page-manager.js";

const Listen = (doc) => {
    return {
        on: (type, selector, callback) => {
            const listener = (event)=>{
                if(!event.target.matches(selector)) return;
                callback.call(event.target, event);
            }
            doc.addEventListener(type, listener, false);
            return listener;
        },
        clear : (type, e) => {
            doc.removeEventListener(type, e);
        }
    }
};

function handler(e){
    unfriendUser(e.target.id, "friendlist");
}

let listener = null;

PageManager.getInstance().setOnPageLoad("friendlist", function() {
    listener = Listen(document).on('click', '.btn', handler);
});

PageManager.getInstance().setOnPageUnload("friendlist", function() {
    Listen(document).clear('click', listener);
});