
export const locale = {
    AUTH: {
        ERROR: {
            INVALID_CREDENTIALS: 'Nombre de usuario o contraseña no válidos',
            FAILED_OAUTH: 'Hubo un error con la solicitud de OAuth. Inténtelo de nuevo más tarde.',
            INVALID_OAUTH_CODE: 'Código OAuth no válido',
            INVALID_OAUTH_CALLBACK: 'Devolución de llamada de OAuth no válida',
            INVALID_2FA_CODE: 'Código no válido o caducado',
            RESEND_2FA_CODE: 'No se pudo reenviar el código',
            SEND_EMAIL: 'No se pudo enviar el correo electrónico',
            UPDATE_2FA: 'No se pudo actualizar la autenticación de dos factores',
            LOGOUT_FAILED: '¡No se pudo cerrar sesión!',
            REFRESH_FAILED: '¡No se pudo actualizar el token!',
            NO_2FA_CODE: 'No se proporcionó ningún código de verificación',
            NO_2FA_USER: 'Ningún usuario proporcionado',
        },
        TFA: {
            EMAIL_MESSAGE: 'Se ha enviado un código de verificación a su dirección de correo electrónico. Por favor ingrese el código a continuación.',
            EMAIL_RESENT_MESSAGE: 'Se ha enviado un nuevo código de verificación a su dirección de correo electrónico.',
            EMAIL_SENT_MESSAGE: 'Se ha enviado un correo electrónico de verificación a su dirección de correo electrónico.',
            UPDATE_SUCCESS: '¡Autenticación de dos factores actualizada!',
            EMAIL_VERIFIED: '¡Correo electrónico verificado!',
        },
    },
    USER: {
        ACTIONS: {
            INVITE: {
                SUCCESS: '¡Invitación enviada!',
                FAILED: '¡No se pudo enviar la invitación!',
            },
            FRIEND: {
                SUCCESS: '¡Usuario agregado a la lista de amigos!',
                FAILED: '¡No se pudo agregar el usuario a la lista de amigos!',
            },
            UNFRIEND: {
                SUCCESS: '¡Usuario eliminado de la lista de amigos!',
                FAILED: '¡No se pudo eliminar al usuario de la lista de amigos!',
            },
            BLOCK: {
                SUCCESS: '¡Usuario bloqueado!',
                FAILED: '¡No se pudo bloquear al usuario!',
            },
            UNBLOCK: {
                SUCCESS: '¡Usuario desbloqueado!',
                FAILED: '¡No se pudo desbloquear al usuario!',
            },
        },
        REGISTER: {
            SUCCESS: '¡Usuario registrado exitosamente!',
            FAILED: '¡No se pudo registrar el usuario!',
            PASSWORD_MISMATCH: '¡Las contraseñas no coinciden!',
        },
    },
    COMMON: {
        ERROR: {
            FETCH: {
                USER_DATA: '¡No se pudieron recuperar los datos del usuario!'
            },
            INVALID_ACTION: 'Acción no válida',
        },
    },
    CHAT: {
        ERROR: {
            CREATE_ROOM_FAILED: '¡No se pudo crear la sala!',
            JOIN_ROOM_FAILED: '¡No se pudo unir a la sala!',
            EMPTY_ROOM_CODE: 'El código de sala no puede estar vacío.',
            DIRECT_ROOM_FAILED: '¡No se pudo unir a la sala de mensajes directos!',
            LEAVE_ROOM_FAILED: '¡No pude salir de la sala!',
            EMPTY_USERNAME: '¡El nombre de usuario no puede estar vacío!',
            EMPTY_ROOM_NAME: '¡El nombre de la sala no puede estar vacío!',
            DM_WITH_SELF: '¡No puedo iniciar un mensaje directo a ti mismo!',
            BLOCKED_BY_USER: '¡Has sido bloqueado por este usuario!',
            BLOCKED_USER: '¡Has bloqueado a este usuario!',
            NOT_FRIENDS: '¡Debes ser amigos para enviar un mensaje directo!',
        },
    },
    GAME: {
        WINNER: 'Ganador',
        D2: {
            PLAYER1_WINS: '¡Jugador 1 gana!',
            PLAYER2_WINS: '¡Jugador 2 gana!',
            PLAYER1: 'Jugador 1',
            PLAYER2: 'Jugador 2',
            WINS: '¡gana!',
        },
        D3: {
        },
        TOURNAMENT: {
            ERROR: {
                PLAYER_EMPTY: 'Todos los nombres de los jugadores son obligatorios. Por favor complete todos los campos.',
                PLAYER_REPEAT: 'Cada jugador debe tener un nombre único. Asegúrese de que todos los nombres sean diferentes.',
            },
            WAITING_FOR_RESULTS: 'Esperando resultados',
        },
    },
}
