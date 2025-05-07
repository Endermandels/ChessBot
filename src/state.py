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
    piece_types: tuple[int,...] = (
        # Bitboards for white pieces
        0b0000000011111111000000000000000000000000000000000000000000000000,
        0b1000000100000000000000000000000000000000000000000000000000000000,
        0b0100001000000000000000000000000000000000000000000000000000000000,
        0b0010010000000000000000000000000000000000000000000000000000000000,
        0b0000100000000000000000000000000000000000000000000000000000000000,
        0b0001000000000000000000000000000000000000000000000000000000000000,
        # Bitboards for black pieces (mirrored from white)
        0b0000000000000000000000000000000000000000000000001111111100000000,
        0b0000000000000000000000000000000000000000000000000000000010000001,
        0b0000000000000000000000000000000000000000000000000000000001000010,
        0b0000000000000000000000000000000000000000000000000000000000100100,
        0b0000000000000000000000000000000000000000000000000000000000001000,
        0b0000000000000000000000000000000000000000000000000000000000010000,
    ) # white_pawn through black_king
    
    # Game rules
    white_turn: bool = True
    castling_rights: int = 0b1111 # 0b0001=white can castle short, 0b1000=black can castle long, etc.
    en_passant_square: int = 0 # which spaces are possible to en passant (set when a pawn moves 2 spaces)

def is_white_piece(piece_type: int) -> bool:
    return piece_type < 6

def is_pawn(pt: int) -> bool:
    return pt == Piece.WHITE_PAWN or pt == Piece.BLACK_PAWN

def is_rook(pt: int) -> bool:
    return pt == Piece.WHITE_ROOK or pt == Piece.BLACK_ROOK

def is_knight(pt: int) -> bool:
    return pt == Piece.WHITE_KNIGHT or pt == Piece.BLACK_KNIGHT

def is_bishop(pt: int) -> bool:
    return pt == Piece.WHITE_BISHOP or pt == Piece.BLACK_BISHOP

def is_queen(pt: int) -> bool:
    return pt == Piece.WHITE_QUEEN or pt == Piece.BLACK_QUEEN

def is_king(pt: int) -> bool:
    return pt == Piece.WHITE_KING or pt == Piece.BLACK_KING

def get_piece_type(state: State, selected_space: int) -> int:
    """ Returns the piece type of the selected space; -1 if selected_space is empty """
    for pt, bb in enumerate(state.piece_types):
        if bb & selected_space:
            return pt
    return -1

def is_illegal_pawn_move(state: State, pt: int, src: int, dst: int) -> bool:
    """ Returns whether the pawn moving from src to dst is legal """
    direction = -1 if is_white_piece(pt) else 1 # white = up, black = down
    start_row = 1 if is_white_piece(pt) else 6 # 2nd row for white, 7th row for black

    src_index = src.bit_length() - 1 # the higher the number, the closer to the white pieces
    dst_index = dst.bit_length() - 1
    src_row, src_col = divmod(src_index, 8)
    dst_row, dst_col = divmod(dst_index, 8)

    delta_row = dst_row - src_row

    # Moving straight
    if dst_col == src_col:
        if (delta_row > 0) != (direction > 0):
            warn("* Cannot move pawn backwards")
            return True # Can't go in the opposite direction

    # Moving straight 2 spaces from beginning to an open space
    # Moving diagonal to capture an enemy piece
    # En passant

    return False

def is_illegal_piece_move(state: State, src: int, dst: int) -> bool:
    """ Returns whether moving the piece at src to dst is illegal """
    pt = get_piece_type(state, src)
    if is_pawn(pt):
        return is_illegal_pawn_move(state, pt, src, dst)
    return False

def is_illegal_target_space(state: State, piece_to_move: int, target_space: int) -> bool:
    """ Returns whether the target space is illegal given the board state and piece to move """
    if piece_to_move == 0 or target_space == 0:
        return True
    
    pt_target = get_piece_type(state, target_space)
    pt_selected = get_piece_type(state, piece_to_move)
    
    # No piece at target space
    if pt_selected < 0:
        return True

    # Cannot capture own piece
    if pt_target > -1 and is_white_piece(pt_target) == is_white_piece(pt_selected):
        warn("* Cannot capture your own piece")
        return True
    
    # Check movement rules
    if is_illegal_piece_move(state, piece_to_move, target_space):
        return True
            
    return False

def is_illegal_piece_selection(state: State, selected_space: int) -> bool:
    """ Returns whether the selected space is illegal for the given state """
    if selected_space == 0:
        return True
    pt = get_piece_type(state, selected_space)
    if pt > -1:
        # found selected piece
        if is_white_piece(pt) and not state.white_turn:
            warn("* Cannot select WHITE piece on BLACK turn")
            return True
        if not is_white_piece(pt) and state.white_turn:
            warn("* Cannot select BLACK piece on WHITE turn")
            return True
        # no issues
        return False
    warn("* Cannot select empty space")
    return True

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
    if selected_space == 0 or target_space == 0:
        return state
    selected_mask = selected_space ^ 0xFFFFFFFFFFFFFFFF
    
    new_piece_types = tuple(pt & selected_mask | (target_space if pt & selected_space else 0) for pt in state.piece_types)
    return State(piece_types=new_piece_types, white_turn=not state.white_turn)