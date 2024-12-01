
def Get_Manhattan_Distance_Hurestic (self , square) :
        Target = self.Get_Target_Square(square.target_square)
        Manhattan_Distance_Hurestic = abs(square.x - Target.x) + abs(square.y - Target.y)
        return Manhattan_Distance_Hurestic