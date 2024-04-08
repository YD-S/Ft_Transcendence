export class PageManager {

    previousPage = null;

    onLoadCallbacks = {};
    onUnloadCallbacks = {};

    static __instance = null;


    constructor() {
        this.contentRoot = document.getElementById('main');
        window.addEventListener('popstate', (event) => {
            this.contentRoot.innerHTML = event.state.data;
        });

        if (PageManager.__instance === null) {
            PageManager.__instance = this;
        }

        return PageManager.__instance
    }

    /**
     * Get the singleton instance of the PageManager
     * @returns {PageManager} The singleton instance of the PageManager
     */
    static getInstance() {
        if (this.__instance === null) {
            this.__instance = new PageManager();
        }
        return this.__instance;
    }

    load(page) {
        fetch(`/page/${page}.html`)
            .then(response => response.text())
            .then(data => {
                history.pushState({data: data}, "", page);
                this.contentRoot.innerHTML = data;
                if (this.onLoadCallbacks[page]) {
                    this.onLoadCallbacks[page]();
                }
                if (this.onUnloadCallbacks[this.previousPage]) {
                    this.onUnloadCallbacks[this.previousPage]();
                }
                this.previousPage = page;
            });
    }

    /**
     * Set a callback to be called when a page is loaded
     * @param page {string} The page to set the callback for
     * @param callback {function} The callback to be called when the page is loaded
     */
    setOnPageLoad(page, callback) {
        this.onLoadCallbacks[page] = callback;
    }

    /**
     * Set a callback to be called when a page is unloaded
     * @param page {string} The page to set the callback for
     * @param callback {function} The callback to be called when the page is unloaded
     */
    setOnPageUnload(page, callback) {
        this.onUnloadCallbacks[page] = callback;
    }

}