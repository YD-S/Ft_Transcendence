let vel_global = 0.025;
let Vel_multiplier = 0.000001;

export default class Ball {
    constructor(ballElem) {
        this.ballElem = ballElem
        this.reset();
    }

    get x() {
        return parseFloat(getComputedStyle(this.ballElem).getPropertyValue('--pos-x'));
    }

    set x(value) {
        this.ballElem.style.setProperty('--pos-x', value);
    }

    get y() {
        return parseFloat(getComputedStyle(this.ballElem).getPropertyValue('--pos-y'));
    }

    set y(value) {
        this.ballElem.style.setProperty('--pos-y', value);
    }

    reset() {
        this.x = 50;
        this.y = 50;
        this.direction = {x: 0};
        while (
            Math.abs(this.direction.x) <= 0.2 ||
            Math.abs(this.direction.x) >= 0.9
            ) {
            const angle = CustomRandomNum(0, 2 * Math.PI);
            this.direction = {x: Math.cos(angle), y: Math.sin(angle)};
        }
        this.velocity = vel_global;
    }

    rect() {
        return this.ballElem.getBoundingClientRect();
    }

    update(delta, paddleRect) {
        this.x = this.x + this.direction.x * this.velocity * delta;
        this.y = this.y + this.direction.y * this.velocity * delta;
        this.velocity += Vel_multiplier * delta;
        const rect = this.rect();

        if(rect.top <= 0 || rect.bottom >= window.innerHeight) {
            this.direction.y = -this.direction.y;
        }

        if(paddleRect.some(r => isColliding(r, rect))) {
            this.direction.x = -this.direction.x;
        }
    }
}

function CustomRandomNum(min, max) {
    return Math.random() * (max - min) + min;
}

function isColliding(r1, r2) {
    return (
        r1.left <= r2.right &&
        r1.right >= r2.left &&
        r1.top <= r2.bottom &&
        r1.bottom >= r2.top
        );
}