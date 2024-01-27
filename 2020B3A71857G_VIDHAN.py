
from FourConnect import * # See the FourConnect.py file
import csv
#Importing time 
import time 
class GameTreePlayer:
    def __init__(self):
         #keeping track of recursive calls
         self.recursive_calls=0
         pass
    def _CoinRowAfterAction(self,state,action):
        cRow=-1
        for r in range(5,-1,-1):
            if state[r][action]==0:
                cRow=r
                break
        return cRow
   #all evaluative functions are mentioned in the report
    def _eval_simple(self,state):
        player=2
        # if state.winner == player:
        #     return float('inf')
        # if state.winner == 1:
        #     return float('-inf')
        player_count =0
        myopic_count =0
        for row in state.GetCurrentState():
            for cell in row:
                if cell == player:
                    player_count+=1
                elif cell ==1 :
                    myopic_count+=1
        return player_count - myopic_count
    def _center_control_eval(self,state):
        # player=2
        # if state.winner == player:
        #     return float('inf')
        # if state.winner == 1:
        #     return float('-inf')
        center_columns = [state.GetCurrentState()[row][3] for row in range(6)]
        return center_columns.count(2) - center_columns.count(1)
    def _connectivity_evaluation(self,state):
        player=2
        if state.winner == player:
            return float('inf')
        if state.winner == 1:
            return float('-inf')
        game_tree_connected = sum([1 for row in state.GetCurrentState() for col in range(4) if row[col:col+4]==[2]*4])
        myopic_connected = sum([1 for row in state.GetCurrentState() for col in range(4) if row[col:col+4]==[1]*4])
        return game_tree_connected-myopic_connected
    def _threat_eval(self,state):
        # player=2
        # if state.winner == player:
        #     return float('inf')
        # if state.winner == 1:
        #     return float('-inf')
        game_tree_threats = sum([1 for col in range(7) if any(state.GetCurrentState()[row][col]== 2 for row in range(3))])
        myopic_threats = sum([1 for col in range(7) if any(state.GetCurrentState()[row][col]==1 for row in range(3))])
        return game_tree_threats - myopic_threats
    def _defense_eval(self,state):
        # player=2
        # if state.winner == player:
        #     return float('inf')
        # if state.winner == 1:
        #     return float('-inf')
        myopic_defense = sum([1 for col in range(7) if any(state.GetCurrentState()[row][col]==2 for row in range(3,6))])
        game_tree__defense = sum([1 for col in range(7) if any(state.GetCurrentState()[row][col]==1 for row in range(3,6))])
        return game_tree__defense-myopic_defense
    def _final_eval(self,state):
        player=2
        if state.winner == player:
            return float('inf')
        if state.winner == 1:
            return float('-inf')
        return 2*self._eval_simple(state)+5*self._center_control_eval(state)+3*self._connectivity_evaluation(state)+4*self._threat_eval(state)+4*self._defense_eval(state)
    #implementing normal minimax algorithm
    # def _GameTreeSearch_MinMax(self,state,depth,maximizing_player):
    #     if depth ==0 or state.winner is not None:
    #         return self._eval_simple(state)
    #     valid_actions = [action for action in range(7) if self._CoinRowAfterAction(state.GetCurrentState(),action)!=-1]
    #     if maximizing_player:
    #         value = float('-inf')
    #         for act in valid_actions:
    #            new_state = copy.deepcopy(state)
    #            new_state.GameTreePlayerAction(act)
    #            value = max(value,self._GameTreeSearch_MinMax(new_state,depth-1,False))
    #         return value
    #     else:
    #         value = float('inf')
    #         if not valid_actions:
    #             return value
    #         new_state = copy.deepcopy(state)
    #         new_state.MyopicPlayerAction()
    #         value = min(value,self._GameTreeSearch_MinMax(new_state,depth-1,True))
    #     return value
    #IMPLEMENTING ALPHA BETA PRUNING
    # def _GameTreeSearch_prune(self,state,depth,alpha,beta,maximizing_player):
    #     self.recursive_calls+=1
    #     if depth ==0 or state.winner is not None:
    #         return self._final_eval(state)
    #     valid_actions = [action for action in range(7) if self._CoinRowAfterAction(state.GetCurrentState(),action)!=-1]
    #     if maximizing_player:
    #         value = float('-inf')
    #         for act in valid_actions:
    #            new_state = copy.deepcopy(state)
    #            new_state.GameTreePlayerAction(act)
    #            value = max(value,self._GameTreeSearch_prune(new_state,depth-1,alpha,beta,False))
    #            alpha = max(alpha,value)
    #            if beta <=alpha:
    #                break
    #         return value
    #     else:
    #         value = float('inf')
    #         if not valid_actions:
    #             return value
    #         new_state = copy.deepcopy(state)
    #         new_state.MyopicPlayerAction()
    #         value = min(value,self._GameTreeSearch_prune(new_state,depth-1,alpha,beta,True))
    #         beta=min(beta,value)
    #     return value
    #IMPLEMENTING MOVE ORDER WITH ALPHA BETA PRUNING
    def _GameTreeSearch_move_order(self,state,depth,alpha,beta,maximizing_player):
        self.recursive_calls+=1
        if depth <=0 or state.winner is not None:
            return self._connectivity_evaluation(state)
        valid_actions = [action for action in range(7) if self._CoinRowAfterAction(state.GetCurrentState(),action)!=-1]
        #implement move order heuristic to prioritize middle columns
        if maximizing_player:
            valid_actions.sort(key=lambda action: abs(action -3))#sort by distance from the center column
        else:
            valid_actions.sort()#sort in ascending order for minimizing player
        if maximizing_player:
            value = float('-inf')
            for act in valid_actions:
               new_state = copy.deepcopy(state)
               new_state.GameTreePlayerAction(act)
               value = max(value,self._GameTreeSearch_move_order(new_state,depth-1,alpha,beta,False))
               alpha = max(alpha,value)
               if beta <=alpha:
                   break
            return value
        else:
            value = float('inf')
            if not valid_actions:
                return value
            new_state = copy.deepcopy(state)
            new_state.MyopicPlayerAction()
            value = min(value,self._GameTreeSearch_move_order(new_state,depth-1,alpha,beta,True))
            beta=min(beta,value)
        return value
    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        best_action = None
        best_value = float('-inf')
        valid_actions = [action for action in range(7) if self._CoinRowAfterAction(currentState,action)!=-1]
        for act in valid_actions:
            depth=5
            new_state = FourConnect()
            new_state.SetCurrentState(currentState)
            new_state.GameTreePlayerAction(act)
            value = self._GameTreeSearch_move_order(new_state,depth-1,float('-inf'),float('inf'),False)
            if value> best_value:
                best_value = value
                best_action = act
        print(f"Number of recursive calls: {self.recursive_calls}")
        return best_action #RETURNING THE BEST ACTION
        # bestAction = input("Take action (0-6) : ")
        # bestAction = int(bestAction)
        # return bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
        csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():
    total_games = 50
    total_wins =0
    total_moves=0
    #NOTING THE START TIME
    start_time = time.time()
    #AVERAGING OVER 50 MOVES 
    for _ in range(total_games):
        fourConnect = FourConnect()
        fourConnect.PrintGameState()
        gameTree = GameTreePlayer()
        
        move=0
        while move<42: #At most 42 moves are possible
            if move%2 == 0: #Myopic player always moves first
                fourConnect.MyopicPlayerAction()
            else:
                currentState = fourConnect.GetCurrentState()
                gameTreeAction = gameTree.FindBestAction(currentState)
                fourConnect.GameTreePlayerAction(gameTreeAction)
            fourConnect.PrintGameState()
            move += 1
            if fourConnect.winner!=None:
                break
        if fourConnect.winner==2:
            total_wins+=1
            total_moves+=move
    average_moves = total_moves/total_wins
    end_time = time.time()
    #NOTING THE END TIME
    #TAKING THE DIFFERENCE
    total_time = end_time-start_time
    #PRINTING
    print(f"Total game duration: {total_time:.6f} seconds")
    print(f"Total Wins :{total_wins}")
    print(f"Average Number of Moves: {average_moves}")
    
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    # if fourConnect.winner==None:
    #     print("Game is drawn.")
    # else:
    #     print("Winner : Player {0}\n".format(fourConnect.winner))
    # print("Moves : {0}".format(move))

def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2020B3A71857G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    
    #PlayGame()
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    
    RunTestCase()


if __name__=='__main__':
    main()
