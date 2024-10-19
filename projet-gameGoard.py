class GameBoard:
    def __init__(self, n):
        # Si n n'est pas un multiple de 4, on prend le plus petit multiple de 4 supérieur
        if n % 4 != 0:
            n = (n // 4 + 1) * 4
        self.__n = n  # Taille du plateau de jeu
        self.__board = []
        for _ in range(n):
            row = [0] * n  # Crée une ligne de 'n' zéros
            self.__board.append(row)

        # Initialisation des pions hounds
        for i in range(1, n, 2):
            self.__board[0][i] = (i // 2) + 1  # Pions hounds dans la première ligne, une colonne sur deux

        # Initialisation du pion fox
        self.__board[n - 1][n // 2] = -1  # Pion fox au milieu de la dernière ligne

    def display(self):
        # Affichage du plateau de jeu
        for row in self.__board:
            print(' '.join(['F' if x == -1 else str(x) if x > 0 else '.' for x in row]))
        print()

    def get_value(self, row, col):
        # Récupérer la valeur d'une case
        return self.__board[row][col]

    def set_value(self, row, col, value):
        # Fixer la valeur d'une case
        self.__board[row][col] = value

    def get_size(self):
        # Getter pour récupérer la taille du plateau
        return self.__n


class Hound:
    def __init__(self, row=0, col=0, num=1):  # Ajout du numéro du hound
        self.__row = row
        self.__col = col
        self.__num = num  # Conserver le numéro unique du hound

    def can_move_to(self, board, new_row, new_col):
        # Vérifier si un hound peut se déplacer vers une case donnée
        if 0 <= new_row < board.get_size() and 0 <= new_col < board.get_size():
            if board.get_value(new_row, new_col) == 0:
                # Le mouvement est possible seulement vers le bas et en diagonale
                if (new_row == self.__row + 1) and (new_col == self.__col - 1 or new_col == self.__col + 1):
                    return True
        return False

    def move(self, board):
        while True:
            try:
                new_row = int(input("Which row? ")) - 1
                new_col = int(input("Which column? ")) - 1
                if self.can_move_to(board, new_row, new_col):
                    board.set_value(self.__row, self.__col, 0)  # Libérer l'ancienne case
                    self.__row, self.__col = new_row, new_col
                    board.set_value(self.__row, self.__col, self.__num)  # Garder le même numéro pour le hound
                    break
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Invalid input, please enter integers.")

    def can_move(self, board):
        # Vérifie s'il existe un mouvement possible pour le pion
        return (self.can_move_to(board, self.__row + 1, self.__col - 1) or
                self.can_move_to(board, self.__row + 1, self.__col + 1))


class Fox:
    def __init__(self, row, col):
        self.__row = row
        self.__col = col

    def can_move_to(self, board, new_row, new_col):
        # Le fox peut se déplacer dans toutes les directions diagonales
        if 0 <= new_row < board.get_size() and 0 <= new_col < board.get_size():
            if board.get_value(new_row, new_col) == 0:
                if abs(new_row - self.__row) == 1 and abs(new_col - self.__col) == 1:
                    return True
        return False

    def move(self, board):
        while True:
            try:
                new_row = int(input("Which row? ")) - 1
                new_col = int(input("Which column? ")) - 1
                if self.can_move_to(board, new_row, new_col):
                    board.set_value(self.__row, self.__col, 0)  # Libérer l'ancienne case
                    self.__row, self.__col = new_row, new_col
                    board.set_value(self.__row, self.__col, -1)  # Garder toujours -1 pour le fox
                    break
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Invalid input, please enter integers.")

    def win(self):
        # Le fox gagne s'il atteint la première ligne
        return self.__row == 0


class FoxAndHounds:
    def __init__(self, n=8):
        print("Initialisation du jeu...")
        self.__board = GameBoard(n)  # Création du plateau de jeu
        self.__hounds = [Hound(0, i, (i // 2) + 1) for i in range(1, n, 2)]  # Initialisation des hounds
        self.__fox = Fox(n - 1, n // 2)  # Initialisation du fox
        print("Jeu initialisé avec succès.")

    def play(self):
        turn = 0

        while True:
            # Affichage du plateau de jeu
            self.__board.display()

            if turn % 2 == 0:
                # Tour du fox
                print("Fox to move:")
                self.__fox.move(self.__board)
                if self.__fox.win():
                    print("Fox wins!")
                    break
            else:
                # Tour du hound
                print("Choose a hound:")
                while True:
                    try:
                        hound_id = int(input("Choose a hound: ")) - 1
                        if 0 <= hound_id < len(self.__hounds) and self.__hounds[hound_id].can_move(self.__board):
                            print(f"Hound n°{hound_id + 1} to move:")
                            self.__hounds[hound_id].move(self.__board)
                            break
                        else:
                            print("Invalid hound or no moves available, try again.")
                    except ValueError:
                        print("Invalid input, please enter a number.")

            # Vérification si le fox est bloqué
            hounds_win = True
            for move_row in [-1, 1]:
                for move_col in [-1, 1]:
                    if self.__fox.can_move_to(self.__board, self.__fox._Fox__row + move_row, self.__fox._Fox__col + move_col):
                        hounds_win = False
                        break

            if hounds_win:
                print("Hounds win!")
                break

            turn += 1  # Passer au tour suivant


# Création et lancement du jeu
game = FoxAndHounds()
game.play()
