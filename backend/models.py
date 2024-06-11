from database import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.Text, nullable=False, default= 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    turn = db.Column(db.String(10), nullable=False, default='black')
    winner = db.Column(db.String(10), nullable=True, default=None)
    moves = db.Column(db.Text, nullable=False, default='')

    def make_move(self, move):
        # Simplified example: Append move to board state
        self.board_state += move
        db.session.commit()

    def render_board(self):
        """Decodes the board state and returns a 2D list representation."""
        board_size = 19  # Assuming a standard 19x19 Go board
        board = [['E' for _ in range(board_size)] for _ in range(board_size)]  # Initialize with empty cells

        # Decode the board state string
        for i, char in enumerate(self.board_state):
            row = i // board_size
            col = i % board_size
            board[row][col] = char

        return board
    

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    game = db.relationship('Game', backref=db.backref('players', lazy=True))




   

        

    