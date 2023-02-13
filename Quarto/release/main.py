# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto
import time

# Set up logging
# logging.basicConfig(level=logging.DEBUG)
MAX_DEPTH = 2       # default value
BOARD_SIDE = 4


class RandomPlayer(quarto.Player):
    """Random player"""   

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)       

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)


class MinmaxPlayer(quarto.Player):
    """Minmax player""" 
    BOARD_SIDE = 4   

    def __init__(self, quarto: quarto.Quarto) -> None:
        '''This function is used to initialize the player'''
        super().__init__(quarto)
        self.__pieces = self._Player__quarto._Quarto__pieces
        self.maxDepth = MAX_DEPTH

    def choose_piece(self) -> int:
        '''This function is used to choose the best piece'''
        # Initialize alpha and beta to negative infinity and positive infinity respectively
        alpha = float('-inf')
        beta = float('inf')
        
        # Initialize the best move and best score as None
        best_move = None
        best_score = None
        # Get the board status
        board = self._Player__quarto.get_board_status()  
        # Get the available pieces, the ones that are not on the board
        available_pieces = len(self.get_available_pieces(board))

        # if there are more than 14 available pieces then choose a random piece
        # this is done to avoid the minimax algorithm to take too much time to choose a piece
        # at a stage where it is impossible to win and therefore the individual move can be choosen more lightly
        if available_pieces >= 15:
            return random.Random().choice(self.get_available_pieces(board))

        start = time.time()
        end = time.time()

        # this loop is used to increase the maxDepth of the minmax algorithm in case the best move is not found in the first iteration
        # the loop will stop when the best move is found or when the time limit is reached
        while ((best_score is None or best_score < 0) and end - start < 2):            
            # Iterate through all the available pieces
            for piece in self.get_available_pieces(board):
                boardo = board.copy()
                # Call the minimax function to get the score of this move
                score = self.minmax(boardo, "place", 0, False, None,  piece, alpha, beta, start)
                if best_score is None or score > best_score:
                    best_score = score
                    best_move = piece                
                # Update alpha
                alpha = max(alpha, best_score)                
            end = time.time()

            # if available_pieces <= 11 then increase the maxDepth to search deeper in the tree for a better move
            # for available_piaces > 11 the maxDepth is always set to 2
            if available_pieces <= 11:
                self.maxDepth += 1

        # at the end of the search reset the maxDepth to the default value
        self.maxDepth = MAX_DEPTH
        return best_move

    def place_piece(self) -> tuple[int, int]:
        '''This function is used to choose the best position to place the selected piece'''
        # Initialize alpha and beta to negative infinity and positive infinity respectively
        alpha = float('-inf')
        beta = float('inf')

        # Get the board status
        board = self._Player__quarto.get_board_status()
        piece = self._Player__quarto.get_selected_piece()
        # Initialize the best move and best score as None
        best_move = None
        best_score = None
        # Get the available pieces, the ones that are not on the board
        available_pieces = len(self.get_available_pieces(board))

        # if there are more than 14 available pieces then choose a random position
        # this is done to avoid the minimax algorithm to take too much time to choose a position
        # at a stage where it is impossible to win and therefore the individual move can be choosen more lightly
        if available_pieces >= 15:
            return random.Random().choice(self.get_available_positions(board))

        start = time.time()
        end = time.time()

        # this loop is used to increase the maxDepth of the minmax algorithm in case the best move is not found in the first iteration
        # the loop will stop when the best move is found or when the time limit is reached
        while ((best_score is None or best_score < 0) and end - start < 3):            
            # Iterate through all the available pieces
            for x, y in self.get_available_positions(board):
                boardo = board.copy()
                # Call the minimax function to get the score of this move
                score = self.minmax(boardo, "choose", 0, False, (x, y),  piece, alpha, beta, start)
                if best_score is None or score > best_score:
                    best_score = score
                    best_move = (x, y)
                
                # Update alpha
                alpha = max(alpha, best_score)
                
            end = time.time()

            # if available_pieces <= 11 then increase the maxDepth to search deeper in the tree for a better move
            # for available_piaces > 11 the maxDepth is always set to 2
            if available_pieces <= 11:
                self.maxDepth += 1
            elif available_pieces <= 8:
                self.maxDepth += 3

        # at the end of the search reset the maxDepth to the default value
        self.maxDepth = MAX_DEPTH        
        return best_move

    def minmax(self, board, move_type, depth: int, is_maximizing: bool, move, piece, alpha: float, beta: float, start: float = None) -> float:
        '''This function is used to calculate the score of a move using the minimax algorithm'''
        # If the game is over or the maximum depth is reached, return the score of the board
        if depth == self.maxDepth and not self.is_game_over(board):
            # if the game is not over and the maximum depth is reached, return 0 for that branch
            return 0
        elif self.is_game_over(board):
            if is_maximizing:
                # If the maximizing player won, return 1 - (depth / MAX_DEPTH)
                # This is done to give more importance to the winning branches that are closer to the root
                return 1 - (depth / MAX_DEPTH)
            else:
                # If the minimizing player won, return -1
                return -1

        # If the time is up, exit the search
        if start is not None:
            end = time.time()
            if end - start > 4.9:
                return -1

        # maximizing 
        if is_maximizing:
            # Initialize the best score as negative infinity
            best_score = float('-inf')

            # If the move type is "place"
            if move_type == "place":
                # all the next possible moves
                next_moves = self.get_available_positions(board)        
                        
                # Iterate through all the next possible moves
                for next_move in next_moves:
                    boardo = board.copy()                    
                    # Call the minimax function recursively and update the best score
                    # obviously the next move is to choose a piece to place
                    score = self.minmax(boardo, "choose", depth + 1, False, next_move, piece, alpha, beta, start)
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    # If beta <= alpha, cut-off the branch
                    if beta <= alpha:
                        break

            # If the move type is "choose"        
            elif move_type == "choose":
                # All the next possible moves
                board[move[1]][move[0]] = piece
                next_moves = self.get_available_pieces(board)

                # Iterate through all the next possible moves
                for next_move in next_moves:
                    boardo = board.copy()
                    # Call the minimax function recursively and update the best score
                    # obviously the next move is to place the piece that is chosen
                    score = self.minmax(boardo, "place", depth + 1, False, None, next_move, alpha, beta, start)
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    # If beta <= alpha, cut-off the branch
                    if beta <= alpha:
                        break
            
            return best_score
        
        # minimizing 
        else:
            # Initialize the best score as positive infinity
            best_score = float('inf')

            # If the move type is "place"
            if move_type == "place":
                # all the next possible moves
                next_moves = self.get_available_positions(board)        
                        
                # Iterate through all the next possible moves
                for next_move in next_moves:
                    boardo = board.copy()
                    # Call the minimax function recursively and update the best score
                    # obviously the next move is to choose a piece
                    score = self.minmax(boardo, "choose", depth + 1, True, next_move, piece, alpha, beta, start)
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    # If beta <= alpha, cut-off the branch
                    if beta <= alpha:
                        break

            # If the move type is "choose"
            elif move_type == "choose":
                # All the next possible moves
                board[move[1]][move[0]] = piece
                next_moves = self.get_available_pieces(board)

                # Iterate through all the next possible moves
                for next_move in next_moves:
                    boardo = board.copy()
                    # Call the minimax function recursively and update the best score
                    # obviously the next move is to place the piece that is chosen
                    score = self.minmax(boardo, "place", depth + 1, True, None, next_move, alpha, beta, start)
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    # If beta <= alpha, cut-off the branch
                    if beta <= alpha:
                        break

            return best_score
    
    def get_available_pieces(self, board) -> list[int]:
        """Return the list of available pieces"""
        available_pieces = []
        for piece in range(16):
            if piece not in board:
                available_pieces.append(piece)
        return available_pieces

    def get_available_positions(self, board) -> list[tuple[int, int]]:
        """Return the list of available positions"""
        available_positions = []
        for x in range(4):
            for y in range(4):
                if board[y,x] == -1:
                    available_positions.append((x, y))
        return available_positions

    def is_game_over(self, board) -> bool:
        """Return True if the game is over, False otherwise"""
        return self.check_horizontal(board) or self.check_vertical(board) or self.check_diagonal(board)

    def check_horizontal(self, board) -> int:
        """Return True if there is a horizontal line of 4 pieces with the same trait, False otherwise"""
        for i in range(4):
            high_values = [
                elem for elem in board[i] if elem >= 0 and self.__pieces[elem].HIGH
            ]
            coloured_values = [
                elem for elem in board[i] if elem >= 0 and self.__pieces[elem].COLOURED
            ]
            solid_values = [
                elem for elem in board[i] if elem >= 0 and self.__pieces[elem].SOLID
            ]
            square_values = [
                elem for elem in board[i] if elem >= 0 and self.__pieces[elem].SQUARE
            ]
            low_values = [
                elem for elem in board[i] if elem >= 0 and not self.__pieces[elem].HIGH
            ]
            noncolor_values = [
                elem for elem in board[i] if elem >= 0 and not self.__pieces[elem].COLOURED
            ]
            hollow_values = [
                elem for elem in board[i] if elem >= 0 and not self.__pieces[elem].SOLID
            ]
            circle_values = [
                elem for elem in board[i] if elem >= 0 and not self.__pieces[elem].SQUARE
            ]
            if len(high_values) == self.BOARD_SIDE or len(
                    coloured_values
            ) == self.BOARD_SIDE or len(solid_values) == self.BOARD_SIDE or len(
                    square_values) == self.BOARD_SIDE or len(low_values) == self.BOARD_SIDE or len(
                        noncolor_values) == self.BOARD_SIDE or len(
                            hollow_values) == self.BOARD_SIDE or len(
                                circle_values) == self.BOARD_SIDE:
                return True
        return False

    def check_vertical(self, board):
        '''Return True if there is a vertical line of 4 pieces with the same trait, False otherwise'''
        for i in range(4):
            high_values = [
                elem for elem in board[:, i] if elem >= 0 and self.__pieces[elem].HIGH
            ]
            coloured_values = [
                elem for elem in board[:, i] if elem >= 0 and self.__pieces[elem].COLOURED
            ]
            solid_values = [
                elem for elem in board[:, i] if elem >= 0 and self.__pieces[elem].SOLID
            ]
            square_values = [
                elem for elem in board[:, i] if elem >= 0 and self.__pieces[elem].SQUARE
            ]
            low_values = [
                elem for elem in board[:, i] if elem >= 0 and not self.__pieces[elem].HIGH
            ]
            noncolor_values = [
                elem for elem in board[:, i] if elem >= 0 and not self.__pieces[elem].COLOURED
            ]
            hollow_values = [
                elem for elem in board[:, i] if elem >= 0 and not self.__pieces[elem].SOLID
            ]
            circle_values = [
                elem for elem in board[:, i] if elem >= 0 and not self.__pieces[elem].SQUARE
            ]
            if len(high_values) == self.BOARD_SIDE or len(
                    coloured_values
            ) == self.BOARD_SIDE or len(solid_values) == self.BOARD_SIDE or len(
                    square_values) == self.BOARD_SIDE or len(low_values) == self.BOARD_SIDE or len(
                        noncolor_values) == self.BOARD_SIDE or len(
                            hollow_values) == self.BOARD_SIDE or len(
                                circle_values) == self.BOARD_SIDE:
                return True
        return False

    def check_diagonal(self, board):
        '''Return True if there is a diagonal line of 4 pieces with the same trait, False otherwise'''
        high_values = []
        coloured_values = []
        solid_values = []
        square_values = []
        low_values = []
        noncolor_values = []
        hollow_values = []
        circle_values = []
        for i in range(self.BOARD_SIDE):
            if board[i, i] < 0:
                break
            if self.__pieces[board[i, i]].HIGH:
                high_values.append(board[i, i])
            else:
                low_values.append(board[i, i])
            if self.__pieces[board[i, i]].COLOURED:
                coloured_values.append(board[i, i])
            else:
                noncolor_values.append(board[i, i])
            if self.__pieces[board[i, i]].SOLID:
                solid_values.append(board[i, i])
            else:
                hollow_values.append(board[i, i])
            if self.__pieces[board[i, i]].SQUARE:
                square_values.append(board[i, i])
            else:
                circle_values.append(board[i, i])
        if len(high_values) == self.BOARD_SIDE or len(coloured_values) == self.BOARD_SIDE or len(
                solid_values) == self.BOARD_SIDE or len(square_values) == self.BOARD_SIDE or len(
                    low_values
        ) == self.BOARD_SIDE or len(noncolor_values) == self.BOARD_SIDE or len(
                    hollow_values) == self.BOARD_SIDE or len(circle_values) == self.BOARD_SIDE:
            return True
        high_values = []
        coloured_values = []
        solid_values = []
        square_values = []
        low_values = []
        noncolor_values = []
        hollow_values = []
        circle_values = []
        for i in range(self.BOARD_SIDE):
            if board[i, self.BOARD_SIDE - 1 - i] < 0:
                break
            if self.__pieces[board[i, self.BOARD_SIDE - 1 - i]].HIGH:
                high_values.append(board[i, self.BOARD_SIDE - 1 - i])
            else:
                low_values.append(board[i, self.BOARD_SIDE - 1 - i])
            if self.__pieces[board[i, self.BOARD_SIDE - 1 - i]].COLOURED:
                coloured_values.append(
                    board[i, self.BOARD_SIDE - 1 - i])
            else:
                noncolor_values.append(
                    board[i, self.BOARD_SIDE - 1 - i])
            if self.__pieces[board[i, self.BOARD_SIDE - 1 - i]].SOLID:
                solid_values.append(board[i, self.BOARD_SIDE - 1 - i])
            else:
                hollow_values.append(board[i, self.BOARD_SIDE - 1 - i])
            if self.__pieces[board[i, self.BOARD_SIDE - 1 - i]].SQUARE:
                square_values.append(board[i, self.BOARD_SIDE - 1 - i])
            else:
                circle_values.append(board[i, self.BOARD_SIDE - 1 - i])
        if len(high_values) == self.BOARD_SIDE or len(coloured_values) == self.BOARD_SIDE or len(
                solid_values) == self.BOARD_SIDE or len(square_values) == self.BOARD_SIDE or len(
                    low_values
        ) == self.BOARD_SIDE or len(noncolor_values) == self.BOARD_SIDE or len(
                    hollow_values) == self.BOARD_SIDE or len(circle_values) == self.BOARD_SIDE:
            return True
        return False  
    
