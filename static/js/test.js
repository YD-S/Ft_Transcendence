import {PageManager} from "./page-manager.js";
import * as THREE from 'three';
import {height_aspect_ratio, makeBall, makeCamera, makePaddle, half, PAD_H, PAD_W} from './Objects.js';

const GAME_WIDTH = 1000;

const GAME_HEIGHT = height_aspect_ratio(GAME_WIDTH);

const WALL_HEIGHT = 20;

const WALL_DEPTH = 20;

const MAX_SCORE = 5;

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
}

const COLORS = {
    white: 0xf8f9fa,
    purple: 0x7858dc,
    pink: 0xc3a5ec,
    space_cadet: 0x202646,
};

class NeonPong {
    constructor() {
        this.websocket = new WebSocket(`wss://${window.location.host}/ws/matchmaking/`);
        this.amIfirst = false;
        this.me = null;
        this.opponent = null;
        this.keys = {};
        this.twoD = false;
        this.scene = new THREE.Scene();
        this.camera = makeCamera(this.twoD);
        this.renderer = new THREE.WebGLRenderer({antialias: true});
        this.renderer.setSize(GAME_WIDTH, GAME_HEIGHT);

        this.pivot =  new THREE.Object3D();
        this.pivot.rotation.y = Math.PI / 2;

        this.pivot2 = new THREE.Object3D();
        this.pivot2.rotation.y = -Math.PI / 2;


        const radius = 15;
        const sectors = 16;
        const rings = 8;
        const divisions = 64;

        const helper = new THREE.PolarGridHelper( radius, sectors, rings, divisions );
        this.scene.add( helper );

        //this.grid = new THREE.GridHelper(WALL_DEPTH, 10);
        //this.scene.add(this.grid);

        this.wall1 = new THREE.Mesh(new THREE.BoxGeometry(1, WALL_HEIGHT, WALL_DEPTH), new THREE.MeshBasicMaterial({color: COLORS.white}));
        this.wall1.position.set(half(WALL_DEPTH), half(WALL_DEPTH), 0);
        //this.scene.add(this.wall1);

        this.wall2 = new THREE.Mesh(new THREE.BoxGeometry(1, WALL_HEIGHT, WALL_DEPTH), new THREE.MeshBasicMaterial({color: COLORS.white}));
        this.wall2.position.set(-half(WALL_DEPTH), half(WALL_DEPTH), 0);
        //this.scene.add(this.wall2);

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

        document.getElementById("game-canvas").appendChild(this.renderer.domElement);


        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "game_start") {
                console.log("Game started");
                this.amIfirst = data.player;
                if (this.amIfirst === true) {
                    this.me = this.pivot;
                    this.opponent = this.pivot2;
                }
                else {
                    this.me = this.pivot2;
                    this.opponent = this.pivot;
                }
                this.setCameraAngle();
            }
            else if (data.type === "move") {
                this.me.position.x = data.x;
            }
        }
    }
    setCameraAngle() {
        if (this.twoD === false) {
            this.camera.position.set(-20, 25, 20);
            this.scene.rotation.y = -Math.PI / 2;
            this.camera.lookAt(0, 0, 0);
        } else {
            this.camera.position.set(0, 25, 0);
            this.scene.rotation.y = -Math.PI / 2;
        }
    }

    checkPaddleWallCollision() {
        if (this.paddle1.position.x > half(WALL_DEPTH) - half(PAD_W) - 0.5) {
            this.paddle1.position.x = half(WALL_DEPTH) - half(PAD_W) - 0.5;
        }
        if (this.paddle1.position.x < -half(WALL_DEPTH) + half(PAD_W) + 0.5) {
            this.paddle1.position.x = -half(WALL_DEPTH) + half(PAD_W) + 0.5;
        }
        if (this.paddle2.position.x > half(WALL_DEPTH) - half(PAD_W) - 0.5) {
            this.paddle2.position.x = half(WALL_DEPTH) - half(PAD_W) - 0.5;
        }
        if (this.paddle2.position.x < -half(WALL_DEPTH) + half(PAD_W) + 0.5) {
            this.paddle2.position.x = -half(WALL_DEPTH) + half(PAD_W) + 0.5;
        }
    }

/*    updateCameraPosition() {
        if (this.twoD === false) {
            if (this.amIfirst === true) {
                this.camera.position.set(this.paddle1.position.x, this.paddle1.position.y + 1.5, this.paddle1.position.z + 9.5);
                this.camera.rotation.y = 0;
            } else {
                this.camera.position.set(this.paddle2.position.x, this.paddle2.position.y + 1.5, this.paddle2.position.z - 8.5);
                this.camera.rotation.y = Math.PI;
            }
        } else {
            this.camera.position.set(0, 25, 0);
            this.camera.lookAt(0, 0, 0);
        }
    }
*/
    movePaddles() {
        if(this.twoD === false){
            if (this.keys['a']) {
                this.me.rotation.y += 0.01;
                //this.websocket.send(JSON.stringify({type: "move", direction: "left", playerId: this.amIfirst, x: this.me.position.x}));
            }
            if (this.keys['d']) {
                this.me.rotation.y -= 0.01;
                //this.websocket.send(JSON.stringify({type: "move", direction: "right", playerId: this.amIfirst, x: this.me.position.x}));
            }
        }
        else {
            if (this.keys['w']) {
                this.websocket.send(JSON.stringify({type: "move", direction: "left", playerId: this.amIfirst, x: this.me.position.x}));
            }
            if (this.keys['s']) {
                this.websocket.send(JSON.stringify({type: "move", direction: "right", playerId: this.amIfirst, x: this.me.position.x}));
            }
        }
    }

    keydown(event) {
        this.keys[event.key] = true;
    }

    keyup(event) {
        this.keys[event.key] = false;
    }

    render() {
        requestAnimationFrame(this.render.bind(this));
        this.movePaddles();
        this.renderer.render(this.scene, this.camera);
        this.checkPaddleWallCollision(); // Check for paddle wall collision in the render loop
       // this.updateCameraPosition(); // Update camera position in the render loop
    }
}

PageManager.getInstance().setOnPageLoad("test", () => {

    const game = new NeonPong();
    game.render();

})