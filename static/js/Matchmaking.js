export default class Matchmaking {
    constructor() {
        this.Matchmakingsocket = new WebSocket(`wss://${window.location.host}/ws/matchmaking/`);
        this.room_id = null;
        this.amIfirst = null;
        this.GameSocket = null;
        this.playerId = null;

        this.Matchmakingsocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "game_start") {
                this.amIfirst = data.player;
                this.room_id = data.room_id;
                this.playerId = data.playerId;
                this.opponentId = data.opponentId;
                console.log(this.playerId, this.opponentId, this.amIfirst)
            } else if (data.type === "redirect") {
                this.Matchmakingsocket.close(4242);
            }
        };

        this.Matchmakingsocket.onclose = (event) => {
            console.log(event.code);
            if (event.code === 4242) {
                console.log("Matchmaking socket closed");
                this.initializeGameSocket().then((gameSocket) => {
                    this.GameSocket = gameSocket;
                    this.onGameSocketReady();
                }).catch((error) => {
                    console.error("Failed to initialize game socket: ", error);
                });
            }
        };
    }

    initializeGameSocket() {
        return new Promise((resolve, reject) => {
            const gameSocket = new WebSocket(`wss://${window.location.host}/ws/game/${this.room_id}/`);

            gameSocket.onopen = () => {
                console.log("Game socket connection established");
                resolve(gameSocket);
            };

            gameSocket.onerror = (error) => {
                console.error("Game socket error: ", error);
                reject(error);
            };
        });
    }

    onGameSocketReady() {
        // This method should be overwritten by the consumer to handle when the game socket is ready
    }
}
