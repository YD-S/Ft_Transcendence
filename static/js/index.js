function loadPage(page) {
    const contentMain = document.getElementById('main');

    fetch(`/${page}`)
    .then(response => response.text())
    .then(data => {
        contentMain.innerHTML = data;
    });
}

function settings(){
    loadPage('settings');
}

function neonPong() {
    const contentMain = document.getElementById('main');

    contentMain.style.setProperty('flex-direction', 'column');
    contentMain.innerHTML = `
    <button class="secondary-box" onclick="multiplayer()">
        MULTIPLAYER
    </button>
    <button class="primary-box">
        SINGLEPLAYER
    </button>
    `;
}

function multiplayer() {
    const contentMain = document.getElementById('main');

    contentMain.innerHTML = `
    <div style="display: flex; flex-wrap: wrap; width: 52.28vw; height: 42.18vh; flex-direction: column; gap: 1vh;">
        <button style="height: 20.5vh" class="primary-box" onclick="oneVSone()">
            1 vs 1
        </button>
        <button style="height: 20.5vh" class="secondary-box" onclick="twoVStwo()">
            2 vs 2
        </button>
        <button style="flex-direction: column; height: 42.18vh" class="accent-box">
            <img style="width: 10.41vw; height: 19.53vh" class="cup-pallete-svg" src="svg/cup.svg" alt="profile" onclick="tournament()">
            TOURNAMENT
        </button>
    </div>

    `;
}

function oneVSone() {
    const contentMain = document.getElementById('main');

    contentMain.innerHTML = `
    <div style="display: flex; width: 26.14vw; height: 19.43vh; flex-direction: column; gap: 6vh; align-items: center; justify-content: center;">
         <div style="display: flex; width: 26.14vw; height: 19.43vh; flex-direction: column; gap: 1vh;">
            <button style="height: 9.66vh" class="primary-box">
                Panesico
            </button>
        </div>
        <div style="color: var(--accent-color); font-size: 5vw; display: flex; align-items: center; justify-content: center;">
            vs
        </div>   
        <div style="display: flex; width: 26.14vw; height: 19.43vh; flex-direction: column; gap: 1vh;">
            <button style="height: 9.66vh" class="secondary-box">
                Panesico
            </button>
        </div>
    </div>
    `;
}

function twoVStwo() {
    const contentMain = document.getElementById('main');

    contentMain.innerHTML = `
    <div style="display: flex; width: 52.28vw; height: 42.18vh; flex-direction: row; gap: 6vh; align-items: center; justify-content: center;">
         <div style="display: flex; width: 26.14vw; height: 19.43vh; flex-direction: column; gap: 1vh;">
            <button style="height: 9.66vh" class="primary-box">
                Panesico
            </button>
            <button style="height: 9.66vh" class="primary-box">
                ...
            </button>
        </div>
        <div style="color: var(--accent-color); font-size: 5vw;">
            vs
        </div>   
        <div style="display: flex; width: 26.14vw; height: 19.43vh; flex-direction: column; gap: 1vh;">
            <button style="height: 9.66vh" class="secondary-box">
                Panesico
            </button>
            <button style="height: 9.66vh" class="secondary-box">
                ...
            </button>
        </div>
    </div>
    `;
}

