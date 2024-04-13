import {changeLanguage, logout, saveToken} from "./utils.js";
import {PageManager} from "./page-manager.js";

export class Global {
    constructor() {
        this.pageManager = PageManager.getInstance();
        this.logout = logout;
        this.saveToken = saveToken;
        this.changeLanguage = changeLanguage
    }
}