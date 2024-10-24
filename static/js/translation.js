import {getCookie} from "./utils.js";
import * as en from './lang/en.js';
import * as es from './lang/es.js';
import * as pt from './lang/pt.js';

const locales = {
    'en-US': en.locale,
    'es-ES': es.locale,
    'pt-PT': pt.locale,
}

export function t(key) {
    const lang = getCookie('django_language');

    let locale = locales[lang];

    return lookup(key, locale);
}

function lookup(path, locale) {
    let aPath = path.split('.');
    try {
        return aPath.reduce((a, v) => a[v], locale);
    } catch {
        try {
            return aPath.reduce((a, v) => a[v], locales['en-US']);
        } catch {
            return path;
        }
    }
}