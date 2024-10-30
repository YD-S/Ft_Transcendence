
export const locale = {
    AUTH: {
        ERROR: {
            INVALID_CREDENTIALS: 'Nome de usuário ou senha inválidos',
            FAILED_OAUTH: 'Ocorreu um erro com a solicitação do OAuth. Por favor, tente novamente mais tarde.',
            INVALID_OAUTH_CODE: 'Código OAuth inválido',
            INVALID_OAUTH_CALLBACK: 'Retorno de chamada OAuth inválido',
            INVALID_2FA_CODE: 'Código inválido ou expirado',
            RESEND_2FA_CODE: 'Não foi possível reenviar o código',
            SEND_EMAIL: 'Não foi possível enviar e-mail',
            UPDATE_2FA: 'Falha ao atualizar a autenticação de dois fatores',
            LOGOUT_FAILED: 'Não foi possível sair!',
            REFRESH_FAILED: 'Falha ao atualizar o token!',
            NO_2FA_CODE: 'Nenhum código de verificação fornecido',
            NO_2FA_USER: 'Nenhum usuário fornecido',
        },
        TFA: {
            EMAIL_MESSAGE: 'Um código de verificação foi enviado para seu endereço de e-mail. Por favor insira o código abaixo.',
            EMAIL_RESENT_MESSAGE: 'Um novo código de verificação foi enviado para seu endereço de e-mail.',
            EMAIL_SENT_MESSAGE: 'Um e-mail de verificação foi enviado para o seu endereço de e-mail.',
            UPDATE_SUCCESS: 'Autenticação de dois fatores atualizada!',
            EMAIL_VERIFIED: 'E-mail verificado!',
        },
    },
    USER: {
        ACTIONS: {
            INVITE: {
                SUCCESS: 'Convite enviado!',
                FAILED: 'Não foi possível enviar o convite!',
            },
            FRIEND: {
                SUCCESS: 'Usuário adicionado à lista de amigos!',
                FAILED: 'Não foi possível adicionar o usuário à lista de amigos!',
            },
            UNFRIEND: {
                SUCCESS: 'Usuário removido da lista de amigos!',
                FAILED: 'Não foi possível remover o usuário da lista de amigos!',
            },
            BLOCK: {
                SUCCESS: 'Usuário bloqueado!',
                FAILED: 'Não foi possível bloquear o usuário!',
            },
            UNBLOCK: {
                SUCCESS: 'Usuário desbloqueado!',
                FAILED: 'Não foi possível desbloquear o usuário!',
            },
        },
        REGISTER: {
            SUCCESS: 'Usuário cadastrado com sucesso!',
            FAILED: 'Falha ao registrar usuário!',
            PASSWORD_MISMATCH: 'As senhas não coincidem!',
        },
    },
    COMMON: {
        ERROR: {
            FETCH: {
                USER_DATA: 'Não foi possível recuperar os dados do usuário!'
            },
            INVALID_ACTION: 'Ação inválida',
        },
    },
    CHAT: {
        ERROR: {
            CREATE_ROOM_FAILED: 'Não foi possível criar Quarto!',
            JOIN_ROOM_FAILED: 'Não foi possível entrar na Quarto!',
            EMPTY_ROOM_CODE: 'O código do quarto não pode ficar vazio.',
            DIRECT_ROOM_FAILED: 'Não foi possível entrar na Quarto de mensagens diretas!',
            LEAVE_ROOM_FAILED: 'Eu não conseguia sair da Quarto!',
            EMPTY_USERNAME: 'O nome de usuário não pode ficar vazio!',
            EMPTY_ROOM_NAME: 'O nome da sala não pode ficar vazio!',
            DM_WITH_SELF: 'Não consigo iniciar uma mensagem direta para você!',
            BLOCKED_BY_USER: 'Você foi bloqueado por este usuário!',
            BLOCKED_USER: 'Você bloqueou este usuário!',
            NOT_FRIENDS: 'Você deve ser amigo para enviar uma mensagem direta!',
        },
    },
    GAME: {
        WINNER: 'Ganhador',
        D2: {
            PLAYER1_WINS: 'Jogador 1 vence!',
            PLAYER2_WINS: 'Jogador 2 vence!',
            PLAYER1: 'Jogador 1',
            PLAYER2: 'Jogador 2',
            WINS: 'ganhar!',
        },
        D3: {
        },
        TOURNAMENT: {
            ERROR: {
                PLAYER_EMPTY: 'Todos os nomes de jogadores são obrigatórios. Por favor preencha todos os campos.',
                PLAYER_REPEAT: 'Cada jogador deve ter um nome exclusivo. Certifique-se de que todos os nomes sejam diferentes.',
            },
            WAITING_FOR_RESULTS: 'Aguardando resultados',
        },
    },
}
