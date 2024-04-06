export default class Paddle {
    constructor(PaddleElement, id, maxY, minY) {
        this.maxY = maxY;
        this.minY = minY;
        this.id = id;
        this.PaddleElement = PaddleElement;
        this.reset();
    }

    get position() {
        return parseFloat(getComputedStyle(this.PaddleElement).getPropertyValue('--pos'));
    }

    set position(value) {
        this.PaddleElement.style.setProperty('--pos', value);
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
        if(this.position < this.minY) this.position = this.minY;
        if(this.position > this.maxY) this.position = this.maxY;
    }

    reset() {
        this.position = window.innerHeight / 2;
    }
}