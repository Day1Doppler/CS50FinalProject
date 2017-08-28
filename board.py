class Board():
    """Implements connect four board"""

    def __init__(self, width, height):
        """Initialize Board"""

        self.width = width
        self.height = height

        # initialize empty board
        self.grid = [[0 for x in range(height)] for y in range(width)]

        # remember whose turn it is (1 for 1st player, -1 for 2nd player)
        self.turn = 1

        # move counter - note that we could fold self.turn into this if we wanted with mc % 2
        self.move_counter = 0

    # print board state
    def draw(self):

        # function to map stored values to print outputs
        def shape_map(n):
            # 1st player's move
            if n == 1:
                # red block
                return("\u001b[41m__\u001b[0m")
            elif n == -1:
                # green block
                return("\u001b[42m__\u001b[0m")
            else:
                # black block
                return("\u001b[40m__\u001b[0m")

        # ascii art
        for i in range(self.height):
            # left column
            print("|", end="")
            for j in range(self.width):
                print(shape_map(self.grid[j][self.height - (i + 1)]), end="\u001b[40m|\u001b[0m")
            print("")
        print("\n")


    # moves based on column indicated
    def move(self,col):
        """Move based on user input"""

        # check column supplied is valid
        try:
            col_int = int(col)

        except ValueError:
            print("Not an integer.")
            # stop function execution
            return

        if col_int not in range(self.width):
            print("Value not in range.")
            # stop function execution
            return

        # check if row is full
        if self.grid[col_int][self.height - 1] != 0:
            # tell player
            print("Row is already full.")

        else:
            # insert value into first non-empty row
            for i in range(self.height):

                # insert player value into first empty row
                if self.grid[col_int][i] == 0:
                    self.grid[col_int][i] = self.turn

                    # change who's turn it is
                    self.turn = -self.turn

                    # increment move counter
                    self.move_counter += 1

                    # stop executing
                    break


    def status(self):
        """Check is if position is won for a player"""
        # Note this could be done more efficiently by storing the most recent move and checking relative to that move only
        # Keeping it general in case we want to use this class to evaluate positions where we don't know the last move in future

        #check if horizontal win:
        for i in range(self.width-3):
            # iterate over all rows
            for j in range(self.height):
                # test if leftmost part of horizontal win
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i+1][j] and self.grid[i][j] == self.grid[i+2][j] and self.grid[i][j] == self.grid[i+3][j]:
                    return "won"

        #check if vertical win:
        for i in range(self.width):
            # iterate over rows
            for j in range(self.height-3):
                # test if leftmost part of horizontal win
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i][j+1] and self.grid[i][j] == self.grid[i][j+2] and self.grid[i][j] == self.grid[i][j+3]:
                    return "won"

        #check if top-left to bot-right diag win:
        for i in range(self.width-3):
            # iterate over rows
            for j in range(self.height-3):
                # test if leftmost part of horizontal win
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i+1][j+1] and self.grid[i][j] == self.grid[i+2][j+2] and self.grid[i][j] == self.grid[i+3][j+3]:
                    return "won"

        #check if top-left to bot-right diag win:
        for i in range(self.width-3):
            # iterate over rows
            for j in range(self.height-3):
                # test if leftmost part of horizontal win
                if self.grid[i][j+3] != 0 and self.grid[i][j+3] == self.grid[i+1][j+2] and self.grid[i][j+3] == self.grid[i+2][j+1] and self.grid[i][j+3] == self.grid[i+3][j]:
                    return "won"

        # if not won and board is full, game is drawn
        if self.move_counter >= self.width * self.height:
            return "drawn"

        # else not over
        return "in progress"

    def summarize(self):
        """ Gives summary info on game state"""

        def turn_map(n):
            if self.turn == 1:
                return "Red"
            elif self.turn == -1:
                return "Green"
            else:
                return "INVALID TURN"

        print("It is move {}. It is {}'s turn to play. The current status of the game is: {}.\n\n".format(self.move_counter, turn_map(self.turn), self.status()))









