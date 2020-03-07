from copy import copy

class Colors:
    WHITE = "WHITE"; BLACK = "BLACK"
    EMPTY = "EMPTY"

def filter(match, coords: (int, int), moves: [(int, int)], color: Colors) -> [(int, int)]:
    valid = list()
    
    for move in moves: 
        temp = [ list([ copy(square) for square in row ]) for row in match.chessboard ]

        initial, final = match.find(coords), match.find(move)
        final.color, final.piece = initial.color, initial.piece

        initial.color = Colors.EMPTY
        initial.piece = None

        if match.check(match.turn) is False: valid.append(move)

        match.chessboard = temp

    return valid

def pawn(match, coords: (int, int), color: Colors, check: bool = True) -> [(int, int)]:
    moves = list()
    X, Y = coords

    if color is Colors.WHITE:
        if Y + 1 <= 7 and match.chessboard[Y + 1][X].color is Colors.EMPTY:
            move = (X, Y + 1)
            moves.append(move)

        if Y is 1 and match.chessboard[Y + 1][X].color is Colors.EMPTY and match.chessboard[Y + 2][X].color is Colors.EMPTY:
            move = (X, Y + 2)
            moves.append(move)
        
        if Y + 1 <= 7 and X + 1 <= 7 and match.chessboard[Y + 1][X + 1].color is not color and match.chessboard[Y + 1][X + 1].color is not Colors.EMPTY:
            move = (X + 1, Y + 1)
            moves.append(move)

        if Y + 1 <= 7 and X - 1 >= 0 and match.chessboard[Y + 1][X - 1].color is not color and match.chessboard[Y + 1][X - 1].color is not Colors.EMPTY:
            move = (X - 1, Y + 1)
            moves.append(move)

    if color is Colors.BLACK:
        if Y - 1 >= 0 and match.chessboard[Y - 1][X].color is Colors.EMPTY:
            move = (X, Y - 1)
            moves.append(move)

        if Y is 6 and match.chessboard[Y - 1][X].color is Colors.EMPTY and match.chessboard[Y - 2][X].color is Colors.EMPTY:
            move = (X, Y - 2)
            moves.append(move)
        
        if Y - 1 >= 0 and  X + 1 <= 7 and match.chessboard[Y - 1][X + 1].color is not color and match.chessboard[Y - 1][X + 1].color is not Colors.EMPTY:
            move = (X + 1, Y - 1)
            moves.append(move)

        if Y - 1 >= 0 and  X - 1 >= 0 and match.chessboard[Y - 1][X - 1].color is not color and match.chessboard[Y - 1][X - 1].color is not Colors.EMPTY:
            move = (X - 1, Y - 1)
            moves.append(move)
        
    if check is True: return filter(match, coords, moves, color)
    if check is False: return moves

def bishop(match, coords: (int, int), color: Colors, check: bool = True) -> [(int, int)]:
    moves = list()
    X, Y = coords

    for i in range(1, 8):
        if X + i <= 7 and Y + i <= 7:
            if match.chessboard[Y + i][X + i].color is color: break
            move = (X + i, Y + i)
            moves.append(move)
            if match.chessboard[Y + i][X + i].color is not Colors.EMPTY: break
        else: break
        
    for i in range(1, 8):
        if X - i >= 0 and Y - i >= 0:
            if match.chessboard[Y - i][X - i].color is color: break
            move = (X - i, Y - i)
            moves.append(move)
            if match.chessboard[Y - i][X - i].color is not Colors.EMPTY: break
        else: break
    
    for i in range(1, 8):
        if X + i <= 7 and Y - i >= 0:
            if match.chessboard[Y - i][X + i].color is color: break
            move = (X + i, Y - i)
            moves.append(move)
            if match.chessboard[Y - i][X + i].color is not Colors.EMPTY: break
        else: break

    for i in range(1, 8):
        if X - i >= 0 and Y + i <= 7:
            if match.chessboard[Y + i][X - i].color is color: break
            move = (X - i, Y + i)
            moves.append(move)
            if match.chessboard[Y + i][X - i].color is not Colors.EMPTY: break
        else: break

    if check is True: return filter(match, coords, moves, color)
    if check is False: return moves

