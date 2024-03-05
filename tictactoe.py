import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Rewards
game_win = 10
game_lose = -10
draw = 0
agent_moved = -1
# oppopent_blocked = 5

class TicTacToeAgent:
    def __init__(self) -> None:
        self.q_values = {}

    def get_q_values(self, state, action):
        return self.q_values((state, action),0.0)
    
    def update_q_values(self, state, action, new_q_value):
        self.q_values[(state, action)] = new_q_value

    def get_best_action(self, state, actions):
        best_action = None
        best_q_value = float('-inf')

        for action in actions:
            q_value = self.get_q_values(state, action)
            if q_value > best_q_value:
                best_action = action
                best_q_value = q_value
        
        return best_action

def get_state_representation(board):
    state_representation = ''
    for row in board:
        new_row = ''
        for char in row:
            if char == '':
                char = '-'
            new_row += char
        state_representation += new_row

    return state_representation

def get_available_actions(state, board):
    actions = []
    for row in board:
        for col in row:
            if state[row][col] == '-':
                actions.append((row,col))

    return actions

def main():

    # Define game variables
    BOARD_SIZE = 3
    CELL_SIZE = WINDOW_WIDTH // BOARD_SIZE
    board = [[''] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    state_representation = ' '
    current_player = 'X'
    game_over = False
    winner = None
    is_x_bot = True
    is_o_bot = True
    is_current_player_bot = True

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if current_player == 'X' and is_x_bot:
                is_current_player_bot = True
            elif current_player == 'O' and is_o_bot:
                is_current_player_bot = True
            else:
                is_current_player_bot = False

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not is_current_player_bot:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_row = mouse_y // CELL_SIZE
                    clicked_col = mouse_x // CELL_SIZE

                    if board[clicked_row][clicked_col] == '':
                        board[clicked_row][clicked_col] = current_player

                        # Check for a winner
                        if ((board[clicked_row][0] == board[clicked_row][1] == board[clicked_row][2] == current_player) or
                                (board[0][clicked_col] == board[1][clicked_col] == board[2][clicked_col] == current_player) or
                                (board[0][0] == board[1][1] == board[2][2] == current_player) or
                                (board[0][2] == board[1][1] == board[2][0] == current_player)):
                            game_over = True
                            winner = current_player
                        elif all(board[row][col] != '' for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
                            game_over = True

                        # Switch player
                        if current_player == 'X':
                            current_player = 'O'
                        else:
                            current_player = 'X'
        if is_current_player_bot and not game_over:
            square_selected = False
            while not square_selected:
                rand_row = random.randint(0,2)
                rand_col = random.randint(0,2)

                if board[rand_row][rand_col] == '':
                    board[rand_row][rand_col] = current_player
                    square_selected = True

            clicked_row = rand_row
            clicked_col = rand_col

            # Check for a winner
            if ((board[clicked_row][0] == board[clicked_row][1] == board[clicked_row][2] == current_player) or
                    (board[0][clicked_col] == board[1][clicked_col] == board[2][clicked_col] == current_player) or
                    (board[0][0] == board[1][1] == board[2][2] == current_player) or
                    (board[0][2] == board[1][1] == board[2][0] == current_player)):
                game_over = True
                winner = current_player
            elif all(board[row][col] != '' for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
                game_over = True

            # Switch player
            if current_player == 'X':
                current_player = 'O'
            else:
                current_player = 'X'

        state_representation = get_state_representation(board)

        # Draw the game board
        window.fill(WHITE)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_x = col * CELL_SIZE
                cell_y = row * CELL_SIZE

                pygame.draw.rect(window, BLACK, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 2)

                if board[row][col] == 'X':
                    pygame.draw.line(window, BLACK, (cell_x + 10, cell_y + 10), (cell_x + CELL_SIZE - 10, cell_y + CELL_SIZE - 10), 2)
                    pygame.draw.line(window, BLACK, (cell_x + CELL_SIZE - 10, cell_y + 10), (cell_x + 10, cell_y + CELL_SIZE - 10), 2)
                elif board[row][col] == 'O':
                    pygame.draw.circle(window, BLACK, (cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 2)

        # Display the winner or a tie message
        if game_over:
            if winner:
                message = f"Player {winner} wins!"
            else:
                message = "It's a tie!"
            text = pygame.font.Font(None, 40).render(message, True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            window.blit(text, text_rect)
            print(f'{state_representation}')
            print(f'{board}')
            running = False
        # Update the display
        pygame.display.update()

        if is_current_player_bot:
            pygame.time.wait(1000)


    # Quit Pygame
    pygame.time.wait(5000)
    pygame.quit()

if __name__ == "__main__":
    main()