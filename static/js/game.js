import Ball from "./Ball.js";
import Paddle from "./Paddle.js";
import {PageManager} from "./page-manager.js";

const  WINNING_SCORE = 1;
export class Game {
    constructor() {
        this.tournament = false;
        window.game = this;
        this.paddleSpeed = 1;
        this.keys = {};
        this.gameEndEvent = new CustomEvent('gameEnd', {
            detail: { winner: null },
            bubbles: true,
            cancelable: true,
            composed: false,
        });
        this.ball = new Ball(document.getElementById('ball'));
        this.paddle1 = new Paddle(document.getElementById('player1_paddle'), 1);
        this.paddle2 = new Paddle(document.getElementById('player2_paddle'), 2);
        this.Team1_score = document.getElementById('score__p1');
        this.Team2_score = document.getElementById('score__p2');
        this.lastTimestamp = null;
        this.accumulatedTime = 0;

        this.fixedTimeStep = 1000 / 60; // 60 FPS or 16.67ms per frame

        this.destroyed = false;

        document.addEventListener('keydown', this.keydown.bind(this));
        document.addEventListener('keyup', this.keyup.bind(this));

        this.lastTimestamp = Date.now();
        if (!this.destroyed)
            window.requestAnimationFrame(this.update.bind(this));
    }

    keydown(event) {
        this.keys[event.key] = true;
    }

    keyup(event) {
        this.keys[event.key] = false;
    }

    update(timestamp) {
        if (this.destroyed) return;
        const currentTimestamp = Date.now();
        const deltaTime = currentTimestamp - this.lastTimestamp;

        this.accumulatedTime += deltaTime;

        while (this.accumulatedTime >= this.fixedTimeStep) {
            this.movePaddles();
            this.ball.update(this.fixedTimeStep, [this.paddle1.rect(), this.paddle2.rect()]);
            this.paddle1.update();
            this.paddle2.update();

            if (this.pointScored()) this.handleScore();

            this.accumulatedTime -= this.fixedTimeStep;
        }

        this.lastTimestamp = currentTimestamp;

        if (!this.destroyed) {
            window.requestAnimationFrame(this.update.bind(this));
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

    handleScore() {
        const rect = this.ball.rect();
        if (rect.right >= window.innerWidth) {
            this.Team1_score.textContent = parseInt(this.Team1_score.textContent) + 1;
        } else {
            this.Team2_score.textContent = parseInt(this.Team2_score.textContent) + 1;
        }
        if (parseInt(this.Team1_score.textContent) >= WINNING_SCORE) {
            this.endGame("Player 1 Wins!");
        } else if (parseInt(this.Team2_score.textContent) >= WINNING_SCORE) {
            this.endGame("Player 2 Wins!");
        } else {
            this.ball.reset();
            this.paddle1.reset();
            this.paddle2.reset();
            this.accumulatedTime = 0;
        }
    }

    endGame(winnerMessage) {
        alert(winnerMessage);
        this.destroy();
        if (!this.tournament) {
            PageManager.getInstance().load('home');
        }else{
           this.gameEndEvent.detail.winner = this.getWinner();
            window.dispatchEvent(this.gameEndEvent);

        }
    }
    pointScored() {
        const rect = this.ball.rect();
        return rect.right >= window.innerWidth || rect.left <= 0;
    }

    destroy() {
        document.removeEventListener('keydown', this.keydown.bind(this));
        document.removeEventListener('keyup', this.keyup.bind(this));
        this.destroyed = true;
    }

    getWinner() {
        return parseInt(this.Team1_score.textContent) >= WINNING_SCORE ? "Player 1" : "Player 2";
    }

    isGameOver() {
        return parseInt(this.Team1_score.textContent) >= WINNING_SCORE || parseInt(this.Team2_score.textContent) >= WINNING_SCORE;
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
