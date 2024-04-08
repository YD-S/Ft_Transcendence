import {invertColors, login, logout} from "./utils.js";
import {PageManager} from "./page-manager.js";

export class Global {
    constructor() {
        this.pageManager = PageManager.getInstance();
        this.invertColors = invertColors;
        this.login = login;
        this.logout = logout;
    }
}