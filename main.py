#
#   Coding Test Done by David Villaba for A Mobile Company
#   dvillaba@protonmail.com
#   www.davidvillaba.net
#

# Flask for web server
from flask import Flask
from flask import request
# re for regular expressions
import re

app = Flask(__name__, instance_path="/{project_folder_abs_path}/instance")


# Class that represents all the movements until the game endeed
class GamePath:
    def __init__(self):
        self.paths = list()
        self.end = ''


# Class that calculates all the possible paths that a game can have, is used for David's solution
class AllPathsCalculator:

    def __init__(self):
        self.GamePaths = list()

    # this method determines if the game has ended, and how has ended.
    # Possible returns:
    # o: o wins
    # x: x wins
    # d: draw
    # ?: game not ended
    def GameFinished(self, pBoard):
        reOWins1 = 'ooo......'
        reOWins2 = '...ooo...'
        reOWins3 = '......ooo'
        reOWins4 = 'o..o..o..'
        reOWins5 = '.o..o..o.'
        reOWins6 = '..o..o..o'
        reOWins7 = 'o...o...o'
        reOWins8 = '..o.o.o..'
        generic_re = re.compile("(%s|%s|%s|%s|%s|%s|%s|%s)" % (
        reOWins1, reOWins2, reOWins3, reOWins4, reOWins5, reOWins6, reOWins7, reOWins8)).findall(pBoard)
        if generic_re:
            return 'o'  # o wins
        else:
            reXWins1 = 'xxx......'
            reXWins2 = '...xxx...'
            reXWins3 = '......xxx'
            reXWins4 = 'x..x..x..'
            reXWins5 = '.x..x..x.'
            reXWins6 = '..x..x..x'
            reXWins7 = 'x...x...x'
            reXWins8 = '..x.x.x..'
            generic_re = re.compile("(%s|%s|%s|%s|%s|%s|%s|%s)" % (
            reXWins1, reXWins2, reXWins3, reXWins4, reXWins5, reXWins6, reXWins7, reXWins8)).findall(pBoard)
            if generic_re:
                return 'x'  # x wins
            elif ' ' not in pBoard:
                return 'd'  # draw
            else:
                return '?'  # "game not finished"

    # Method that makes multiple game paths doing movements
    def Move(self, pBoard, pGamePath, pPlayer):
        i = 0
        t = len(pBoard)
        while i < t:
            if pBoard[i] == ' ':
                vNewGamePath = GamePath()
                vNewGamePath.paths = pGamePath.paths.copy()
                vBoardWithMovement = pBoard
                vBoardWithMovement = vBoardWithMovement[:i] + pPlayer + vBoardWithMovement[i + 1:]
                vGameState = self.GameFinished(vBoardWithMovement)
                vNewGamePath.paths.append(vBoardWithMovement)
                if vGameState == "?":
                    if pPlayer == 'o':
                        self.Move(vBoardWithMovement, vNewGamePath, 'x')
                    else:
                        self.Move(vBoardWithMovement, vNewGamePath, 'o')
                elif vGameState == "o":
                    vNewGamePath.end = 'o'
                    self.GamePaths.append(vNewGamePath)
                elif vGameState == "d":
                    vNewGamePath.end = 'd'
                    self.GamePaths.append(vNewGamePath)
                elif vGameState == "x":
                    vNewGamePath.end = 'x'
                    self.GamePaths.append(vNewGamePath)
            i = i + 1