def test():
    '''A method to test the agent and collect some statistics'''
    game = quarto.Quarto()

    matches = 100
    wins1 = 0
    wins2 = 0
    losses1 = 0
    losses2 = 0
    draws1 = 0
    draws2 = 0

    start = time.time()
    cont = 0
    c_max = 0
    p_max = 0

    for i in range(matches//2):
        game.reset()
        game.set_players((MinmaxPlayer(game), RandomPlayer(game)))
        winner, max_c, max_p, conto = game.run2(False)

        if max_c > c_max:
            c_max = max_c
        if max_p > p_max:
            p_max = max_p

        if winner == 0:
            wins1 += 1
        elif winner == 1:
            losses1 += 1
            print(f"pieces: {conto}")
        else:
            draws1 += 1
        cont += 1
        if cont % 10 == 0:
            logging.warning(f"matches: {cont} winrate: {wins1/cont} max c: {c_max} max p: {p_max}")
        

    logging.warning(f"Agent as first player: Wins: {wins1} Losses: {losses1} Draws: {draws1} Max c: {c_max} Max p: {p_max}")
    
    cont = 0
    c_max = 0
    p_max = 0

    for i in range(matches//2):
        game.reset()
        game.set_players((RandomPlayer(game), MinmaxPlayer(game)))
        winner, max_c, max_p, conto = game.run2(False)
        if max_c > c_max:
            c_max = max_c
        if max_p > p_max:
            p_max = max_p

        if winner == 0:
            losses2 += 1
            print(f"pieces: {conto}")
        elif winner == 1:
            wins2 += 1
        else:
            draws2 += 1
        cont += 1

        if cont % 10 == 0:
            logging.warning(f"matches: {cont} winrate: {wins2/cont} max c: {c_max} max p: {p_max}")
   
    end = time.time()

    
    logging.warning(f"Agent as second player: Wins: {wins2} Losses: {losses2} Draws: {draws2}")
    logging.warning(f"Total: Wins: {wins1 + wins2} Losses: {losses1 + losses2} Draws: {draws1 + draws2}")
    logging.warning(f"Max c: {c_max} Max p: {p_max}")
    logging.warning(f"Time: {end - start} seconds for {matches} matches ({(end - start)/matches} seconds per match) ")
    input("Press any key to continue...")


def main():
    win_string = None
    game = quarto.Quarto()
    game.set_players((RandomPlayer(game), MinmaxPlayer(game)))

    winner = game.run()
    if winner == 0:
        win_string = "Random Win"
    elif winner == 1:
        win_string = "MinMax Win"
    else:
        win_string = "Draw"
    logging.warning(f"main: Result: {win_string}")

    input("Press any key to continue...")
    game.reset()
    game.set_players((MinmaxPlayer(game), RandomPlayer(game)))

    winner = game.run()
    if winner == 0:
        win_string = "MinMax Win"
    elif winner == 1:
        win_string = "Random Win"
    else:
        win_string = "Draw"
    logging.warning(f"main: Result: {win_string}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    #test()
    main()