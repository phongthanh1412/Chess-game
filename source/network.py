import json

def encode_move(move, en_passant=None):
    return (json.dumps({
        'type': 'move',
        'start': [move.initial.row, move.initial.col],
        'end': [move.final.row, move.final.col],
        'en_passant': list(en_passant) if en_passant else None
    }) + '\n').encode()

def encode_control(action, winner=None, game_result=None):
    return (json.dumps({
        'type': 'control',
        'action': action,
        'winner': winner,
        'game_result': game_result
    }) + '\n').encode()

def decode_message(data):
    return json.loads(data.decode())
