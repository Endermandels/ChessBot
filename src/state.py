from typing import NamedTuple
from toolbox import *

class Piece:
    WHITE_PAWN = 0
    WHITE_ROOK = 1
    WHITE_KNIGHT = 2
    WHITE_BISHOP = 3
    WHITE_QUEEN = 4
    WHITE_KING = 5
    
    BLACK_PAWN = 6
    BLACK_ROOK = 7
    BLACK_KNIGHT = 8
    BLACK_BISHOP = 9
    BLACK_QUEEN = 10
    BLACK_KING = 11

class State(NamedTuple):
    """ Immutable state of chess game """
    # Bitboard
    piece_types: tuple[int,...] = (0,0,0,0,0,0, 0,0,0,0,0,0) # white_pawn through black_king
    
    # Game rules
    white_turn: bool = True
    castling_rights: int = 0b1111 # 0b0001=white can castle short, 0b1000=black can castle long, etc.
    en_passant_square: int = 0 # which spaces are possible to en passant (set when a pawn moves 2 spaces)

def is_illegal_piece_selection(state: State, selected_space: int) -> bool:
    """ Returns whether the selected space is illegal for the given state """
    # TODO: Implement
    return False

def is_illegal_target_space(state: State, piece_to_move: int, target_space: int) -> bool:
    # TODO: Implement
    return False

def convert_selected_space_to_int(selected_space: str) -> int:
    """ Returns converted space integer, or 0 if selected space is illegal """
    if len(selected_space) != 2:
        warn("* Invalid length")
        return 0
    
    col =  ord(selected_space[0]) - ord('A') 
    row = 7 - ord(selected_space[1]) + ord('1') # Reverse this because of how it's displayed in view
    if col < 0 or col > 7:
        warn(f"* Invalid column: {selected_space[0]}")
        return 0
    if row < 0 or row > 7:
        warn(f"* Invalid row: {selected_space[1]}")
        return 0
        
    res = 1 << (8*row + col)
    return res

def get_new_state(state: State, selected_space: int, target_space: int) -> State:
    """ Move selected piece on bit board to target space on bit board (assumes this is legal) """
    # TODO: Fix this function
    if selected_space == 0 or target_space == 0:
        return state
    selected_mask = selected_space ^ 0xFFFFFFFFFFFFFFFF
    
    new_piece_types = tuple(pt & selected_mask | (target_space if pt & selected_space else 0) for pt in state.piece_types)
    return State(piece_types=new_piece_types, white_turn=not state.white_turn)