import { Game } from './game.js';
import { PageManager } from "./page-manager.js";
import {Notification} from "./notification.js";
import {t} from "./translation.js";

class Tournament {
    constructor() {
        this.results = [];
        this.tournamentSocket = new WebSocket(`wss://${window.location.host}/ws/tournament/`);
    }

    initializeTournament() {
        this.showMatchesPage();
    }

    showMatchesPage() {
        PageManager.getInstance().loadToContainer('ui/matches', document.getElementById('game-container'), false, { storeInHistory: false }).then(() => {
            this.updateMatchDisplay();
            this.addDeployMatchListeners();
        });
    }

    updateMatchDisplay() {
        for (let i = 0; i < 3; i++) {
            const matchElement = document.getElementById(`match${i + 1}`);
            const match = this.matches[i];

            if (match.played) {
                matchElement.innerHTML = `<button class="button">${match.player1} vs ${match.player2} <p>${t('GAME.WINNER')}: ${this.results[i]}</p> </button>`;
                matchElement.setAttribute('id', 'finished');
            } else if (match.player1 && match.player2) {
                matchElement.innerHTML = `<button class="deploy-match button" data-match="${i}">${match.player1} vs ${match.player2}</button>`;
            } else {
                matchElement.innerHTML = `<button class="button waiting">${t('GAME.TOURNAMENT.WAITING_FOR_RESULTS')}</button>`;
            }
        }
    }

    addDeployMatchListeners() {
        const deployLinks = document.querySelectorAll('.deploy-match');
        deployLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const matchIndex = parseInt(e.target.getAttribute('data-match'));
                this.startGame(matchIndex);
            });
        });
    }

    startGame(matchIndex) {
        const currentMatch = this.matches[matchIndex];
        if (currentMatch && !currentMatch.played) {
            PageManager.getInstance().loadToContainer('pong/game', document.getElementById('game-container'), false, { storeInHistory: false }).then(() => {
                this.game = window.game;
                this.game.tournament = true;
                this.gameWatcher(matchIndex);
            });
        }
    }

    gameWatcher(matchIndex) {
        const handleGameEnd = (event) => {
            let winner = event.detail.winner;
            if (winner === 'Player 1') {
                winner = this.matches[matchIndex].player1;
            }
            if (winner === 'Player 2') {
                winner = this.matches[matchIndex].player2;
            }
            this.results[matchIndex] = winner;
            this.matches[matchIndex].played = true;

            if (matchIndex === 0 || matchIndex === 1) {
                if (this.matches[0].played && this.matches[1].played) {
                    this.matches[2] = { player1: this.results[0], player2: this.results[1], played: false };
                }
            }

            window.removeEventListener('gameEnd', handleGameEnd);

            if (this.matches[2].played) {
                this.endTournament();
            } else {
                this.showMatchesPage();
            }
        };

        window.addEventListener('gameEnd', handleGameEnd);
    }

    validateForm() {
        const player1 = document.getElementById('player1').value.trim();
        const player2 = document.getElementById('player2').value.trim();
        const player3 = document.getElementById('player3').value.trim();
        const player4 = document.getElementById('player4').value.trim();

        if (!player1 || !player2 || !player3 || !player4) {
            Notification.warning("GAME.TOURNAMENT.ERROR.PLAYER_EMPTY");
            return false;
        }

        const playerNames = [player1, player2, player3, player4];
        const uniqueNames = new Set(playerNames);
        if (uniqueNames.size !== playerNames.length) {
            Notification.warning("GAME.TOURNAMENT.ERROR.PLAYER_REPEAT");
            return false;
        }

        return true;
    }

    endTournament() {
        this.showMatchesPage();
        this.tournamentSocket.send(JSON.stringify({
            'player1': this.matches[0].player1,
            'player2': this.matches[0].player2,
            'player3': this.matches[1].player1,
            'player4': this.matches[1].player2,
            'semi_winner_1': this.results[0],
            'semi_winner_2': this.results[1],
            'final_winner': this.results[2]
        }));
    }

    destroy() {
        if (this.game) {
            this.game.destroyed = true;
        }
    }
}

let tournament = null;
PageManager.getInstance().setOnPageLoad('pong/tournament', () => {
    document.getElementById('button').addEventListener('click', (e) => {
        const tournamentInstance = new Tournament();
        if (tournamentInstance.validateForm()) {
            const player1 = document.getElementById('player1').value.trim();
            const player2 = document.getElementById('player2').value.trim();
            const player3 = document.getElementById('player3').value.trim();
            const player4 = document.getElementById('player4').value.trim();

            tournament = tournamentInstance;
            tournament.matches = [
                {player1: player1, player2: player2, played: false},
                {player1: player3, player2: player4, played: false},
                {player1: null, player2: null, played: false}
            ];
            tournament.initializeTournament();
        }
    });
});

PageManager.getInstance().setOnPageUnload('pong/tournament', () => {
    if (tournament) {
        tournament.destroy();
        tournament = null;
    }
});