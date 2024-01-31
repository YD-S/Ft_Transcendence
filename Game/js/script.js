
import Ball from "./Ball.js";
import Paddle from "./Paddle.js";

const ball = new Ball(document.getElementById('ball'));
const paddle1 = new Paddle(document.getElementById('player1_paddle'));
const paddle2 = new Paddle(document.getElementById('player2_paddle'));

let lastTimestamp;
function update(timestamp) {
    if (lastTimestamp != null) {
        const delta = (timestamp - lastTimestamp);
        ball.update(delta, [paddle1.rect(), paddle2.rect()]);
    }
    lastTimestamp = timestamp;
    window.requestAnimationFrame(update);
}

document.addEventListener('keydown', event => {
    console.log(event.key);
    switch (event.key) {
        case 'w':
            paddle1.position -= 5;
            break;
        case 's':
            paddle1.position += 5;
            break;
        case 'ArrowUp':
            paddle2.position -= 5;
            break;
        case 'ArrowDown':
            paddle2.position += 5;
            break;
    }
});

window.requestAnimationFrame(update);