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

    get heightPaddle1() {
        return parseFloat(getComputedStyle(this.PaddleElement).getPropertyValue('--paddle1_height'));
    }

    set heightPaddle1(value) {
        this.PaddleElement.style.setProperty('--paddle1_height', value);
    }

    get heightPaddle2() {
        return parseFloat(getComputedStyle(this.PaddleElement).getPropertyValue('--paddle2_height'));
    }

    set heightPaddle2(value) {
        this.PaddleElement.style.setProperty('--paddle2_height', value);
    }

    rect() {
        return this.PaddleElement.getBoundingClientRect();
    }

    update() {
        if(this.position < 0) this.position = 0;
        if(this.position > 100) this.position = 100;
    }

    reset() {
        this.position = 50;
    }
}