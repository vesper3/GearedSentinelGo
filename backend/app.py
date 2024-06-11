from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from database import db
from models import Game, Player
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///go_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/create_game', methods=['POST'])
def create_game():
    board_size = 19
    initial_board = [['' for _ in range(board_size)] for _ in range(board_size)]
    game = Game(board_state=json.dumps(initial_board))
    db.session.add(game)
    db.session.commit()
    return jsonify({'game_id': game.id})

@app.route('/join_game', methods=['POST'])
def join_game():
    data = request.json
    game_id = data['game_id']
    player_color = data['color']
    player = Player(game_id=game_id, color=player_color)
    db.session.add(player)
    db.session.commit()
    return jsonify({'player_id': player.id})

@socketio.on('join')
def on_join(data):
    room = data['game_id']
    join_room(room)
    emit('status', {'msg': 'Player has entered the game.'}, room=room)

@socketio.on('move')
def on_move(data):
    game_id = data['game_id']
    move = data['move']
    game = Game.query.get(game_id)
    board = json.loads(game.board_state)
    x, y, color = move
    board[x][y] = color
    game.board_state = json.dumps(board)
    db.session.commit()
    emit('move', {'move': move, 'board_state': board}, room=game_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)