def knight(match, coords: (int, int), color: Colors, check: bool = True) -> [(int, int)]:
    moves = list()
    X, Y = coords

    if X - 1 >= 0 and Y + 2 <= 7 and match.chessboard[Y + 2][X - 1].color is not color: moves.append((X - 1, Y + 2))
    if X + 1 <= 7 and Y + 2 <= 7 and match.chessboard[Y + 2][X + 1].color is not color: moves.append((X + 1, Y + 2))
    if X + 2 <= 7 and Y + 1 <= 7 and match.chessboard[Y + 1][X + 2].color is not color: moves.append((X + 2, Y + 1))
    if X + 2 <= 7 and Y - 1 >= 0 and match.chessboard[Y - 1][X + 2].color is not color: moves.append((X + 2, Y - 1))

    if X + 1 <= 7 and Y - 2 >= 0 and match.chessboard[Y - 2][X + 1].color is not color: moves.append((X + 1, Y - 2))
    if X - 1 >= 0 and Y - 2 >= 0 and match.chessboard[Y - 2][X - 1].color is not color: moves.append((X - 1, Y - 2))
    if X - 2 >= 0 and Y + 1 <= 7 and match.chessboard[Y + 1][X - 2].color is not color: moves.append((X - 2, Y + 1))
    if X - 2 >= 0 and Y - 1 >= 0 and match.chessboard[Y - 1][X - 2].color is not color: moves.append((X - 2, Y - 1))

    if check is True: return filter(match, coords, moves, color)
    if check is False: return moves

def rook(match, coords: (int, int), color: Colors, check: bool = True) -> [(int, int)]:
    moves = list()
    X, Y = coords

    for i in range(1, 8):
        if Y + i <= 7:
            if match.chessboard[Y + i][X].color is color: break
            move = (X, Y + i)
            moves.append(move)
            if match.chessboard[Y + i][X].color is not Colors.EMPTY: break
        else: break

    for i in range(1, 8):
        if Y - i >= 0:
            if match.chessboard[Y - i][X].color is color: break
            move = (X, Y - i)
            moves.append(move)
            if match.chessboard[Y - i][X].color is not Colors.EMPTY: break
        else: break

    for i in range(1, 8):
        if X + i <= 7:
            if match.chessboard[Y][X + i].color is color: break
            move = (X + i, Y)
            moves.append(move)
            if match.chessboard[Y][X + i].color is not Colors.EMPTY: break
        else: break

    for i in range(1, 8):
        if X - i >= 0:
            if match.chessboard[Y][X - i].color is color: break
            move = (X - i, Y)
            moves.append(move)
            if match.chessboard[Y][X - i].color is not Colors.EMPTY: break
        else: break

    if check is True: return filter(match, coords, moves, color)
    if check is False: return moves

def queen(match, coords: (int, int), color: Colors, check: bool = True) -> [(int, int)]:
    moves = list()

    lateral = bishop(match, coords, color, check = check); moves.extend(lateral)
    vertical = rook(match, coords, color, check = check); moves.extend(vertical)

    if check is True: return filter(match, coords, moves, color)
    if check is False: return moves

def king(match, coords: (int, int), color: Colors, check: bool = True) -> [(int, int)]:
    moves = list()
    X, Y = coords

    if X + 1 <= 7 and Y + 1 <= 7 and match.chessboard[Y + 1][X + 1].color is not color: moves.append((X + 1, Y + 1))
    if X - 1 >= 0 and Y - 1 >= 0 and match.chessboard[Y - 1][X - 1].color is not color: moves.append((X - 1, Y - 1))
    if X + 1 <= 7 and Y - 1 >= 0 and match.chessboard[Y - 1][X + 1].color is not color: moves.append((X + 1, Y - 1))
    if X - 1 >= 0 and Y + 1 <= 7 and match.chessboard[Y + 1][X - 1].color is not color: moves.append((X - 1, Y + 1))

    if X + 1 <= 7 and match.chessboard[Y][X + 1].color is not color: moves.append((X + 1, Y))
    if X - 1 >= 0 and match.chessboard[Y][X - 1].color is not color: moves.append((X - 1, Y))
    if Y + 1 <= 7 and match.chessboard[Y + 1][X].color is not color: moves.append((X, Y + 1))
    if Y - 1 >= 0 and match.chessboard[Y - 1][X].color is not color: moves.append((X, Y - 1))

    if check is True: return filter(match, coords, moves, color)
    if check is False: return moves

class Pieces:
    PAWN = pawn
    BISHOP = bishop; KNIGHT = knight
    ROOK = rook
    QUEEN = queen; KING = king

class Square:
    def __init__(self, color: Colors, piece: Pieces = None):
        self.color = color
        self.piece = piece

