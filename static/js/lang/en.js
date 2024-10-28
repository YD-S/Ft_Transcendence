
export const locale = {
    AUTH: {
        ERROR: {
            INVALID_CREDENTIALS: 'Invalid username or password',
            FAILED_OAUTH: 'There was an error with the OAuth request. Please try again later.',
            INVALID_OAUTH_CODE: 'Invalid OAuth code',
            INVALID_OAUTH_CALLBACK: 'Invalid OAuth callback',
            INVALID_2FA_CODE: 'Invalid or expired code',
            RESEND_2FA_CODE: 'Failed to resend code',
            SEND_EMAIL: 'Failed to send email',
            UPDATE_2FA: 'Failed to update two-factor authentication',
            LOGOUT_FAILED: 'Failed to logout!',
            REFRESH_FAILED: 'Failed to refresh token!',
            NO_2FA_CODE: 'No verification code provided',
            NO_2FA_USER: 'No user provided',
        },
        TFA: {
            EMAIL_MESSAGE: 'A verification code has been sent to your email address. Please enter the code below.',
            EMAIL_RESENT_MESSAGE: 'A new verification code has been sent to your email address.',
            EMAIL_SENT_MESSAGE: 'A verification email has been sent to your email address.',
            UPDATE_SUCCESS: 'Two-factor authentication updated!',
            EMAIL_VERIFIED: 'Email verified!',
        },
    },
    USER: {
        ACTIONS: {
            INVITE: {
                SUCCESS: 'Invitation sent!',
                FAILED: 'Failed to send invitation!',
            },
            FRIEND: {
                SUCCESS: 'Added user to friend list!',
                FAILED: 'Failed to add user to friend list!',
            },
            UNFRIEND: {
                SUCCESS: 'Removed user from friend list!',
                FAILED: 'Failed to remove user from friend list!',
            },
            BLOCK: {
                SUCCESS: 'User blocked!',
                FAILED: 'Failed to block user!',
            },
            UNBLOCK: {
                SUCCESS: 'User unblocked!',
                FAILED: 'Failed to unblock user!',
            },
        },
        REGISTER: {
            SUCCESS: 'User registered successfully!',
            FAILED: 'Failed to register user!',
            PASSWORD_MISMATCH: 'Passwords do not match!',
        },
    },
    COMMON: {
        ERROR: {
            FETCH: {
                USER_DATA: 'Failed to fetch user data!'
            },
            INVALID_ACTION: 'Invalid action',
        },
    },
    CHAT: {
        ERROR: {
            CREATE_ROOM_FAILED: 'Failed to create room!',
            JOIN_ROOM_FAILED: 'Failed to join room!',
            EMPTY_ROOM_CODE: 'Room code cannot be empty',
            DIRECT_ROOM_FAILED: 'Failed to join direct message room!',
            LEAVE_ROOM_FAILED: 'Failed to leave room!',
            EMPTY_USERNAME: 'Username cannot be empty!',
            EMPTY_ROOM_NAME: 'Room name cannot be empty!',
            DM_WITH_SELF: 'Can\'t initiate a direct message to yourself!',
            BLOCKED_BY_USER: 'You have been blocked by this user!',
            BLOCKED_USER: 'You have blocked this user!',
            NOT_FRIENDS: 'You must be friends to send a direct message!',
        },
    },
    GAME: {
        WINNER: 'Winner',
        D2: {
            PLAYER1_WINS: 'Player 1 wins!',
            PLAYER2_WINS: 'Player 2 wins!',
            PLAYER1: 'Player 1',
            PLAYER2: 'Player 2',
            WINS: 'wins!',
        },
        D3: {
        },
        TOURNAMENT: {
            ERROR: {
                PLAYER_EMPTY: 'All player names are required. Please fill in all fields.',
                PLAYER_REPEAT: 'Each player must have a unique name. Please ensure all names are different.',
            },
            WAITING_FOR_RESULTS: 'Waiting for results',
        },
    },
}