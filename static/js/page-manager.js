export class PageManager {

    previousPage = null;

    onLoadCallbacks = {};
    onUnloadCallbacks = {};

    static __instance = null;


    constructor() {
        this.contentRoot = document.getElementById('root');
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

    /**
     * Load a page into the content root
     * @param page {string} The page to load
     * @param preserve_query {boolean} Whether to preserve the query string in the URL
     * @param options {object} Options for loading the page
     */
    load(page, preserve_query = true, options = {}) {
        this.loadToContainer(page, this.contentRoot, preserve_query, options)
    }

    combineQueries(qs1, qs2) {
        qs1 = qs1.startsWith('?') ? qs1.slice(1) : qs1;
        qs2 = qs2.startsWith('?') ? qs2.slice(1) : qs2;

        const params1 = new URLSearchParams(qs1);
        const params2 = new URLSearchParams(qs2);

        for (const [key, value] of params2) {
            params1.set(key, value);
        }

        return `?${params1.toString()}`;
    }

    loadToContainer(page, container, preserve_query = true, options = {}) {
        this.setLoading(container);
        return fetch(`/page/${page}.html` + this.combineQueries(window.location.search, (options.query || "")))
            .then(response => {
                if (response.status !== 200) {
                    if (response.status === 401) {
                        this.load('auth/login', false)
                    } else {
                        this.load('home')
                    }
                    return '__redirected__'
                }
                return response.text();
            })
            .then(data => {
                if (data === '__redirected__') {
                    return
                }
                if (options.storeInHistory !== false) {
                    const url = '/' + page + (preserve_query ? window.location.search : "")
                    history.pushState({data: data}, "", url);
                    console.log(url)
                }
                container.innerHTML = data;
                if (this.onUnloadCallbacks[this.previousPage]) {
                    this.onUnloadCallbacks[this.previousPage]();
                }
                if (this.onLoadCallbacks[page]) {
                    this.onLoadCallbacks[page](...(options.args || []));
                }
                if (options.storeInHistory !== false) {
                    this.previousPage = page;
                }
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

	setLoading(container) {
		container.innerHTML = `<div class='loader'>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
        </div>`;
	}
}