function tournament() {

    const contentMain = document.getElementById('main');

    contentMain.innerHTML = `
    <div style="display: flex; width: 95vw; height: 11vh; flex-direction: row; justify-content: space-between; align-items: center">
        <div style="display: flex; flex-direction: column;">
            <div style="width: 19vw; height: 11vh; display: flex; flex-direction: column; flex-wrap: wrap; justify-content: space-between"">
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="primary-box" onclick="oneVSone()">
                    ...
                </button>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="primary-box" onclick="twoVStwo()">
                    ...
                </button>
                <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                    </div>
                </div>
                <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
                <div style="height: 5.27vh; width: 1vw; display: flex; align-items: center">
                    <div style="width: 0; height: 12.1vh; border: 1px solid var(--primary-darker-color); margin-top: 11.9vh">
                        
                    </div>
                </div>
            </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.7vh">
            <div style="width: 20.5vw; height: 11vh; display: flex; flex-direction: column; flex-wrap: wrap; justify-content: space-between">
            
                <div style="height: 12.1vh; width: 2vw; display: flex; align-items: center; justify-content: right">
                    <div style="width: 0; height: 11vh; border: 1px solid var(--primary-darker-color); margin-top: 5vh">
                        
                    </div>
                </div>
            
                            <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                    </div>
                </div>
                <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="secondary-box" onclick="oneVSone()">
                    ...
                </button>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="secondary-box" onclick="twoVStwo()">
                    ...
                </button>


            </div>
        </div>
    </div>
    <div style="display: flex; width: 80vw; height: 11vh; flex-direction: row; justify-content: center">
        <div style="display: flex; flex-direction: column; flex-wrap: wrap; width: 16.7vw; height: 11vh; justify-content: space-between">
            <div style="display: flex; flex-direction: column; justify-content: space-between; height: 11vh">
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="primary-box" onclick="oneVSone()">
                    ...
                </button>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="primary-box" onclick="twoVStwo()">
                    ...
                </button>
            </div>
            <div style="display: flex; flex-direction: column; justify-content: space-between; height: 11vh">
                <div style="height: 5.27vh; width: 1.27vw; display: flex; align-items: center;">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                    </div>
                </div>
                <div style="height: 5.27vh; width: 1.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
    
            </div>
            
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 11vh">
                <div style="height: 11vh; width: 1px; display: flex; align-items: center">
                    <div style="width: 0; height: 5.9vh; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
            </div>
           
            <div style="height: 11vh; width: 1.27vw; display: flex; align-items: center">
                <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                </div>
            </div>
    
        </div>

        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="primary-box" onclick="oneVSone()">
                ...
            </button>
        </div>

        <div style="color: var(--accent-color); font-size: 5vw; height: 12.6vh; display: flex; align-items: center; justify-content: center; padding-right: 2vw; padding-left: 2vw">
            <div style="padding-bottom: 2.2vh">vs</div>
        </div>   
        
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="secondary-box" onclick="oneVSone()">
                ...
            </button>
        </div>
        
        <div style="display: flex; flex-direction: column; flex-wrap: wrap; width: 16.7vw; height: 11vh; justify-content: space-between">
            <div style="height: 11vh; width: 1.27vw; display: flex; align-items: center">
                <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                </div>
            </div>
            
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 11vh">
                <div style="height: 11vh; width: 1px; display: flex; align-items: center">
                    <div style="width: 0; height: 5.9vh; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
            </div>
            
            <div style="display: flex; flex-direction: column; justify-content: space-between; height: 11vh">
                <div style="height: 5.27vh; width: 1.27vw; display: flex; align-items: center;">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                    </div>
                </div>
                <div style="height: 5.27vh; width: 1.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
    
            </div>
          
            <div style="display: flex; flex-direction: column; justify-content: space-between; height: 11vh">
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="secondary-box" onclick="oneVSone()">
                    ...
                </button>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="secondary-box" onclick="twoVStwo()">
                    ...
                </button>
            </div>
        </div>
    </div>
    <div style="display: flex; width: 95vw; height: 11vh; flex-direction: row; justify-content: space-between">
        <div style="display: flex; flex-direction: column; justify-content: space-between">
            <div style="width: 19vw; height: 11vh; display: flex; flex-direction: column; flex-wrap: wrap; justify-content: space-between">
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="primary-box" onclick="oneVSone()">
                    ...
                </button>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="primary-box" onclick="twoVStwo()">
                    ...
                </button>
                <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                    </div>
                </div>
                <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
                <div style="height: 5.27vh; width: 1vw; display: flex; align-items: center">
                    <div style="width: 0; height: 11.4vh; border: 1px solid var(--primary-darker-color); margin-top: 1.4vh">
                        
                    </div>
                </div>
            </div>
        </div>
            <div style="width: 20.5vw; height: 11vh; display: flex; flex-direction: column; flex-wrap: wrap;">
                <div style="height: 11vh; width: 2vw; display: flex; align-items: center; justify-content: right">
                    <div style="width: 0; height: 11.4vh; border: 1px solid var(--primary-darker-color); margin-bottom: 6vh">
                        
                    </div>
                </div>
                            <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                    
                    </div>
                </div>
                <div style="height: 5.27vh; width: 4.27vw; display: flex; align-items: center">
                    <div style="width: 4.27vw; height: 0; border: 1px solid var(--primary-darker-color);">
                        
                    </div>
                </div>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="secondary-box" onclick="oneVSone()">
                    ...
                </button>
                <button style="height: 5.27vh; width: 14.27vw; font-size: 2.35vw" class="secondary-box" onclick="twoVStwo()">
                    ...
                </button>


            </div>
        </div>
    </div>
    `;

}
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