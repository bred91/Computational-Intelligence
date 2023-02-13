# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto
from copy import deepcopy, copy
import numpy as np
import matplotlib.pyplot as plt


class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

class HumanPlayer(quarto.Player):
    """Human player"""
    # needed for some debugging
    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return int(input("Choose piece: "))

    def place_piece(self) -> tuple[int, int]:
        return int(input("Place piece in row: ")), int(input("Place piece in column: "))
    

class QLeanrningPlayer(quarto.Player):
    '''Q-Learning Player'''    
    previous_state_choose = None           # previous state for choose action
    previous_state_place = None            # previous state for place action
    previous_choose = None                 # previous choose of a piece
    previous_place = None                  # previous place of a piece 
    previous_piece = None                  # previous piece

    def __init__(self, quarto: quarto.Quarto, mode, epsilon = 0.02, learning_rate = 1, discount_factor = 1) -> None:
        super().__init__(quarto)
        self.__quarto = quarto
        self.mode = mode                            # mode, to separate between training and testing
                                                    # in training mode, the player will update the Q-table (or take a random action)
                                                    # in testing mode, the player will only take the best action, according to the Q-table
        if self.mode == "TRAIN":
            self.epsilon = epsilon                  # epsilon
        else:
            self.epsilon = 0                        # we want no random actions
        self.learning_rate = learning_rate          # alpha
        self.discount_factor = discount_factor      # gamma 

        self.choose_q = {}                          # Q-table for choose actions
        self.place_q = {}                           # Q-table 2 for place actions
        
        self.win_reward = 100                       # reward for winning   
        self.loss_reward = -100                     # reward for losing
        self.draw_reward = 0                        # reward for drawing

        self.makeKey(self._Player__quarto._Quarto__board, "CHOOSE")
        self.makeKey(self._Player__quarto._Quarto__board, "PLACE")

        self.c = 0

        

    def makeKey(self, state, action, piece = None):
        # choose q-table
        if action == "CHOOSE":
            possible_actions = self.free_pieces(state)

            for i in possible_actions:
                if (tuple(state.flatten()), i) not in self.choose_q:
                    self.choose_q[(tuple(state.flatten()), i)] = np.random.uniform(0.0,0.01)
        # place q-table
        elif action == "PLACE":
            possible_actions = self.free_places(state)
            #an_action = possible_actions[0]

            if piece is not None:
                for i in possible_actions:
                    if ((str(state), piece), tuple(i)) not in self.place_q:
                        self.place_q[((str(state), piece), tuple(i))] = np.random.uniform(0.0,0.01)
            else:
                for j in range(16):
                    for i in possible_actions:
                        if ((str(state), j), tuple(i)) not in self.place_q:
                            self.place_q[((str(state), j), tuple(i))] = np.random.uniform(0.0,0.01)           

    def is_terminal(self, nextstate = None) -> bool:
        '''check if the game is over'''
        if nextstate is None:            
            if self.__quarto.check_winner() > 0:
                return True
            else:
                return False
        else:
            if self.check_horizontal(nextstate) or self.check_diagonal(nextstate):
                return True
            else:
                return False

    def is_terminal_choose(self, state, piece) -> bool:
        for i in self.free_places(state):
            nextstate_bin = self._Player__quarto._Quarto__binary_board.copy()
            nextstate_bin[i[1], i[0]] = self._Player__quarto._Quarto__pieces[piece].binary
            if self.is_terminal(nextstate_bin):
                return True
        return False
    
    def check_horizontal(self, nextstate) -> int:
        hsum = np.sum(nextstate, axis=1)
        vsum = np.sum(nextstate, axis=0)

        if (4 in hsum or 0 in hsum) or (4 in vsum or 0 in vsum):
            return True
        else:
            return False

    def check_diagonal(self, nextstate) -> int:
        dsum1 = np.trace(nextstate, axis1=0, axis2=1)
        dsum2 = np.trace(np.fliplr(nextstate), axis1=0, axis2=1)

        if 4 in dsum1 or 4 in dsum2 or 0 in dsum1 or 0 in dsum2:
            return True
        else:
            return False    
       

    def choose_piece(self) -> int:
        '''choose a piece'''
        state = self._Player__quarto._Quarto__board

        if self.mode == "TRAIN":
            # in training mode, the player will update the Q-table (or take a random action)
            return self.update_q2(state, "CHOOSE")
        else:
            # in testing mode, the player will only take the best action, according to the Q-table
            return self.best_choose_action(state)

    def place_piece(self) -> tuple[int, int]:
        '''place a piece'''
        state = self._Player__quarto._Quarto__board

        if self.mode == "TRAIN":
            # in training mode, the player will update the Q-table (or take a random action)
            return self.update_q2(state, "PLACE", self._Player__quarto._Quarto__selected_piece_index)
        else:
            # in game mode, the player will only take the best action, according to the Q-table
            return self.best_place_action(state, self._Player__quarto._Quarto__selected_piece_index)

    def free_places(self, state):
        '''returns a list of free places'''
        free_places_ = []
        for i in range(4):
            for j in range(4):
                if state[j,i] < 0:
                    free_places_.append([i, j])
        return free_places_

    def free_pieces(self, state):
        '''returns a list of free pieces'''
        free_pieces_ = []
        for i in range(16):
            if i not in state:
                free_pieces_.append(i)
        return free_pieces_

    def best_choose_action(self, state):
        '''return the best action, according to the Q-table 1'''
        possible_actions_ = self.free_pieces(state)
        q_values = [self.choose_q[(tuple(state.flatten()), a)] if (tuple(state.flatten()), a) in self.choose_q else np.random.uniform(0.0,0.01) for a in possible_actions_]
        return possible_actions_[np.argmax(q_values)]
    
    def best_place_action(self, state, piece):
        '''return the best action, according to the Q-table 2'''
        possible_actions_ = self.free_places(state)
        q_values = [self.place_q[((str(state), piece), tuple(a))] if ((str(state), piece), tuple(a)) in self.place_q else np.random.uniform(0.0,0.01) for a in possible_actions_]
        return possible_actions_[np.argmax(q_values)]

    def place_piece_train(self, state):
        if random.random() < self.epsilon:
            # take a random action
            possible_actions_ = self.free_places(state)
            chosen_action_idx = random.randint(0, len(possible_actions_)-1)
            return possible_actions_[chosen_action_idx]
        else:
            # take the best action, according to the Q-table
            return self.best_place_action(state, self._Player__quarto._Quarto__selected_piece_index)
    
    def choose_piece_train(self, state):
        if random.random() < self.epsilon:
            # take a random action
            possible_actions_ = self.free_pieces(state)
            chosen_action_idx = random.randint(0, len(possible_actions_)-1)
            return possible_actions_[chosen_action_idx]
        else:
            # take the best action, according to the Q-table
            return self.best_choose_action(state)

    def ending_rewards(self, winner):
        if winner == 0:
            # if the myplayer wins, the reward is 100
            self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)] += self.learning_rate * (self.win_reward - self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)])
            self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))] += self.learning_rate * (self.win_reward - self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))])
            self.previous_state_place = self.previous_place = self.previous_piece = None
            self.previous_state_choose = self.previous_choose = None 
        elif winner == 1:
            # if the opponent wins, the reward is -100
            self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)] += self.learning_rate * (self.loss_reward - self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)])
            self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))] += self.learning_rate * (self.loss_reward- self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))])
            self.previous_state_place = self.previous_place = self.previous_piece = None
            self.previous_state_choose = self.previous_choose = None  
        else:
            # draw
            self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)] += self.learning_rate * (self.draw_reward - self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)])
            self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))] += self.learning_rate * (self.draw_reward- self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))])
            self.previous_state_place = self.previous_place = self.previous_piece = None
            self.previous_state_choose = self.previous_choose = None 

    def update_q2(self, state, action, piece = None):
        '''update the Q-table'''
        if action == "CHOOSE":
            self.makeKey(state, action)
            current_choose = self.choose_piece_train(state)
            
            if self.previous_choose is not None:
                reward = 0 # the reward is 0 because choosing a piece is it never terminal
                #reward = self.loss_reward/16 if self.is_terminal_choose(state, current_choose) else 0
                maxQ = np.max([self.choose_q[(tuple(state.flatten()), a)] for a in self.free_pieces(state)])

                self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))] += self.learning_rate * (reward + self.discount_factor * maxQ - self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))])   
                self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)] += self.learning_rate * (reward + self.discount_factor * maxQ - self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)])

            self.previous_state_choose = state.copy().flatten()
            self.previous_choose = current_choose
            return current_choose

        elif action == "PLACE":
            self.makeKey(state, action, piece)
            current_place = self.place_piece_train(state)
            
            if self.previous_place is not None:
                next_state = state.copy()
                next_state_bin = self._Player__quarto._Quarto__binary_board.copy()
                next_state[current_place[1], current_place[0]] = piece
                next_state_bin[current_place[1], current_place[0]] = self._Player__quarto._Quarto__pieces[piece].binary

                reward = self.win_reward if self.is_terminal(next_state_bin) else 0                
                maxQ = np.max([self.place_q[((str(state), piece), tuple(a))] for a in self.free_places(state)])

                self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)] += self.learning_rate * (reward + self.discount_factor * maxQ - self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)])
                self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))] += self.learning_rate * (reward + self.discount_factor * maxQ - self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))])

            self.previous_state_place = state.copy()
            self.previous_piece = piece
            self.previous_place = current_place
            return current_place

    def update_q(self, state, action, piece = None):
        '''update the Q-table'''
        if action == "CHOOSE":
            self.makeKey(state, action)
            current_choose = self.choose_piece_train(state)
            
            if self.previous_choose is not None:
                reward = 0 # the reward is 0 because choosing a piece is it never terminal
                #reward = self.loss_reward/16 if self.is_terminal_choose(state, current_choose) else 0
                maxQ = np.max([self.choose_q[(tuple(state), a)] for a in self.free_pieces(state)])
                    
                self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)] += self.learning_rate * (reward + self.discount_factor * maxQ - self.choose_q[(tuple(self.previous_state_choose), self.previous_choose)])

            self.previous_state_choose = state.copy()
            self.previous_choose = current_choose
            return current_choose

        elif action == "PLACE":
            self.makeKey(state, action, piece)
            current_place = self.place_piece_train(state)
            
            if self.previous_place is not None:
                next_state = state.copy()
                next_state_bin = self._Player__quarto._Quarto__binary_board.copy()
                next_state[current_place[1], current_place[0]] = piece
                next_state_bin[current_place[1], current_place[0]] = self._Player__quarto._Quarto__pieces[piece].binary

                reward = self.win_reward if self.is_terminal(next_state_bin) else 0                
                maxQ = np.max([self.place_q[((str(state), piece), tuple(a))] for a in self.free_places(state)])

                self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))] += self.learning_rate * (reward + self.discount_factor * maxQ - self.place_q[((str(self.previous_state_place), self.previous_piece), tuple(self.previous_place))])

            self.previous_state_place = state.copy()
            self.previous_piece = piece
            self.previous_place = current_place
            return current_place

    def get_clone_for_test(self):
        '''Create a copy of the player, but in testing mode'''
        clone_for_test = copy(self)
        clone_for_test.mode = "GAME"
        return clone_for_test
        

