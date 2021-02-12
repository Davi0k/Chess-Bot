from PIL import Image
from typing import Union

import chess

class Generator:
    layout = [
        [ chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8 ],
        [ chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7 ],
        [ chess.A6, chess.B6, chess.C6, chess.D6, chess.E6, chess.F6, chess.G6, chess.H6 ],
        [ chess.A5, chess.B5, chess.C5, chess.D5, chess.E5, chess.F5, chess.G5, chess.H5 ],
        [ chess.A4, chess.B4, chess.C4, chess.D4, chess.E4, chess.F4, chess.G4, chess.H4 ],
        [ chess.A3, chess.B3, chess.C3, chess.D3, chess.E3, chess.F3, chess.G3, chess.H3 ],
        [ chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2 ],
        [ chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1 ]
    ]

    coordinates = [ 25, 109, 194, 279, 363, 448, 531, 616 ]

    @staticmethod
    def generate(board: chess.BaseBoard) -> Image:
        chessboard = Image.open("resources/chessboard.png")

        for y, Y in enumerate(Generator.coordinates):
            for x, X in enumerate(Generator.coordinates):
                piece = board.piece_at(Generator.layout[y][x])

                if piece is not None:
                    path = Generator.path(piece)
                else: continue

                piece = Image.open(path).convert("RGBA")
                
                chessboard.paste(piece, (X, Y), piece)

        return chessboard

    @staticmethod
    def path(piece: chess.Piece) -> Union[str, None]:
        path = "resources/"

        if piece.color == chess.WHITE: path += "white/"
        if piece.color == chess.BLACK: path += "black/"

        if piece.piece_type == chess.PAWN: path += "pawn.png"
        if piece.piece_type == chess.KNIGHT: path += "knight.png"
        if piece.piece_type == chess.BISHOP: path += "bishop.png"
        if piece.piece_type == chess.ROOK: path += "rook.png"
        if piece.piece_type == chess.QUEEN: path += "queen.png"
        if piece.piece_type == chess.KING: path += "king.png"

        return path