class Match:
    layout = [
        [ Square(Colors.WHITE, Pieces.ROOK), Square(Colors.WHITE, Pieces.KNIGHT), Square(Colors.WHITE, Pieces.BISHOP), Square(Colors.WHITE, Pieces.QUEEN), Square(Colors.WHITE, Pieces.KING), Square(Colors.WHITE, Pieces.BISHOP), Square(Colors.WHITE, Pieces.KNIGHT), Square(Colors.WHITE, Pieces.ROOK) ],
        [ Square(Colors.WHITE, Pieces.PAWN), Square(Colors.WHITE, Pieces.PAWN), Square(Colors.WHITE, Pieces.PAWN), Square(Colors.WHITE, Pieces.PAWN), Square(Colors.WHITE, Pieces.PAWN), Square(Colors.WHITE, Pieces.PAWN), Square(Colors.WHITE, Pieces.PAWN), Square(Colors.WHITE, Pieces.PAWN) ],
        [ Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY) ],
        [ Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY) ],
        [ Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY) ],
        [ Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY), Square(Colors.EMPTY) ],
        [ Square(Colors.BLACK, Pieces.PAWN), Square(Colors.BLACK, Pieces.PAWN), Square(Colors.BLACK, Pieces.PAWN), Square(Colors.BLACK, Pieces.PAWN), Square(Colors.BLACK, Pieces.PAWN), Square(Colors.BLACK, Pieces.PAWN), Square(Colors.BLACK, Pieces.PAWN), Square(Colors.BLACK, Pieces.PAWN) ],
        [ Square(Colors.BLACK, Pieces.ROOK), Square(Colors.BLACK, Pieces.KNIGHT), Square(Colors.BLACK, Pieces.BISHOP), Square(Colors.BLACK, Pieces.QUEEN), Square(Colors.BLACK, Pieces.KING), Square(Colors.BLACK, Pieces.BISHOP), Square(Colors.BLACK, Pieces.KNIGHT), Square(Colors.BLACK, Pieces.ROOK) ]
    ]

    def __init__(self):
        self.chessboard = [ list([ copy(square) for square in row ]) for row in Match.layout ]
        self.turn = Colors.WHITE
        self.finished = False
        
    def move(self, initial: str, final: str) -> bool:
        if self.finished is not False: raise Exception("The match is finished, impossible to move")

        initial, final = Match.decode(initial), Match.decode(final)
        initial = { "COORDS": initial, "SQUARE": self.find(initial) }
        final = { "COORDS": final, "SQUARE": self.find(final) }

        if initial["SQUARE"].color is not self.turn: raise Exception("None of your pieces are present in the initial square")

        if self.validate(initial, final):
            initial, final = initial["COORDS"], final["COORDS"]

            self.chessboard[final[1]][final[0]].color = self.chessboard[initial[1]][initial[0]].color
            self.chessboard[final[1]][final[0]].piece = self.chessboard[initial[1]][initial[0]].piece
            self.chessboard[initial[1]][initial[0]] = Square(Colors.EMPTY)

            self.turn = (Colors.WHITE, Colors.BLACK)[self.turn is Colors.WHITE]

            moves = self.possible(self.turn, check = True)
            
            if len(moves) is 0: 
                self.finished = True

            return self.finished
        else: raise Exception("Illegal move for the selected piece")

    def validate(self, initial, final) -> bool:
        moves = initial["SQUARE"].piece(self, initial["COORDS"], initial["SQUARE"].color, check = True)

        try: moves.index(final["COORDS"]); return True
        except: return False

    def check(self, color: Colors) -> bool:
        X, Y = int(), int()

        for y, row in enumerate(self.chessboard): 
            for x, square in enumerate(row): 
                if square.color is color and square.piece is Pieces.KING:
                     X, Y = x, y

        moves = self.possible((Colors.WHITE, Colors.BLACK)[color is Colors.WHITE], check = False)
        
        try: moves.index((X, Y)); return True
        except: return False

    def possible(self, color: Colors, check: bool = True) -> [(int, int)]:
        moves = list()

        for y, row in enumerate(self.chessboard):
            for x, square in enumerate(row):
                coords = (x, y)

                if square.color is color:
                    array = square.piece(self, coords, square.color, check = check)
                    moves.extend(array)

        return moves

    def find(self, coords: (int, int)) -> Square:
        X, Y = coords
        square = self.chessboard[Y][X]
        return square

    @staticmethod
    def decode(string : str) -> (int, int):
        exception = Exception("Invalid move format: <Letter from A to H> + <Number from 1 to 8>")

        if len(string) is not 2: raise exception

        letter, number = tuple(string.upper())

        try:
            letters = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
            numbers = [ '1', '2', '3', '4', '5', '6', '7', '8' ]
            result = (letters.index(letter), numbers.index(number))
        except: raise exception

        return result
