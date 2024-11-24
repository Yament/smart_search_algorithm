
from User_Play import User_Play
from Depth_First_Search import Depth_First_Search
from Breadth_First_Search import Breadth_First_Search
from UCS import UCS


 
class Zero_Squares_Game:

    def __init__(self , init_state) -> None:
        self.init_state = init_state

    def User_Play(self):
       game = User_Play(self.init_state)
       game.Play_Game()

    def Depth_First_Search(self) :
        game = Depth_First_Search(self.init_state)
        game.Depth_First_Search_Solve()

    def Breadth_First_Search(self) :
        game = Breadth_First_Search(self.init_state)
        game.Breadth_First_Search_Solve()

    def Unifrom_Cost_Search(self) :
        game = UCS(self.init_state)
        game.UCS()

         
    
   


 

 

 




