import {Game} from './game.js';
import {PageManager} from "./page-manager.js";

class Tournament {
    constructor() {
        this.players = [];
        this.matches = [];
        this.currentMatchIndex = 0;
        this.results = [];
    }

    startGame() {
        const currentMatch = this.matches[this.currentMatchIndex];
        if (currentMatch) {
            PageManager.getInstance().loadToContainer('pong/game', document.getElementById('game-container'), false, {storeInHistory: false}).then(() => {
                this.game = window.game;
            });
            this.gameWatcher();
        } else {
            PageManager.getInstance().loadToContainer('ui/matches', document.getElementById('game-container'), false, {storeInHistory: false}).then(() => {
                document.getElementById('match1').innerText = `${this.matches[0].player1} vs ${this.matches[0].player2} Winner: ${this.results[0]}`;
                document.getElementById('match2').innerText = `${this.matches[1].player1} vs ${this.matches[1].player2} Winner: ${this.results[1]}`;
                document.getElementById('match3').innerText = `${this.results[0]} vs ${this.results[1]} Winner: ${this.results[2]}`;
            });
        }
    }

    gameWatcher() {
        const interval = setInterval(() => {
            if (this.game.isGameOver()) {
                clearInterval(interval);

                const winner = this.game.getWinner();
                if (winner === this.matches[this.currentMatchIndex].player1) {
                    this.results.push(this.matches[this.currentMatchIndex].player1);
                } else {
                    this.results.push(this.matches[this.currentMatchIndex].player2);
                }
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
        }, 250);
    }

    showMatchesPage() {
        const match1 = this.results[0];
        const match2 = this.results[1];
        const finalMatch = this.results[2];
        PageManager.getInstance().loadToContainer('ui/matches', document.getElementById('game-container'), false, {storeInHistory: false}).then(() => {
            if (match1 !== undefined) {
                document.getElementById('match1').innerHTML = `${this.matches[0].player1} vs ${this.matches[0].player2} <p>Winner: ${match1}</p>`;
                document.getElementById('match1').setAttribute('id', 'finished');
            }
            else
                document.getElementById('match1').innerText = `${this.matches[0].player1} vs ${this.matches[0].player2}`;
            if (match2 !== undefined) {
                document.getElementById('match2').innerHTML = `${this.matches[1].player1} vs ${this.matches[1].player2} <p>Winner: ${match2}</p>`;
                document.getElementById('match2').setAttribute('id', 'finished');
            }
            else
                document.getElementById('match2').innerText = `${this.matches[1].player1} vs ${this.matches[1].player2}`;
            if (finalMatch !== undefined) {
                document.getElementById('match3').innerHTML = `${match1} vs ${match2} <p>Winner: ${finalMatch}</p>`;
                document.getElementById('match3').setAttribute('id', 'finished');
            }
            else
                document.getElementById('match3').innerText = `Waiting for results`;
        });
    }

    endTournament() {
        const finalWinner = this.results[2];
        this.showMatchesPage();
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
    document.getElementById('button').addEventListener('click', (e) => {
        const player1 = document.getElementById('player1').value;
        const player2 = document.getElementById('player2').value;
        const player3 = document.getElementById('player3').value;
        const player4 = document.getElementById('player4').value;
        game.players = [player1, player2, player3, player4];
        game.matches =[
            { player1: game.players[0], player2: game.players[1] },
            { player1: game.players[2], player2: game.players[3] },
            null
        ];
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
