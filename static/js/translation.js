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
    let val = key;
    if (!lang) {
        val = lookup(key, locales['en-US']);
    } else {
        val = lookup(key, locales[lang]);
    }
    return val;
}

function lookup(path, locale) {
    let aPath = path.split('.');
    try {
        return aPath.reduce((a, v) => a[v], locale) || path;
    } catch {
        try {
            return aPath.reduce((a, v) => a[v], locales['en-US']) || path;
        } catch {
            return path;
        }
    }
}