def train():
    game = quarto.Quarto()
    my_player = QLeanrningPlayer(game, "TRAIN")
    game.set_players((my_player, RandomPlayer(game)))

    epochs = 2000
    history = []
    winrate_history = []
    phases = 5

    for f in range(phases):
        if f == 0:
            epochs = 100
        else:
            epochs = 10000
        for e in range(epochs):
            game.reset()
            winner = game.run(False)
            #logging.warning(f"train: e: {e} Winner: player {winner}")

            history.append(winner)

            my_player.ending_rewards(winner)
            
            if (e != 0) and (e % 50 == 0):            
                s50 = history[-50:]
                wi = len([s for s in s50 if s == 0])
                lo = 50 - wi
                winrate_history.append(wi/(wi+lo))
                logging.warning(f"train: f: {f} e: {e} winrate: {wi/(wi+lo)} place {len(my_player.place_q)} choose {len(my_player.choose_q)}")


        game.reset()       
        new_adv = my_player.get_clone_for_test()
        game.set_players((my_player, new_adv))

           
    print(f"matches: {epochs}")
    #print(f"history: {history}")
    #logging.warning(f"train: e: {e} Winner: player {winner}")
    plt.plot(winrate_history)

    # todo: aggiungere salvataggio tabelle

    


def main():
    game = quarto.Quarto()
    game.set_players((QLeanrningPlayer(game, "TRAIN"), RandomPlayer(game)))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
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

    #train()
    main()