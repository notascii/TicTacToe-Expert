import tkinter as tk
from game import Game
import ia


class Application(object):
    def __init__(self, w, h):
        self.geometry = {"width":w, "heigth":h}
        self.gapx = 25
        self.gapy = 25
        self.pawns = {"white":[], "yellow":[], "black":[]}
        self.end_images = []
        self.buttons = []
        self.pawns_theme = ""

    ####################
    # CREATE FUNCTIONS #
    ####################

    def create_root(self, w, h):
        """Créé la fenêtre principale root de dimensions (w,h) non redimensionnable et la retourne."""

        self.root = tk.Tk()
        self.root.title("TicTacToe Expert")
        self.root.configure(background="black")
        self.root.geometry(f"{w}x{h}")
        self.root.resizable(0, 0)
    
    def create_frame_and_canvas(self):
        """ """

        self.topframe = tk.Frame(root)
        self.topframe.pack()

        self.canvasGrid = tk.Canvas(self.topframe, height=500, width=500, bg="blue", highlightthickness=0)
        self.canvasGrid.pack()

    def create_pawns(self):
        """ """

        for couleur in ["white", "yellow", "black"]:
            for symbol in ["croix", "rond"]:
                for taille in ["petit", "grand"]:
                    self.pawns[couleur].append(tk.PhotoImage(file=f"images/{symbol}_{taille}_{couleur}.png"))
    
    def create_end_images(self):
        """ """

        self.end_images.append(tk.PhotoImage(file="images/end_croix_win.png"))


    def display_menu_buttons(self):
        """Affiche les boutons du menu sur root."""

        global buttonPlayImage, buttonPlay, buttonQuitImage, buttonQuit, buttonRules, buttonParameters

        buttonPlayImage = tk.PhotoImage(file="images/buttonPlay.png")
        buttonPlay = tk.Button(self.root, image=buttonPlayImage, relief="flat", command=self.play)
        pack_button(buttonPlay)
        self.buttons.append(buttonPlay)

        buttonRules = tk.Button(self.root, relief="flat", text="Règles")
        pack_button(buttonRules)
        self.buttons.append(buttonRules)

        buttonParameters = tk.Button(self.root, relief="flat", text="Paramètres", command=self.parameters)
        pack_button(buttonParameters)
        self.buttons.append(buttonParameters)

        buttonQuitImage = tk.PhotoImage(file="images/buttonQuit.png")
        buttonQuit = tk.Button(self.root, image=buttonQuitImage, relief="flat", command=self.root.destroy)
        pack_button(buttonQuit)
        self.buttons.append(buttonQuit)

    def play(self):
        """Cette fonction s'éxécute lorsque l'on clique sur le bouton Play.
        Elle cache les boutons, créé le canvas, affiche la grille sur le canvas
        et associe le clic gauche de la souris à la fonction clic."""


        self.create_frame_and_canvas()
        self.create_pawns()
        self.create_end_images()

        # define gapx and gapy

        hide_menu_buttons()

        self.display_grid()

        # associe le bouton clic gauche à la fonction clic
        self.root.bind("<Button 1>", clic)

        # créé les boutons accessibles pendant la phase de jeu
        self.bottom_frame = tk.Frame()
        self.bottom_frame.pack(side=tk.BOTTOM)

        smallButtonQuit = tk.Button(self.bottom_frame, image=smallButtonQuitImage, relief="flat", command=self.root.destroy)
        smallButtonQuit.pack(side=tk.LEFT)
        smallButtonReplay = tk.Button(self.bottom_frame, text="Rejouer", relief="flat", command=self.replay)
        smallButtonReplay.pack(side=tk.RIGHT)
    
    def parameters(self):
        """Cette fonction s'éxécute lorsque l'on clique sur le bouton Paramètres."""

        global var

        hide_menu_buttons()

        var = tk.StringVar()

        radioButtonBlack = tk.Radiobutton(self.root, text="Noir", variable=var, value="black")
        radioButtonBlack.pack()

        radioButtonWhite = tk.Radiobutton(self.root, text="Blanc", variable=var, value="white")
        radioButtonWhite.pack()

        b1 = tk.Button(self.root, text="click me", command=self.issou)
        b1.pack()

        self.pawns_theme = var.get()
        print(self.pawns_theme)
        # pb avec stringvar
        # je peux print(var.get())
        # mais je peux pas :
        # a = var.get()
        # print(a)

    def issou(self):
        print(self.pawns_theme)

    def replay(self):
        """ """

        game.reset()
        self.canvasGrid.delete("all")
        self.display_grid()
        self.root.bind("<Button 1>", clic)

    def end(self):
        """ """

        self.canvasGrid.create_image(250, 250, image=app.end_images[0])
        # arrêter le jeu

        self.root.unbind("<Button-1>")


    ############################
    # DRAW ON CANVAS FUNCTIONS #
    ############################

    def draw_pawn_on_canvas(self, xmoy, ymoy, player, color):
        """Dessine un pion du joueur sur le canvas aux coordonnées (xmoy, ymoy)."""

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

    def draw_outline(self, n, color, width):
        """ """

        if n == 1:
            x, y = 0, 0
        else:
            x = ((n - 1)%3)*150
            y = ((n - 1)//3)*150

        self.canvasGrid.create_rectangle(x + self.gapx + 3, y + self.gapx + 3, x + 150 + self.gapy - 3, y + 150 + self.gapy - 3, outline=color, width=width)
    
    def clear_outline(self):
        """ """
        
        for i in range(1,10):
            self.draw_outline(i, "white", 3)

    def display_grid(self):
        """Affiche la grille sur le canvas. Laisse un peu de place dans le coin supérieur
        gauche, en fonction des variables gapx et gapy."""

        gapx, gapy = self.gapx, self.gapy

        for i in range(10): # lignes fines
            self.canvasGrid.create_line(gapx, 50*i + gapy, 450 + gapx, 50*i + gapy, fill="white") # lignes horizontales
            self.canvasGrid.create_line(50*i + gapx, gapy, 50*i + gapx, 450 + gapy, fill="white") # lignes verticales

        for i in range(4): # lignes épaisses
            self.canvasGrid.create_line(gapx, 150*i+gapy, 450+gapx, 150*i+gapy, width=9, fill="white") # lignes horizontales
            self.canvasGrid.create_line(150*i+gapx, gapy, 150*i+gapx, 450+gapy, width=9, fill="white") # lignes verticales

    def is_clic_in_canvas(self, x, y):
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
    hide_button(buttonRules)
    hide_button(buttonParameters)
    hide_button(buttonQuit)

def hide_button(button):
    """Cache le bouton passé en argument en appliquant la méthode pack_forget."""

    button.pack_forget()

def pack_button(button):
    """pack le bouton passé en argument avec l'option tk.TOP et en l'étirant en plus."""

    button.pack(side=tk.TOP, expand=True)


def get_grid_position(x, y):
    return ((x - 25) // 50, (y - 25) // 50)

def convert_ij_to_nlc(i, j):
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

    # print(f"A pre={game.pre_n} actuel={game.n} ({game.pre_l},{game.pre_c})")

    # détermine si le joueur peut poser un pion là où il a cliqué
    if game.is_possible(n, l, c):
        app.clear_outline()
        app.draw_pawn_on_canvas(xmoy, ymoy, game.player, "yellow")
        game.subgrid_place(n, l, c, symbol)

        # un joueur a posé un pion, on vérifie s'il a remporté la sous-grille
        # et s'il l'a remporté on vérifie s'il a remporté la grille
        is_subgrid_or_grid_win(n, symbol, app.pawns_theme)

        if not (game.pre_l == 0) and not (game.pre_c == 0):
            pre_i, pre_j = convert_nlc_to_ij(game.pre_n, game.pre_l, game.pre_c)
            pre_x = 50*(pre_j - 1) + 25 + app.gapx
            pre_y = 50*(pre_i - 1) + 25 + app.gapy
            # print(f"(i,j)=({pre_i},{pre_j}), (x,y)=({pre_x},{pre_y})\n")
            app.draw_pawn_on_canvas(pre_x, pre_y, (game.player+1)%2, app.pawns_theme)

        game.player = (game.player + 1)%2
        game.pre_n = n
        game.n = 3*(l - 1) + c

        update_l_and_c(game, l , c)

        if game.is_subgrid_win_or_full(game.n):
            # on colorie tous contours possible en vert
            for subgrid_nb in range(1,10):
                if not game.is_subgrid_win_or_full(subgrid_nb):
                    app.draw_outline(subgrid_nb, "red", 3)
        else:
            app.draw_outline(game.n, "red", 3)
        
        if game.end:
            app.end()

        # print(f"B pre={game.pre_n} actuel={game.n} ({game.pre_l},{game.pre_c})\n")



        #####   #####
          #     #   #
          #     #####
          #     #   #
        #####   #   #

        if game.player == 1 and is_ia == True: # joueur rond = IA
            
            if not (game.pre_l == 0) and not (game.pre_c == 0):
                pre_i, pre_j = convert_nlc_to_ij(game.pre_n, game.pre_l, game.pre_c)
                pre_x = 50*(pre_j - 1) + 25 + gapx
                pre_y = 50*(pre_i - 1) + 25 + gapy
                # print(f"(i,j)=({pre_i},{pre_j}), (x,y)=({pre_x},{pre_y})\n")
                app.draw_pawn_on_canvas(pre_x, pre_y, (game.player+1)%2, app.pawns_theme)

            game.n, l_ia, c_ia = ia.best_move(game, scores) # où joue l'ia ?
            i_ia, j_ia = convert_nlc_to_ij(game.n, l_ia, c_ia)
            x_ia = 50*(j_ia - 1) + 25 + gapx
            y_ia = 50*(i_ia - 1) + 25 + gapy

            """print(f"l_ia = {l_ia}, c_ia = {c_ia}")
            print(f"game.n = {game.n} | n = {n}")
            print("symbol =", symbol)
            print(x_ia, y_ia)"""

            app.clear_outline()
            app.draw_pawn_on_canvas(x_ia, y_ia, game.player, "white")
            print("symbol =", symbol)
            game.subgrid_place(game.n, l_ia, c_ia, symbol)

            is_subgrid_or_grid_win(n, "o", app.pawns_theme)
            if game.is_subgrid_full(n):
                print(f"La grille {n} est pleine.")
            
            # game.player vaut 1 mais je mets tjrs des croix
            # dans game.subgrids
            game.player = (game.player + 1)%2
            game.pre_n = game.n
            game.n = 3*(l_ia - 1) + c_ia

            update_l_and_c(game, l_ia , c_ia)

            if game.is_subgrid_win_or_full(game.n):
                # on colorie tous contours possible en vert
                for subgrid_nb in range(1,10):
                    if not game.is_subgrid_win_or_full(subgrid_nb):
                        app.draw_outline(subgrid_nb, "red", 3)
            else:
                app.draw_outline(game.n, "red", 3)
            
        # print(game.subgrids)


if __name__ == "__main__":

    app = Application(500, 550)
    game = Game()

    app.pawns_theme = "white"
    scores = ia.Scores()

    root = app.create_root(app.geometry["width"], app.geometry["heigth"])
  
    smallButtonQuitImage = tk.PhotoImage(file="images/buttonQuit_small.png")

    app.display_menu_buttons()

    app.root.mainloop()