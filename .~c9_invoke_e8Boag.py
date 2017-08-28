class Board():
    """Implements connect four board"""

    # TODO - move to init variable




    def __init__(self, width, height):
        """Initialize Board."""

        # board constants - TODO check style guide (CAPS?)
        self.width = width
        self.height = height

        # initialize empty board
        self.grid = [[0 for x in range(height)] for y in range(width)]

        # remember whose turn it is - TODO make more elegant
        self.turn = 0



    # print board state TODO - comment about storing and transposing for printing, use zip for elegance
    def draw(self):
        """Print board to console."""
        for row in reverstuple(zip(self.grid)):
        print(self.grid)

        print("maps to:")

        for row in range(self.height):
            for col in self.grid:
                print(col[self.height - row - 1], end="")
                print(" ", end="")
            print("")

    # moves based on column indicated
    def move(self,col):
        self.grid[1][0] = 1

    def is_legal(self,move):
        return true

    def




