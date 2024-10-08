import * as THREE from "three";

const GAME_WIDTH = 1000;
const GAME_HEIGHT = height_aspect_ratio(GAME_WIDTH);
export const PAD_H = GAME_HEIGHT / 1000;
export const PAD_W = GAME_WIDTH / 350;
const RADIUS = 15;
const BALL_SIZE = GAME_WIDTH / 1500;

export function height_aspect_ratio(width) {
    return (width / 16) * 9;
}

export function makeCamera() {
    return new THREE.PerspectiveCamera(55, GAME_WIDTH / GAME_HEIGHT, 0.1, 1000);
}

export function makePaddle(color) {
        const shape = new THREE.Shape();
        const radius = 0.2; // adjust the radius as needed
        shape.moveTo(-PAD_W / 2 + radius, -PAD_H / 2);
        shape.lineTo(PAD_W / 2 - radius, -PAD_H / 2);
        shape.quadraticCurveTo(PAD_W / 2, -PAD_H / 2, PAD_W / 2, -PAD_H / 2 + radius);
        shape.lineTo(PAD_W / 2, PAD_H / 2 - radius);
        shape.quadraticCurveTo(PAD_W / 2, PAD_H / 2, PAD_W / 2 - radius, PAD_H / 2);
        shape.lineTo(-PAD_W / 2 + radius, PAD_H / 2);
        shape.quadraticCurveTo(-PAD_W / 2, PAD_H / 2, -PAD_W / 2, PAD_H / 2 - radius);
        shape.lineTo(-PAD_W / 2, -PAD_H / 2 + radius);
        shape.quadraticCurveTo(-PAD_W / 2, -PAD_H / 2, -PAD_W / 2 + radius, -PAD_H / 2);

        const extrudeSettings = {
            depth: 1,
            bevelEnabled: true
        };
        const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
        const neonMaterial = new THREE.MeshPhongMaterial({
          color: color,    // Base color (green neon)
          emissive: color, // Emissive color (this creates the glowing effect)
          emissiveIntensity: 1.5, // How much it emits light
          shininess: 100, // High shininess for a glossy look
        });
        return new THREE.Mesh(geometry, neonMaterial);
}

export function makeBall(color) {
    const geometry = new THREE.SphereGeometry(BALL_SIZE, 32, 32);
    const material = new THREE.MeshBasicMaterial({color: color});
    return new THREE.Mesh(geometry, material);
}

export function makeGrid() {
    const radius = RADIUS;
    const sectors = 16;
    const rings = 8;
    const divisions = 64;

    return new THREE.PolarGridHelper(radius, sectors, rings, divisions);
}