def GetNextMovement(pBoard):
    # empty corner for an empty board
    if pBoard == '         ':
        return 'x        '

    vAllPathsCalculator = AllPathsCalculator()
    vAllPathsCalculator.Move(pBoard, GamePath(), 'o')

    # 1 - Win if two in a row
    vAllPathsWhereOWinsWith1Movement = [x for x in vAllPathsCalculator.GamePaths if x.end == 'o' and len(x.paths) == 1]
    for x in vAllPathsWhereOWinsWith1Movement:
        return x.paths[0]

    # 2 - Block if necessary
    vAllPathsWhereDraw = [x for x in vAllPathsCalculator.GamePaths if x.end == 'x' and len(x.paths) == 2]
    for x in vAllPathsWhereDraw:
        i = 0
        t = len(x.paths[1])
        while i < t:
            if x.paths[1][i] == 'x' and pBoard[i] != 'x':
                return pBoard[:i] + 'o' + pBoard[i + 1:]
            i = i + 1

    # 3 - Fork
    vAllPathsForCalculatingForks = [x for x in vAllPathsCalculator.GamePaths if x.end == 'o' and len(x.paths) == 3]
    vFirstMovementWinFreq = {}
    for x in vAllPathsForCalculatingForks:
        if (x.paths[0] in vFirstMovementWinFreq):
            vFirstMovementWinFreq[x.paths[0]] += 1
        else:
            vFirstMovementWinFreq[x.paths[0]] = 1
    if len(vFirstMovementWinFreq) > 0:
        return max(vFirstMovementWinFreq)

    # 4 - Blocking an opponent's fork
    vAllPathsForCalculatingForksBlock = [x for x in vAllPathsCalculator.GamePaths if x.end == 'x' and len(x.paths) == 4]
    vFirstMovementWinFreqToBlock = {}
    for x in vAllPathsForCalculatingForksBlock:
        if (x.paths[0] in vFirstMovementWinFreqToBlock):
            vFirstMovementWinFreqToBlock[x.paths[0]] += 1
        else:
            vFirstMovementWinFreqToBlock[x.paths[0]] = 1
    if len(vFirstMovementWinFreqToBlock) > 0:
        vMovementToBloq = max(vFirstMovementWinFreqToBlock)
        i = 0
        t = len(vFirstMovementWinFreqToBlock)
        while i < t:
            if max(vFirstMovementWinFreqToBlock)[i] == 'x' and pBoard[i] != 'x':
                return pBoard[:i] + 'o' + pBoard[i + 1:]
            i = i + 1

    # 5 - Center
    if pBoard == '    x    ':
        return 'o   x    '

    # 6 - Opposite corner
    if pBoard == 'x        ':
        return 'x       o'
    elif pBoard == '  x      ':
        return '  x   o  '
    elif pBoard == '      x  ':
        return '  o   x  '
    elif pBoard == '        x':
        return 'o       x'

    # 7 Empty corner
    if pBoard == '         ':
        return 'x        '

    # 8 Empty side
    # TODO - I don't inderstand this  very well...

    # 9 Lower winning path strategy - By David
    vMinPathLenght = 10
    vNextMove = ''
    # Movement for win
    vAllPathsWhereOWins = [x for x in vAllPathsCalculator.GamePaths if x.end == 'o']
    for x in vAllPathsWhereOWins:
        if len(x.paths) < vMinPathLenght:
            vMinPathLenght = len(x.paths)
            vNextMove = x.paths[0]
    if vNextMove != '':
        return vNextMove
    # Movement for draw
    vAllPathsWhereDraw = [x for x in vAllPathsCalculator.GamePaths if x.end == 'd']
    for x in vAllPathsWhereDraw:
        if len(x.paths) < vMinPathLenght:
            vMinPathLenght = len(x.paths)
            vNextMove = x.paths[0]
    if vNextMove != '':
        return vNextMove
    # Movement for lose
    vAllPathsWhereDraw = [x for x in vAllPathsCalculator.GamePaths if x.end == 'x']
    for x in vAllPathsWhereDraw:
        if len(x.paths) < vMinPathLenght:
            vMinPathLenght = len(x.paths)
            vNextMove = x.paths[0]
    if vNextMove != '':
        return vNextMove


@app.route('/')
def TicTacToeDavidVillaba():
    vBoard = request.args.get('board')
    if vBoard is not None:
        # check that the board is valid
        if (len(vBoard) != 9):
            return 'Insert a valid board', 400
        for x in vBoard:
            if x != ' ' and x != 'x' and x != 'o':
                return 'Insert a valid board', 400

        vNumOfX = vBoard.count('x')
        vNumOfO = vBoard.count('o')
        if vNumOfX < vNumOfO:
            return 'Is not the turn of o', 400

        if ((vNumOfX - vNumOfO) != 1) and (vNumOfX + vNumOfO) != 0:
            if ((vNumOfX - vNumOfO) != 0):
                return 'Insert a valid board', 400

        return GetNextMovement(vBoard)
    else:
        return 'Insert a valid boardS', 400


if __name__ == '__main__':
    app.run('localhost', 4449)



