import {PageManager} from "./page-manager.js";
import Matchmaking from "./Matchmaking.js";
import * as THREE from 'three';
import {height_aspect_ratio, makeBall, makeCamera, makePaddle, makeGrid} from './Objects.js';

const GAME_WIDTH = 1000;
const GAME_HEIGHT = height_aspect_ratio(GAME_WIDTH);

const PLAYER_COLORS = {
    mindaro: 0xe2ef70,
    verdigris: 0x16bac5,
    jade: 0x00a878,
    golden_gate: 0xeb4511,
    pear: 0xd1d646,
    sunset: 0xffcb77,
    aqua: 0x42f2f7,
    persian_blue: 0x072ac8,
    emerald: 0x48bf84,
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
        this.twoD = false;
        this.keys = {};

        this.sendIntialData();

        this.camera = makeCamera(this.twoD);
        this.scene = new THREE.Scene();
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(GAME_WIDTH, GAME_HEIGHT);

        this.pivot = new THREE.Object3D();
        this.pivot.rotation.y = Math.PI / 2;

        this.pivot2 = new THREE.Object3D();
        this.pivot2.rotation.y = -Math.PI / 2;

        const helper = makeGrid();
        this.scene.add(helper);

        document.addEventListener('keydown', this.keydown.bind(this));
        document.addEventListener('keyup', this.keyup.bind(this));

        this.paddle1 = makePaddle(PLAYER_COLORS.emerald);
        this.paddle1.position.set(0, 0.5, 15);
        this.pivot.add(this.paddle1);

        this.paddle2 = makePaddle(PLAYER_COLORS.aqua);
        this.paddle2.position.set(this.paddle1.position.x, this.paddle1.position.y, this.paddle1.position.z);
        this.pivot2.add(this.paddle2);

        this.ball = makeBall(COLORS.pink);
        this.ball.position.set(0, 5, 0);
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
                    this.me.rotation.y = message.player1_y;
                    this.opponent.rotation.y = message.player2_y;
                }
                else {
                    this.me.rotation.y = message.player2_y;
                    this.opponent.rotation.y = message.player1_y;
                }
                break;
        }
    }

    sendIntialData(){
        let Player1;
        let Player2;
            if (this.amIfirst){
                Player1 = this.playerId;
                Player2 = this.opponentId
            }else {
                Player2 = this.playerId;
                Player1 = this.opponentId
            }
        this.GameSocket.send(JSON.stringify(
            {
                type: "initial_data",
                Player1: Player1,
                Player2: Player2,
                amIfirst: this.amIfirst,
            }
        ));
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
        if (this.twoD === false) {
            console.log("3D");
            this.camera.position.set(-20, 25, 20);
            this.scene.rotation.y = -Math.PI / 2;
            this.camera.lookAt(0, 0, 0);
        } else {
            console.log("2D");
            this.camera.position.set(0, 25, 0);
            this.scene.rotation.y = -Math.PI / 2;
        }
    }

    movePaddles() {
        const directionMap = this.twoD ? { 'w': 'left', 's': 'right' } : { 'a': 'left', 'd': 'right' };

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

// Ensure WebSocket is ready before starting the game
PageManager.getInstance().setOnPageLoad("test", () => {
    const matchmaking = new Matchmaking();
    matchmaking.onGameSocketReady = () => {
        const game = new NeonPong(matchmaking);
        game.render();
    };
});
