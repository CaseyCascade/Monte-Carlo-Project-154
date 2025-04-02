
# "\033[31m\u2022\033[0m " # Red Bullet
# "\033[32m\u2022\033[0m" # Green Bullet

class Grid:
    def __init__(self, size):
        self.cols = size 
        self.rows = size 
        self.grid = [["- " for _ in range(self.cols)] for _ in range(self.rows)]

    def print(self):
        for row in self.grid:
            line = ''.join(row)
            print(line)
            

def main():
    new_grid = Grid(10)
    new_grid.print()
    

if __name__ == "__main__":
    main()