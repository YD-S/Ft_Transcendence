function loadPage(page) {
    const contentMain = document.getElementById('main');

    fetch(`/${page}`)
    .then(response => response.text())
    .then(data => {
        contentMain.innerHTML = data;
    });
}

window.onload = () => loadPage('home');

function invertColors() {
    const rootStyles = getComputedStyle(document.documentElement);
    const variableNames = [
        '--primary-color',
        '--primary-darker-color',
        '--secondary-color',
        '--secondary-darker-color',
        '--tertiary-color',
        '--tertiary-darker-color',
        '--accent-color',
        '--accent-darker-color',
        '--background-color',
        '--background-secondary-color'
    ];
    variableNames.forEach((variable) => {
        console.log(rootStyles.getPropertyValue(variable));
        document.documentElement.style.setProperty(variable, invertColor(rootStyles.getPropertyValue(variable)));
    });
}

function invertColor(hex) {
    if (hex.indexOf('#') === 0) {
        hex = hex.slice(1);
    }
    // convert 3-digit hex to 6-digits.
    if (hex.length === 3) {
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
    if (hex.length !== 6) {
        throw new Error('Invalid HEX color.');
    }
    // invert color components
    var r = (255 - parseInt(hex.slice(0, 2), 16)).toString(16),
        g = (255 - parseInt(hex.slice(2, 4), 16)).toString(16),
        b = (255 - parseInt(hex.slice(4, 6), 16)).toString(16);
    // pad each with zeros and return
    return '#' + padZero(r) + padZero(g) + padZero(b);
}

function padZero(str, len) {
    len = len || 2;
    var zeros = new Array(len).join('0');
    return (zeros + str).slice(-len);
}