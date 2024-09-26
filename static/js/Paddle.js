export default class Paddle {
    constructor(PaddleElement, id) {
        this.id = id;
        this.PaddleElement = PaddleElement;
        this.reset();
    }

    get position() {
        return parseFloat(getComputedStyle(this.PaddleElement).getPropertyValue('--pos'));
    }

    set position(value) {
        this.PaddleElement.style.setProperty('--pos', Math.min(Math.max(value, 0), 100));
    }

    get heightPaddle() {
        return parseFloat(getComputedStyle(this.PaddleElement).getPropertyValue(`--paddle${this.id}_height`));
    }

    set heightPaddle(value) {
        this.PaddleElement.style.setProperty(`--paddle${this.id}_height`, value);
    }

    rect() {
        return this.PaddleElement.getBoundingClientRect();
    }

    update() {
        const paddleHeightVH = this.heightPaddle / window.innerHeight * 500;

        if (this.position < 0 + paddleHeightVH) {
            this.position = 0 + paddleHeightVH;
        } else if (this.position > 100 - paddleHeightVH) {
            this.position = 100 - paddleHeightVH;
        }
    }

    reset() {
        this.position = 50;
    }
}