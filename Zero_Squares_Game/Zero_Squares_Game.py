
from User_Play import User_Play
from Depth_First_Search import Depth_First_Search
from Breadth_First_Search import Breadth_First_Search
from DFS_By_Recursion import DFS_By_Recursion
from Uniform_Cost_Search import Unifrom_Cost_Search
from Hill_Climbing import Hill_Climbing
from A_Star import A_Star


 
class Zero_Squares_Game:

    def __init__(self , init_state) -> None:
        self.init_state = init_state

    def User_Play(self):
       game = User_Play(self.init_state)
       game.Play_Game()

    def Depth_First_Search(self) :
        game = Depth_First_Search(self.init_state)
        game.Depth_First_Search_Solve()

    def Depth_First_Search_Recursion(self) :
        game = DFS_By_Recursion()
        game.Depth_First_Search_BY_Recursion(self.init_state)

    def Breadth_First_Search(self) :
        game = Breadth_First_Search(self.init_state)
        game.Breadth_First_Search_Solve()

    def Unifrom_Cost_Search(self) :
        game = Unifrom_Cost_Search(self.init_state)
        game.Unifrom_Cost_Search_Solve()

    def A_Star_Search(self) :
        game = A_Star(self.init_state)
        game.A_Star_Solve()


    def Hill_Climbing_Search(self) :
        game = Hill_Climbing(self.init_state)
        game.Hill_Climbing_solve()

         
   


 

 

 




