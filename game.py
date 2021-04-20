class Game(object):
    def __init__(self: object) -> None:
        self.grid = 9*[""]
        self.subgrids = {
            "1":9*[" "], "2":9*[" "], "3":9*[" "],
            "4":9*[" "], "5":9*[" "], "6":9*[" "],
            "7":9*[" "], "8":9*[" "], "9":9*[" "],
        }
        self.players = ["x", "o"]
        self.player = 0
        self.end = False

        # la sous-grille dans laquelle le prochain joueur joue
        self.n = 5

        # précédents n, l et c
        self.pre_n = 0
        self.pre_l = 0
        self.pre_c = 0

    def reset(self: object) -> None:
        self.__init__()

    #################
    # WIN FUNCTIONS #
    #################

    def is_horizontal_win(self: object, key: str, symbol: str) -> bool:
        """Retourne True si le joueur précisé a gagné la sous-grille 
        horizontalement, False sinon."""
        for i in range(0,3):
            if (self.subgrids[key][3*i:3*i + 3] == 3 * list(symbol)):
                return True
        return False

    def is_vertical_win(self: object, key: str, symbol: str) -> bool:
        """Retourne True si le joueur précisé a gagné la sous-grille
        verticalement, False sinon."""
        for i in range(0,3):
            if (self.subgrids[key][i:9:3] == 3 * list(symbol)):
                return True
        return False

    def is_diagonal_win(self: object, key: str, symbol: str) -> bool:
        """Retourne True si le joueur précisé a gagné la sous-grille
        diagonalement, False sinon."""
        if (self.subgrids[key][0:9:4] == 3 * list(symbol) or \
            self.subgrids[key][2:7:2] == 3 * list(symbol)):
            return True
        return False

    def is_subgrid_win(self: object, key: str, symbol: str) -> bool:
        """Retourne True si le joueur précisé a gagné la sous-grille d'une
        quelconque manière, False sinon."""
        if (self.is_horizontal_win(key, symbol) or \
            self.is_vertical_win(key, symbol) or \
            self.is_diagonal_win(key, symbol)):
            return True
        return False

    def is_grid_win(self: object, symbol: str) -> bool:
        """Retourne True si le joueur précisé a gagné la grille, False sinon."""
        s = list(symbol)
        c, l, d = False, False, False
        for i in range(0,3):
            if (self.grid[3*i:3*i+3] == 3*s):
                l = True
            if (self.grid[i:9:3] == 3*s):
                c = True
        if (self.grid[0:9:4] == 3*s or self.grid[2:7:2] == 3*s):
            d = True
        return (c or l or d)



    def is_subgrid_full(self: object, n: int) -> bool:
        """Retourne True si la sous-grille est pleine, False sinon."""
        key = str(n)
        for i in range(9):
            if self.subgrids[key][i] == " ":
                return False
        return True

    def pretty_print_grid(self: object) -> None:
        """Affiche la grille de manière lisible dans le terminal"""

        for grid_row in range(3):
            for subgrid_row in range(3):
                for grid_col in range(3):
                    print("".join(self.subgrids[str(3*grid_row+grid_col)]\
                    [3*subgrid_row:3*subgrid_row+3]), end="")
                    print(["", "|"][grid_col < 2], end="")
                print("")
            print(["", 11*"-"][grid_row < 2])
    
    def is_pawn(self: object, n: int, l: int, c: int) -> bool:
        """Prend le numéro de la sous-grille, la ligne et la colonne dans cette
        sous-grille en entrée. Retourne True s'il y a un pion, False sinon."""

        key = str(n)
        if self.subgrids[key][3*(l - 1) + c - 1] != " ":
            # il y a déjà un symbole
            return True

        return False
    
    def is_right_subgrid(self: object, n: int) -> bool:
        """Retourne True si on joue dans la bonne sous-grille, False sinon."""

        if (n == self.n):
            # on joue dans la bonne sous-grille
            return True

        return False

    def is_subgrid_win_or_full(self: object, n: int) -> bool:
        """Retourne True si la sous-grille dans laquelle on devait jouer a été remporté
        par l'un des deux joueurs ou si la sous-grille est pleine. False sinon."""

        for s in ["x", "o"]:
            if (self.is_subgrid_win(str(n), s)):
                return True

        if (self.is_subgrid_full(n)):
            return True
        
        return False

    def is_possible(self: object, n: int, l: int, c: int) -> bool:
        """Retourne True si le coup est possible, False sinon."""

        if self.is_pawn(n, l, c):
            # il n'y a pas de pion
            return False
        if self.is_right_subgrid(n) and (not self.is_subgrid_win_or_full(n)):
            # on est dans la bonne sous-grille et elle n'est ni gagnée ni pleine
            return True
        if not self.is_right_subgrid(n) and self.is_subgrid_win_or_full(self.n) and \
            not self.is_subgrid_win_or_full(n):
            # la grille dans laquelle on devait jouer est gagnée ou pleine
            # on joue dans une autre sous-grille.
            return True
        return False
    
    def update_n(self: object, l: int, c: int) -> None:
        """Met à jour self.n avec les coordonnées dans la sous-grille du pion
        posé par le joueur."""

        # probleme ici
        self.pre_n = self.n
        self.n = 3*(l - 1) + c

    def subgrid_place(self: object, n: int, l: int, c: int, symbol: str) -> None:
        """Ecrit le symbole dans la sous-grille numéro n, à la ligne l et à la
        colonne c."""

        key = str(n)
        self.subgrids[key][3*(l - 1) + c - 1] = symbol
    
    def grid_place(self: object, n: int, symbol: str) -> None:
        """Ecrit le symbole dans la grille à la case n."""

        key = str(n)
        self.grid[int(key)] += symbol

### MAIN ###
if __name__ == "__main__":
    game = Game()
    
    for i in range(9):
        game.subgrids[str(i)] = [" " if j%2 else game.players[game.player] for j in range(9)]
        game.player = (game.player + 1)%2

    game.pretty_print_grid()