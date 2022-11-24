import logging


class Config():
    logging_stream_level = logging.DEBUG
    logging_file_level = logging.DEBUG
    logging_level = min(logging_stream_level, logging_file_level)
    logging_file_path = 'logs\\'

    use_debug_auth = False
    
    lobby_hub_path = '/hubs/lobby'
    game_hub_path = '/hubs/game'
    login_path = '/api/v1/Identity/DebugAuth' if use_debug_auth else '/api/v1/Identity/Login'
    sign_auto_path = '/api/v1/Lobby/SignForAutoMatch'
