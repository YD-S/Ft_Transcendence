import {Game} from './game.js';
import {PageManager} from "./page-manager";

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
        this.WINNING_SCORE = 5;

        this.startGame();
    }

    startGame() {
        const currentMatch = this.matches[this.currentMatchIndex];

        if (currentMatch) {
            this.game = new Game();
            this.game.Team1_score = document.getElementById('score__p1');
            this.game.Team2_score = document.getElementById('score__p2');
            this.game.Team1_score.innerHTML = '0';
            this.game.Team2_score.innerHTML = '0';
            this.game.WINNING_SCORE = this.WINNING_SCORE;

            this.gameWatcher();
        } else {
            console.log("Tournament over! Final match has concluded.");
        }
    }

    gameWatcher() {
        const interval = setInterval(() => {
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
PageManager.getInstance().setOnPageLoad('pong/tournament', () => {
    game = new Tournament();
});

PageManager.getInstance().setOnPageUnload('pong/tournament', () => {
    if (game) {
        game.destroy();
        game = null;
    }
});
