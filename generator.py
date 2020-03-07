from chess import Square, Colors, Pieces
from PIL import Image
from typing import Union

class Generator:
    X = [ 25, 109, 194, 279, 363, 448, 531, 616 ]
    Y = [ 616, 531, 448, 363, 279, 194, 109, 25 ]

    @staticmethod
    def generate(layout) -> Image:
        chessboard = Image.open("resources/chessboard.png")

        for y, Y in enumerate(Generator.Y):
            for x, X in enumerate(Generator.X):
                path = Generator.path(layout[y][x])
                if path is None: continue

                piece = Image.open(path).convert("RGBA")
                chessboard.paste(piece, (X, Y), piece)

        return chessboard

    @staticmethod
    def path(square: Square) -> Union[str, None]:
        path = "resources/"

        if square.color is Colors.EMPTY: return None

        if square.color is Colors.WHITE: path += "white/"
        if square.color is Colors.BLACK: path += "black/"

        if square.piece is Pieces.PAWN: path += "pawn.png"
        if square.piece is Pieces.BISHOP: path += "bishop.png"
        if square.piece is Pieces.KNIGHT: path += "knight.png"
        if square.piece is Pieces.ROOK: path += "rook.png"
        if square.piece is Pieces.QUEEN: path += "queen.png"
        if square.piece is Pieces.KING: path += "king.png"

        return path