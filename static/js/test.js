import {PageManager} from "./page-manager.js";
import Matchmaking from "./Matchmaking.js";
import * as THREE from 'three';
import {height_aspect_ratio, makeBall, makeCamera, makePaddle, makeGrid} from './Objects.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const GAME_WIDTH = 1000;
const GAME_HEIGHT = height_aspect_ratio(GAME_WIDTH);

const NEON_COLORS = {
    neon_magenta: 0xff00ff,  // Bright magenta
    electric_violet: 0x8f00ff,  // Deep electric violet
    neon_green: 0x39ff14,  // Bright neon green
    hot_pink: 0xff69b4,  // Vivid hot pink
    neon_cyan: 0x00ffff,  // Cyan
    electric_blue: 0x7df9ff,  // Light electric blue
    neon_orange: 0xff5f1f,  // Bright orange
    neon_yellow: 0xffff33,  // Pure neon yellow
    laser_lemon: 0xfefe22,  // Vibrant lemon yellow
    neon_purple: 0xbc13fe,  // Neon purple
};

const COLORS = {
    white: 0xf8f9fa,
    purple: 0x7858dc,
    pink: 0xc3a5ec,
    space_cadet: 0x202646,
};

class NeonPong {
    constructor(matchmaking) {
        this.Matchmaking = matchmaking;
        this.GameSocket = this.Matchmaking.GameSocket;
        this.me = null;
        this.opponent = null;
        this.amIfirst = this.Matchmaking.amIfirst;
        this.playerId = this.Matchmaking.playerId;
        this.opponentId = this.Matchmaking.opponentId;
        this.keys = {};

        this.camera = makeCamera();
        this.scene = new THREE.Scene();
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(GAME_WIDTH, GAME_HEIGHT);

        this.pivot = new THREE.Object3D();
        this.pivot.rotation.y = 0;

        this.pivot2 = new THREE.Object3D();
        this.pivot2.rotation.y = 0;

        const helper = makeGrid();
        this.scene.add(helper);
        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambientLight);
        const pointLight = new THREE.PointLight(0xffffff, 1, 100);
        pointLight.position.set(5, 5, 5);
        this.scene.add(pointLight);

        const composer = new EffectComposer(this.renderer);
        const renderPass = new RenderPass(this.scene, this.camera);
        composer.addPass(renderPass);

        const bloomPass = new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.5, 0.4, 0.85);
        composer.addPass(bloomPass);

        document.addEventListener('keydown', this.keydown.bind(this));
        document.addEventListener('keyup', this.keyup.bind(this));
        window.addEventListener('onpagehide', this.disconnectWebSocket.bind(this));

        this.paddle1 = makePaddle(NEON_COLORS.neon_magenta);
        this.paddle1.position.set(0, 0.5, 15);
        this.pivot.add(this.paddle1);

        this.paddle2 = makePaddle(NEON_COLORS.laser_lemon);
        this.paddle2.position.set(this.paddle1.position.x, this.paddle1.position.y, this.paddle1.position.z);
        this.pivot2.add(this.paddle2);

        this.ball = makeBall(COLORS.pink);

        this.ball.position.set(0, 0, 0);

        this.scene.add(this.ball);

        this.scene.add(this.pivot);
        this.scene.add(this.pivot2);

        this.setPlayers();
        this.setCameraAngle();

        document.getElementById("game-canvas").appendChild(this.renderer.domElement);

        this.GameSocket.onmessage = async (event) => {
            await this.handleMessage(event);
        };
    }

    disconnectWebSocket() {
        if (this.GameSocket) {
            this.GameSocket.close();
            console.log('WebSocket connection closed');
        }
    }

    async handleMessage(event) {
        try {
            const message = JSON.parse(event.data);
            await this.processMessage(message);
        } catch (error) {
            console.error("Error handling message: ", error);
        }
    }

    async processMessage(message) {
        switch (message.type) {
            case "move":
                if (this.amIfirst) {
                    this.me.rotation.y = -message.player1_y + Math.PI / 2;
                    this.opponent.rotation.y = -message.player2_y + Math.PI / 2;
                }
                else {
                    this.me.rotation.y = -message.player2_y + Math.PI / 2;
                    this.opponent.rotation.y = -message.player1_y + Math.PI / 2;
                }
                this.ball.position.x = message.ball_x;
                this.ball.position.z = message.ball_y;
                this.ball.position.y = (((message.ball_x * message.ball_x + message.ball_y * message.ball_y) / -60) + 3.4) * 2;
                console.log(message)
                const s1 = document.getElementById("score1");
                if (s1) s1.innerText = message.player1_score;
                const s2 = document.getElementById("score2");
                if (s2) s2.innerText = message.player2_score;
                break;
            case "winner" :
                console.log("winner is: " + message.winner);
                this.GameSocket.close();
                PageManager.getInstance().load("home");
                break;
        }
    }


    setPlayers() {
        if (this.amIfirst === true) {
            this.me = this.pivot;
            this.opponent = this.pivot2;
        } else {
            this.me = this.pivot2;
            this.opponent = this.pivot;
        }
    }

    setCameraAngle() {
        this.camera.position.set(-20, 25, 20);
        this.scene.rotation.y = -Math.PI / 2;
        this.camera.lookAt(0, 0, 0);
    }

    movePaddles() {
        const directionMap ={ 'a': 'left', 'd': 'right' };

        for (let key in directionMap) {
            if (this.keys[key]) {
                this.GameSocket.send(JSON.stringify({
                    type: "move",
                    direction: directionMap[key],
                    amIfirst: this.amIfirst,
                }));
            }
        }
    }
    keydown(event) {
        if (event.repeat) {
            return;
        }
        this.keys[event.key] = true;
    }

    keyup(event) {
        if (event.repeat) {
            return;
        }
        this.keys[event.key] = false;
    }

    render() {
        requestAnimationFrame(this.render.bind(this));
        this.movePaddles();
        this.renderer.render(this.scene, this.camera);
    }
}

let game = null;
// Ensure WebSocket is ready before starting the game
PageManager.getInstance().setOnPageLoad("test", () => {
    const matchmaking = new Matchmaking();
    matchmaking.onGameSocketReady = () => {
        game = new NeonPong(matchmaking);
        game.render();
    };
});

PageManager.getInstance().onUnloadCallbacks["test"] = () => {
    if (game) {
        game.GameSocket.send(JSON.stringify({
            type: "leave",
            playerId: game.playerId,
        }));
    }
}
