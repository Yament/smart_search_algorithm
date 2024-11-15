
from Zero_Squares_LeveLs import Zero_Squares_LeveLs
from Level_Selection_Menu import Level_Selection_Menu
from Main_Menu_GUI import Main_Menu_GUI

def main():
    Level_Object = Level_Selection_Menu()
    Level_Selected = Level_Object.level_selection_menu() - 1
    init_state = Zero_Squares_LeveLs(Level_Selected).Return_Array_Object()
    print(init_state)
    Game = Main_Menu_GUI()
    Game.main_menu(init_state)
   
if __name__ == '__main__':
    main()
