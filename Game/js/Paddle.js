export default class Paddle {
    constructor(PaddleElement) {
        this.PaddleElement = PaddleElement;
        this.reset();
    }

    get position() {
        return parseFloat(getComputedStyle(this.PaddleElement).getPropertyValue('--pos'));
    }

    set position(value) {
        this.PaddleElement.style.setProperty('--pos', value);
    }

    rect() {
        return this.PaddleElement.getBoundingClientRect();
    }

    reset() {
        this.position = 50;
    }
}