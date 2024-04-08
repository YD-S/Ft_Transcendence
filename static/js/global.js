import {invertColors, login, logout} from "./utils.js";
import {PageManager} from "./pageManager.js";

export class Global {
    constructor() {
        this.pageManager = PageManager.getInstance();
        this.invertColors = invertColors;
        this.login = login;
        this.logout = logout;
    }
}