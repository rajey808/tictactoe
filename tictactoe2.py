import pygame
import random

# Rewards
game_win = 10
game_lose = -10
draw = 0
agent_moved = -1
# opponent_blocked = 5

# Initialize Pygame

pygame.init()

# Set up the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')
pygame.font.Font()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

BOARD_SIZE = 3
CELL_SIZE = WINDOW_WIDTH // BOARD_SIZE
# board = [[''] * BOARD_SIZE for _ in range(BOARD_SIZE)]

class TicTacToe():
    def __init__(self) -> None:
        self.board = [['_'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.state_representation = ['_'] * 9

    def reset(self):
        self.board = [['_'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.state_representation = ['_'] * 9

    def is_empty(self, position):
        return self.state_representation[position] == '_'
    
    def make_move(self, row, col, symbol):
        position = row * BOARD_SIZE + col
        if self.is_empty(position):
            self.board[row][col] = symbol
            self.state_representation[position] = symbol
            return True
        else:
            return False
        
    def is_winner(self, symbol):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combination in winning_combinations:
            if all(self.state_representation[position] == symbol for position in combination):
                return True
        return False

    def is_draw(self):
        return '_' not in self.state_representation
    
    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()
    
class TicTacToeAgent:
    def __init__(self) -> None:
        self.q_values = {}

    def get_q_values(self, state, action):
        return self.q_values.get((tuple(state), tuple(action)), 0.0)
    
    def update_q_values(self, state, action, new_q_value):
        self.q_values[(tuple(state), tuple(action))] = new_q_value

    def get_best_action(self, state, actions, epsilon):
        if random.random() < epsilon:
            return random.choice(actions)
        else:
            best_action = None
            best_q_value = float('-inf')

            for action in actions:
                q_value = self.get_q_values(state, action)
                if q_value > best_q_value:
                    best_action = action
                    best_q_value = q_value
            
            return best_action
        
    def load_q_values(self, loaded_q_values):
        self.q_values = list(loaded_q_values)
    
def get_state_representation(board):
    state_representation = ''
    for row in board:
        new_row = ''
        for char in row:
            if char == '':
                char = '_'
            new_row += char
        state_representation += new_row

    return state_representation

def get_available_actions(board):
    actions = []
    for ri, row in enumerate(board):
        for ci, col in enumerate(row):
            if col == '_':
                actions.append((ri,ci))

    return actions

def main():

    train_agent = True

    ticTacToeEnv = TicTacToe()
    ticTacToeAgent = TicTacToeAgent()
    
    num_training_interations = 500
    learning_rate = 0.1
    discount_factor = 0.9
    epsilon = 0.9

    x_agent = 'X'
    o_agent = 'O'
    current_player = 'X'

    game_over = False
    winner = None

    # Train agent or load values
    if not train_agent:
        with open('./tictactoeAgent.txt', 'r+') as tictactoeAgentFile:
            ticTacToeAgent.load_q_values(tictactoeAgentFile.read())
            # print(f'{train_agent}\n{ticTacToeAgent.q_values}')
    else:
        for iteration in range(num_training_interations):
            ticTacToeEnv.reset()
            state = ticTacToeEnv.board
            state_representation = get_state_representation(state)

            count = 0
            while not ticTacToeEnv.is_game_over():
            # while count < 2:
                actions = get_available_actions(state)
                action = ticTacToeAgent.get_best_action(state_representation, actions, epsilon)
                epsilon -= 0.05

                if epsilon < 0.2:
                    epsilon = 0.2
                count += 1

                ticTacToeEnv.make_move(action[0], action[1], 'X')

                state = ticTacToeEnv.board
                state_representation = get_state_representation(state)

                if ticTacToeEnv.is_game_over():
                    reward = 0
                    if ticTacToeEnv.is_winner('X'):
                        reward = game_win
                    elif ticTacToeEnv.is_winner('0'):
                        reward = game_lose
                    else:
                        reward = draw
                    ticTacToeAgent.update_q_values(state_representation, action, reward)

                else:
                    opponent_action = random.choice(get_available_actions(state))
                    ticTacToeEnv.make_move(opponent_action[0], opponent_action[1], 'O')

                    state = ticTacToeEnv.board
                    state_representation = get_state_representation(state)

                    reward = agent_moved
                    next_state = ticTacToeEnv.board
                    next_state_representation = get_state_representation(next_state)
                    next_actions = get_available_actions(next_state)
                    next_action = ticTacToeAgent.get_best_action(state_representation, next_actions, epsilon)
                    next_q_value = ticTacToeAgent.get_q_values(next_state_representation, next_action)

                    new_q_value = (1 - learning_rate) * ticTacToeAgent.get_q_values(state_representation, action) + learning_rate * (reward + discount_factor * next_q_value)
                    ticTacToeAgent.update_q_values(state_representation, action, new_q_value)

            # print(f'{ticTacToeAgent.q_values}')

        print(f'Agent Trained')
        # print(f'{ticTacToeAgent.q_values}')

        with open('./tictactoeAgent.txt', 'w+') as tictactoeAgentFile:
            tictactoeAgentFile.write(str(dict(ticTacToeAgent.q_values)))

    

    '''
    # Play against player
    # Start Game
    running = True
    epsilon = 0.05
    while running:

        #if ticTacToeEnv.is_game_over():
            #game_over = True

        game_over = ticTacToeEnv.is_game_over()

        if '_' not in ticTacToeEnv.board:
            ticTacToeEnv.is_winner(current_player)

        if not game_over:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False

                #elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not current_player == 'X':
                elif current_player == 'X':

                    state = ticTacToeEnv.board
                    state_representation = get_state_representation(state)
                    actions = get_available_actions(state)

                    if 'X' not in state_representation and 'O' not in state_representation:
                        action = random.choice(actions)
                    else: 
                        action = ticTacToeAgent.get_best_action(state_representation, actions, epsilon)
                    ticTacToeEnv.make_move(action[0], action[1], 'X')

                    # Check for a winner
                    if ticTacToeEnv.is_winner(current_player):
                        winner = current_player
                    if current_player == 'X':
                        current_player = 'O'
                    else:   
                        current_player = 'X'

                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not current_player == 'X':
                    if pygame.mouse.get_pressed()[0]:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        clicked_row = mouse_y // CELL_SIZE
                        clicked_col = mouse_x // CELL_SIZE

                        if ticTacToeEnv.board[clicked_row][clicked_col] == '_' :
                            ticTacToeEnv.board[clicked_row][clicked_col] = current_player

                            position = clicked_row * BOARD_SIZE + clicked_col
                            ticTacToeEnv.state_representation[position] = current_player

                            # Check for a winner
                            if ticTacToeEnv.is_winner(current_player):
                                winner = current_player

                            if current_player == 'X':
                                current_player = 'O'
                            else:   
                                current_player = 'X'

            # Draw the game board
            window.fill(WHITE)
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    cell_x = col * CELL_SIZE
                    cell_y = row * CELL_SIZE

                    pygame.draw.rect(window, BLACK, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 2)

                    if ticTacToeEnv.board[row][col] == 'X':
                        pygame.draw.line(window, BLACK, (cell_x + 10, cell_y + 10), (cell_x + CELL_SIZE - 10, cell_y + CELL_SIZE - 10), 2)
                        pygame.draw.line(window, BLACK, (cell_x + CELL_SIZE - 10, cell_y + 10), (cell_x + 10, cell_y + CELL_SIZE - 10), 2)
                    elif ticTacToeEnv.board[row][col] == 'O':
                        pygame.draw.circle(window, BLACK, (cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 2)

        if game_over:
            if winner:
                message = f"Player {winner} wins!"
            else:
                message = "It's a tie!"
            text = pygame.font.Font(None, 40).render(message, True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            window.blit(text, text_rect)
            running = False

        # Update the display
        pygame.display.update()

        #if is_current_player_bot:
        #   pygame.time.wait(1000)
        '''

    # Quit Pygame
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()