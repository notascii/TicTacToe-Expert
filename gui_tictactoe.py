import tkinter as tk
from game import Game
import json

class Application(object):
    def __init__(self, w, h):
        self.geometry = {"width":w, "heigth":h}
        self.gapx = 25
        self.gapy = 25
        self.pawns = {"white":[], "yellow":[], "black":[]}
        self.end_images = []
        self.buttons = []
        self.pawns_theme = "white" # A CHANGER ENTRE DANS LA LISTE DE COULEURS POSSIBLES
        self.themes = {"black":"white", "white":"black"}

    ####################
    # CREATE FUNCTIONS #
    ####################

    def create_root(self, w, h):
        """Créé la fenêtre principale root de dimensions (w,h) non redimensionnable et la retourne."""

        self.root = tk.Tk()
        self.root.title("TicTacToe Expert")
        self.root.configure(background=self.themes[self.pawns_theme])
        self.root.geometry(f"{w}x{h}")
        self.root.resizable(0, 0)
    
    def create_frame_and_canvas(self):
        """utils"""

        self.topframe = tk.Frame(self.root)
        self.topframe.pack()

        self.canvasGrid = tk.Canvas(self.topframe, height=500, width=500, bg=self.themes[self.pawns_theme], highlightthickness=0)
        self.canvasGrid.pack()

    def create_pawns_images(self):
        """utils"""

        for couleur in ["white", "yellow", "black"]:
            for symbol in ["croix", "rond"]:
                for taille in ["petit", "grand"]:
                    self.pawns[couleur].append(tk.PhotoImage(file=f"images/{symbol}_{taille}_{couleur}.png"))
    
    def create_end_images(self):
        """utils"""

        self.end_images.append(tk.PhotoImage(file="images/end_croix_win.png"))
        self.end_images.append(tk.PhotoImage(file="images/end_rond_win.png"))


    def display_menu_buttons(self):
        """Affiche les boutons du menu sur root."""

        global buttonPlayImage, buttonPlay, buttonLoad, buttonLoadImage, buttonRules, buttonRulesImage, buttonQuitImage, buttonQuit

        buttonPlayImage = tk.PhotoImage(file="images/buttonPlay.png")
        buttonPlay = tk.Button(self.root, image=buttonPlayImage, relief="flat", command=self.play)
        pack_button(buttonPlay)
        self.buttons.append(buttonPlay)

        buttonLoadImage = tk.PhotoImage(file="images/buttonLoad.png")
        buttonLoad = tk.Button(self.root, image=buttonLoadImage, relief="flat", command=self.load_game)
        pack_button(buttonLoad)
        self.buttons.append(buttonLoad)

        buttonRulesImage = tk.PhotoImage(file="images/buttonRules.png")
        buttonRules = tk.Button(self.root, image=buttonRulesImage, relief="flat", command=self.rules)
        pack_button(buttonRules)
        self.buttons.append(buttonRules)

        """ PAS LE TEMPS DE REMETTRE EN ETAT
        buttonParameters = tk.Button(self.root, relief="flat", text="Paramètres", command=self.parameters)
        pack_button(buttonParameters)
        self.buttons.append(buttonParameters)
        """

        buttonQuitImage = tk.PhotoImage(file="images/buttonQuit.png")
        buttonQuit = tk.Button(self.root, image=buttonQuitImage, relief="flat", command=self.root.destroy)
        pack_button(buttonQuit)
        self.buttons.append(buttonQuit)

    ##########################
    # MENU BUTTONS FUNCTIONS #
    ##########################

    def play(self):
        """Cette fonction s'éxécute lorsque l'on clique sur le bouton Play.
        Elle cache les boutons, créé le canvas, affiche la grille sur le canvas
        et associe le clic gauche de la souris à la fonction clic."""

        global smallButtonSaveImage, smallButtonReplayImage, smallButtonQuitImage

        self.create_frame_and_canvas()
        self.create_pawns_images()
        self.create_end_images()

        # define gapx and gapy issou

        hide_menu_buttons()

        self.display_grid()
        self.draw_all_pawns()

        # associe le bouton clic gauche à la fonction clic
        self.root.bind("<Button 1>", clic)

        # créé les boutons accessibles pendant la phase de jeu
        self.bottom_frame = tk.Frame()
        self.bottom_frame.pack(side=tk.BOTTOM)

        smallButtonSaveImage = tk.PhotoImage(file="images/buttonSave_small.png")
        small_button_save = tk.Button(self.bottom_frame, image=smallButtonSaveImage, relief="flat", command=self.save)
        small_button_save.pack(side=tk.LEFT)

        smallButtonReplayImage = tk.PhotoImage(file="images/buttonReplay_small.png")
        small_button_replay = tk.Button(self.bottom_frame, image=smallButtonReplayImage, relief="flat", command=self.replay)
        small_button_replay.pack(side=tk.LEFT)
        
        smallButtonQuitImage = tk.PhotoImage(file="images/buttonQuit_small.png")
        small_button_quit = tk.Button(self.bottom_frame, image=smallButtonQuitImage, relief="flat", command=self.root.destroy)
        small_button_quit.pack(side=tk.LEFT)
    
    def load_game(self):
        """Charge la partie."""

        savefile = open("save_tictactoe.json", "r")
        data = json.load(savefile)
        savefile.close()

        game.grid = data["grid"]
        game.subgrids = data["subgrids"]
        game.n = int(data["n"])
        game.pre_n = int(data["pre_n"])
        game.pre_l = int(data["pre_l"])
        game.pre_c = int(data["pre_c"])

        self.play()
    
    def rules(self):
        """Cette fonction s'éxécute lorsque l'on clique sur le bouton Règles."""

        global rulesImage

        def local_return_to_menu():
            self.canvas_for_rules.delete("all")
            self.canvas_for_rules.pack_forget()
            returnButton.pack_forget()
            self.display_menu_buttons()

        hide_menu_buttons()

        self.canvas_for_rules = tk.Canvas(self.root, width=500, height=500, bg="black", highlightthickness=0)
        self.canvas_for_rules.pack()

        rulesImage = tk.PhotoImage(file="images/regles.png")
        self.canvas_for_rules.create_image(250, 275, image=rulesImage)

        returnButton = tk.Button(self.root, text="Retour", command=local_return_to_menu)
        returnButton.pack()
    
    """ PAS LE TEMPS DE LA REMETTRE EN ETAT
    def parameters(self):
        # Cette fonction s'éxécute lorsque l'on clique sur le bouton Paramètres.

        def local_return_to_menu():
            returnButton.pack_forget()
            black_pawns_button.pack_forget()
            white_pawns_button.pack_forget()
            b1.pack_forget()
            self.display_menu_buttons()

        hide_menu_buttons()

        black_pawns_button = tk.Button(self.root, text="Noir", command=lambda: self.change_color("black"))
        black_pawns_button.pack()

        white_pawns_button = tk.Button(self.root, text="Blanc", command=lambda: self.change_color("white"))
        white_pawns_button.pack()

        returnButton = tk.Button(self.root, text="Retour", command=local_return_to_menu)
        returnButton.pack(side=tk.BOTTOM)
    """
   
    def change_color(self, color):
        """utils"""
        self.pawns_theme = color

    def replay(self):
        """Reset la partie, nettoie le canvas, redisplay la grille de jeu et
        rebind le bouton-1 de la souris à la fonction clic."""

        game.reset()
        self.canvasGrid.delete("all")
        self.display_grid()
        self.root.bind("<Button 1>", clic)

        if game.is_subgrid_win_or_full(game.n):
            # on colorie tous contours possible
            for subgrid_nb in range(1,10):
                if not game.is_subgrid_win_or_full(subgrid_nb):
                    app.draw_outline(subgrid_nb, "red", 3)
        else:
            app.draw_outline(game.n, "red", 3)


    def end(self):
        """Affiche un message lorsque la partie a été gagnée et unbind le bouton-1
        de la souris."""

        if game.is_grid_win("x"):
            self.canvasGrid.create_image(250, 250, image=app.end_images[0])
        if game.is_grid_win("o"):
            self.canvasGrid.create_image(250, 250, image=app.end_images[1])

        self.root.unbind("<Button-1>")

    def save(self):
        """Sauvegarde la partie dans le fichier save_tictactoe.json"""

        for symbol in ["x", "o"]:
            if game.is_grid_win(symbol):
                print("Vous ne pouvez pas sauvegarder une partie déjà gagnée.")
                return -1

        savefile = open("save_tictactoe.json", "r")
        data = json.load(savefile)
        savefile.close()

        data["grid"] = game.grid
        data["subgrids"] = game.subgrids
        data["n"] = str(game.n)
        data["pre_n"] = str(game.pre_n)
        data["pre_l"] = str(game.pre_l)
        data["pre_c"] = str(game.pre_c)

        savefile = open("save_tictactoe.json", "w")
        json.dump(data, savefile, indent=4)
        savefile.close()


    ############################
    # DRAW ON CANVAS FUNCTIONS #
    ############################

    def draw_pawn_on_canvas(self, xmoy, ymoy, player, color):
        """Dessine un pion du joueur sur le canvas aux coordonnées (xmoy, ymoy)."""

        if color == None:
            color = self.pawns_theme

        if player:
            # joueur o
            # canvas.create_oval(xmoy-20, ymoy-20, xmoy+20, ymoy+20, outline="white", width=4)
            self.canvasGrid.create_image(xmoy, ymoy, image=self.pawns[color][2])
        else:
            # joueur x
            # canvas.create_line(xmoy-20, ymoy-20, xmoy+20, ymoy+20, fill="white", width=4)
            # canvas.create_line(xmoy-20, ymoy+20, xmoy+20, ymoy-20, fill="white", width=4)
            self.canvasGrid.create_image(xmoy, ymoy, image=self.pawns[color][0])

    def draw_big_pawn_on_canvas(self, n, player, color):
        """Dessine un grand pion sur le canvas sur la sous-grille numéro n."""
        
        # calcule (xc,yc) les coordonnées du centre de la sous-grille
        xc = 150*((n - 1) % 3) + 75 + self.gapx
        yc = 150*((n - 1) // 3) + 75 + self.gapy

        if player:
            # canvas.create_oval(xc-60, yc-60, xc+60, yc+60, outline="white", width=10)
            self.canvasGrid.create_image(xc, yc, image=self.pawns[color][3])
        else:
            # canvas.create_line(xc-60, yc-60, xc+60, yc+60, fill="white", width=10)
            # canvas.create_line(xc-60, yc+60, xc+60, yc-60, fill="white", width=10)
            self.canvasGrid.create_image(xc, yc, image=self.pawns[color][1])
    
    def draw_all_pawns(self):
        """Dessine l'état de la partie actuelle."""

        game.player = 0
        for n in range(1, 10):
            for l in range(0, 3):
                for c in range(0, 3):
                    i, j = convert_nlc_to_ij(n, l, c)
                    x = 50*j + 25 + app.gapx
                    y = 50*i + 25 + app.gapy

                    if game.subgrids[str(n)][3*l + c] == "x":
                        self.draw_pawn_on_canvas(x, y, 0, None)
                        game.player = (game.player + 1)%2
                    if game.subgrids[str(n)][3*l + c] == "o":
                        self.draw_pawn_on_canvas(x, y, 1, None)
                        game.player = (game.player + 1)%2

        game.player = (game.player + 1)%2
        i, j = convert_nlc_to_ij(game.pre_n, game.pre_l, game.pre_c)
        x = 50*(j - 1) + 25 + app.gapx
        y = 50*(i - 1) + 25 + app.gapy
        self.draw_pawn_on_canvas(x, y, game.player, "yellow")
        game.player = (game.player + 1)%2

        for n in range(0, 9):
            if game.grid[n] == "x":
                self.draw_big_pawn_on_canvas(n + 1, 0, app.pawns_theme)
            if game.grid[n] == "o":
                self.draw_big_pawn_on_canvas(n + 1, 1, app.pawns_theme)
        
        if game.is_subgrid_win_or_full(game.n):
            # on colorie tous contours possible
            for subgrid_nb in range(1,10):
                if not game.is_subgrid_win_or_full(subgrid_nb):
                    app.draw_outline(subgrid_nb, "red", 3)
        else:
            app.draw_outline(game.n, "red", 3)


    def draw_outline(self, n, color, width):
        """Repasse le contour d'une sous-grille."""

        if n == 1:
            x, y = 0, 0
        else:
            x = ((n - 1)%3)*150
            y = ((n - 1)//3)*150

        self.canvasGrid.create_rectangle(x + self.gapx + 3, y + self.gapx + 3, x + 150 + self.gapy - 3, y + 150 + self.gapy - 3, outline=color, width=width)
    
    def clear_outline(self):
        """Repasse le contour de toutes les sous-grilles."""
        
        for i in range(1,10):
            self.draw_outline(i, self.pawns_theme, 3)

    def display_grid(self):
        """Affiche la grille sur le canvas. Laisse un peu de place dans le coin supérieur
        gauche, en fonction des variables gapx et gapy."""

        gapx, gapy = self.gapx, self.gapy

        for i in range(10): # lignes fines
            self.canvasGrid.create_line(gapx, 50*i + gapy, 450 + gapx, 50*i + gapy, fill=self.pawns_theme) # lignes horizontales
            self.canvasGrid.create_line(50*i + gapx, gapy, 50*i + gapx, 450 + gapy, fill=self.pawns_theme) # lignes verticales

        for i in range(4): # lignes épaisses
            self.canvasGrid.create_line(gapx - 4, 150*i+gapy, 450+gapx + 5, 150*i+gapy, width=9, fill=self.pawns_theme) # lignes horizontales
            self.canvasGrid.create_line(150*i+gapx, gapy, 150*i+gapx, 450+gapy, width=9, fill=self.pawns_theme) # lignes verticales

    def is_clic_in_canvas(self, x, y):
        """utils"""
        if not ((self.gapx <= x <= self.gapx + 450) and (self.gapy <= y <= self.gapy + 450)):
            # le clic n'est pas dans le canvas
            return False
        return True


############################
# MANAGE BUTTONS FUNCTIONS #
############################

def hide_menu_buttons():
    """Cache les boutons Play, Rules, Parameters et Quit."""

    hide_button(buttonPlay)
    hide_button(buttonLoad)
    hide_button(buttonRules)
    #hide_button(buttonParameters)
    hide_button(buttonQuit)

def hide_button(button):
    """Cache le bouton passé en argument en appliquant la méthode pack_forget."""

    button.pack_forget()

def pack_button(button):
    """pack le bouton passé en argument avec l'option tk.TOP et en l'étirant en plus."""

    button.pack(side=tk.TOP, expand=True)


def get_grid_position(x, y):
    """utils"""

    return ((x - 25) // 50, (y - 25) // 50)

def convert_ij_to_nlc(i, j):
    """utils"""

    case_number = 9*j + i + 1 # numéro de la case : de 1 à 81.
    n = 3*(j // 3) + i // 3 + 1

    # calculate c (column)
    c = (case_number % 9) % 3
    if (c == 0):
        c += 3

    # calculate l (line)
    if (case_number % 9 == 0):
        case_number -= 1
    l = (case_number % 27) // 9 + 1
    
    return (n, l, c)

def convert_nlc_to_ij(n, l, c):
    """utils"""

    i = ((n - 1)//3)*3 + l
    j = ((n - 1)%3)*3 + c
    return (i, j)

def is_subgrid_or_grid_win(n, symbol, color):
    """Si quelque chose a été écrit dans l'une des sous-grilles, on vérifie si la
    sous-grille a été remportée. Si c'est le cas on dessine un gros pion sur cette sous-grille
    et on vérifie si le joueur a gagnée la partie."""

    key = str(n)
    if game.is_subgrid_win(key, symbol):
    # si c'est le cas on dessine un gros pion et nous l'écrivons dans grille
        app.draw_big_pawn_on_canvas(n, game.player, color)
        game.grid_place(n - 1, symbol)
    
        if game.is_grid_win(symbol):
            game.end = True

def update_l_and_c(game, l, c):
    """utils"""
    game.pre_l = l
    game.pre_c = c

def clic(event):

    is_ia = False

    if not app.is_clic_in_canvas(event.x, event.y):
        return -1

    # calcule les coordonnées du centre de la "case cliquée"
    xmoy = ((event.x - app.gapx) // 50) * 50 + 25 + app.gapx
    ymoy = ((event.y - app.gapy) // 50) * 50 + 25 + app.gapy

    # quel symbole joue ?
    symbol = game.players[game.player]

    i, j = get_grid_position(xmoy, ymoy) # avoir (i,j) les coordonnées dans la grille 9x9 
    n, l, c = convert_ij_to_nlc(i, j) # les convertir dans le format (numéro de sous-grille,ligne,colonne)
    key = str(n)

    # détermine si le joueur peut poser un pion là où il a cliqué
    if game.is_possible(n, l, c):
        app.clear_outline()
        app.draw_pawn_on_canvas(xmoy, ymoy, game.player, "yellow")
        game.subgrid_place(n, l, c, symbol)

        # un joueur a posé un pion, on vérifie s'il a remporté la sous-grille
        # et s'il l'a remporté on vérifie s'il a remporté la grille
        is_subgrid_or_grid_win(n, symbol, app.pawns_theme)

        # si un coup a déjà été jouée, on dessine par dessus le dernier coup
        # en blanc pour effacer le pion jaune.
        if not (game.pre_l == 0) and not (game.pre_c == 0):
            pre_i, pre_j = convert_nlc_to_ij(game.pre_n, game.pre_l, game.pre_c)
            pre_x = 50*(pre_j - 1) + 25 + app.gapx
            pre_y = 50*(pre_i - 1) + 25 + app.gapy
            app.draw_pawn_on_canvas(pre_x, pre_y, (game.player+1)%2, app.pawns_theme)

        game.player = (game.player + 1)%2
        game.pre_n = n
        game.n = 3*(l - 1) + c

        update_l_and_c(game, l , c)

        if game.is_subgrid_win_or_full(game.n):
            # on colorie tous contours possible
            for subgrid_nb in range(1,10):
                if not game.is_subgrid_win_or_full(subgrid_nb):
                    app.draw_outline(subgrid_nb, "red", 3)
        else:
            app.draw_outline(game.n, "red", 3)
        
        if game.end:
            app.end()


if __name__ == "__main__":

    app = Application(500, 550)
    game = Game()

    app.create_root(app.geometry["width"], app.geometry["heigth"])

    app.display_menu_buttons()

    app.root.mainloop()