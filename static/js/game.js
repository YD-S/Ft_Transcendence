import Ball from "./Ball.js";
import Paddle from "./Paddle.js";
import {PageManager} from "./page-manager.js";

export class Game {
    constructor() {
        this.paddleSpeed = 10;
        this.keys = {};

        this.maxY = window.innerHeight - 100;
        this.minY = 50;

        this.ball = new Ball(document.getElementById('ball'), this.maxY, this.minY);
        this.paddle1 = new Paddle(document.getElementById('player1_paddle'), 1, this.maxY, this.minY);
        this.paddle2 = new Paddle(document.getElementById('player2_paddle'), 2, this.maxY, this.minY);
        this.Team1_score = document.getElementById('score__p1');
        this.Team2_score = document.getElementById('score__p2');
        this.lastTimestamp = null;

        this.destroyed = false;

        document.addEventListener('keydown', this.keydown.bind(this));

        document.addEventListener('keyup', this.keyup.bind(this));

        this.lastTimestamp = Date.now();
        window.requestAnimationFrame(() => this.update(this.lastTimestamp));
    }

    keydown(event) {
        this.keys[event.key] = true;
    }

    keyup(event) {
        this.keys[event.key] = false;
    }

    update(timestamp) {
        if (this.lastTimestamp != null) {
            const delta = (Date.now() - timestamp);
            this.movePaddles();

            this.ball.update(15, [this.paddle1.rect(), this.paddle2.rect()]);
            this.paddle1.update();
            this.paddle2.update();
            if (this.isLose()) this.handleLost();
        }
        this.lastTimestamp = Date.now();
        if (!this.destroyed) {
            window.requestAnimationFrame(() => this.update(this.lastTimestamp));
        }
    }

    movePaddles() {
        if (this.keys['w'] || this.keys['W']) {
            this.paddle1.position -= this.paddleSpeed;
        }
        if (this.keys['s'] || this.keys['S']) {
            this.paddle1.position += this.paddleSpeed;
        }
        if (this.keys['ArrowUp']) {
            this.paddle2.position -= this.paddleSpeed;
        }
        if (this.keys['ArrowDown']) {
            this.paddle2.position += this.paddleSpeed;
        }
    }


    handleLost() {
        const rect = this.ball.rect();
        if (rect.right >= window.innerWidth) {
            this.Team1_score.textContent = parseInt(this.Team1_score.textContent) + 1;
        } else
            this.Team2_score.textContent = parseInt(this.Team2_score.textContent) + 1;
        this.ball.reset();
        this.paddle1.reset();
        this.paddle2.reset();
        this.lastTimestamp = null;
    }

    isLose() {
        const rect = this.ball.rect();
        return rect.right >= window.innerWidth || rect.left <= 0;
    }

    destroy() {
        document.removeEventListener('keydown', this.keydown.bind(this));
        document.removeEventListener('keyup', this.keyup.bind(this));
        this.destroyed = true;
    }
}

let game = null;

PageManager.getInstance().setOnPageLoad('pong/game', () => {
    game = new Game();
})

PageManager.getInstance().setOnPageUnload('pong/game', () => {
    if (game) {
        game.destroy();
        game = null;
    }
})
