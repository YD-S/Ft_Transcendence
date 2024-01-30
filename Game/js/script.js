
import Ball from "./Ball.js";

const ball = new Ball(document.getElementById('ball'));

let lastTimestamp;
function update(timestamp) {
    if (lastTimestamp != null) {
        const delta = (timestamp - lastTimestamp);
        ball.update(delta);
    }
    lastTimestamp = timestamp;
    window.requestAnimationFrame(update);
}

window.requestAnimationFrame(update);