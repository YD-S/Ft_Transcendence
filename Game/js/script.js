
import Ball from "./Ball.js";
import Paddle from "./Paddle.js";

const paddleSpeed = 1;
const keys = {};
const ball = new Ball(document.getElementById('ball'));
const paddle1 = new Paddle(document.getElementById('player1_paddle'));
const paddle2 = new Paddle(document.getElementById('player2_paddle'));
const player1_score = document.getElementById('score__p1');
const player2_score = document.getElementById('score__p2');

let lastTimestamp;
function update(timestamp) {
    if (lastTimestamp != null) {
        const delta = (timestamp - lastTimestamp);
        movePaddles();
        ball.update(delta, [paddle1.rect(), paddle2.rect()]);
        paddle1.update();
        paddle2.update();
        if(isLoose()) handleLost();
    }
    lastTimestamp = timestamp;
    window.requestAnimationFrame(update);
}

document.addEventListener('keydown', event => {
    keys[event.key] = true;
});

document.addEventListener('keyup', event => {
    keys[event.key] = false;
});

function movePaddles() {
    if (keys['w'] || keys['W']) {
        paddle1.position -= paddleSpeed;
    }
    if (keys['s'] || keys['S']) {
        paddle1.position += paddleSpeed;
    }
    if (keys['ArrowUp']) {
        paddle2.position -= paddleSpeed;
    }
    if (keys['ArrowDown']) {
        paddle2.position += paddleSpeed;
    }
}

window.requestAnimationFrame(update);


function handleLost() {
    const rect = ball.rect();
    if(rect.right >= window.innerWidth) {
        player1_score.textContent = parseInt(player1_score.textContent) + 1;
    }
    else
        player2_score.textContent = parseInt(player2_score.textContent) + 1;
    ball.reset();
    paddle1.reset();
    paddle2.reset();
    lastTimestamp = null;
}

function isLoose() {
    const rect = ball.rect();
    return rect.right >= window.innerWidth || rect.left <= 0;
}