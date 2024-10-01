import {Game} from './game.js';
import {PageManager} from "./page-manager.js";

class Tournament {
    constructor() {
        this.players = ['Player 1', 'Player 2', 'Player 3', 'Player 4'];
        this.matches = [
            { player1: this.players[0], player2: this.players[1] },
            { player1: this.players[2], player2: this.players[3] },
            null
        ];
        this.currentMatchIndex = 0;
        this.results = [];
    }

    startGame() {
        const currentMatch = this.matches[this.currentMatchIndex];
                console.log("Starting game...");

        if (currentMatch) {
            PageManager.getInstance().loadToContainer('pong/game', document.getElementById('game-container'), false, {storeInHistory: false}).then(() => {
                this.game = window.game;
            });
            this.gameWatcher();
        } else {
            console.log("Tournament over! Final match has concluded.");
        }
    }

    gameWatcher() {
        const interval = setInterval(() => {
                    console.log("Game Watcher...");
            if (this.game.isGameOver()) {
                clearInterval(interval);

                const winner = this.game.getWinner();
                this.results.push(winner);

                if (this.currentMatchIndex === 1) {
                    this.matches[2] = { player1: this.results[0], player2: this.results[1] };  // Final match setup
                }

                this.currentMatchIndex++;
                if (this.currentMatchIndex < 3) {
                    this.startGame();
                } else {
                    this.endTournament();
                }
            }
        }, 100);
    }

    endTournament() {
        const finalWinner = this.results[2];
        console.log(`Tournament winner: ${finalWinner}`);
    }

    destroy() {
        if (this.game) {
            this.game.destroyed = true;
        }
    }
}

let game = null;
PageManager.getInstance().setOnPageLoad('tournament', () => {
    game = new Tournament();
    document.getElementById('button').addEventListener('click', (e) => {
        console.log("Starting tournament...");
        game.startGame();
        e.preventDefault();
    });
});

PageManager.getInstance().setOnPageUnload('pong/tournament', () => {
    if (game) {
        game.destroy();
        game = null;
    }
});
