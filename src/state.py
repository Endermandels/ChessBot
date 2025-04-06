from typing import NamedTuple

class State(NamedTuple):
    """ Immutable state of chess game """
    # Bitboard
    white_pawns: int = 0
    white_rooks: int = 0
    white_knights: int = 0
    white_bishops: int = 0
    white_queens: int = 0
    white_king: int = 0
    
    black_pawns: int = 0
    black_rooks: int = 0
    black_knights: int = 0
    black_bishops: int = 0
    black_queens: int = 0
    black_king: int = 0
    
    # Game rules
    white_turn: bool = True
    castling_rights: int = 0b1111 # 0b0001=white can castle short, 0b1000=black can castle long, etc.
    en_passant_square: int = 0 # which spaces are possible to en passant (set when a pawn moves 2 spaces)
