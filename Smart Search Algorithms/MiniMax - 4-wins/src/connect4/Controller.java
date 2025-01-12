package connect4;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


/**
 *
 * @author Dallal, Z
 */
public class Controller {

    char computer = 'o';
    char human = 'x';
    Connect4Game board = new Connect4Game(3, 3, 3);

    public void play() {
        System.out.println(board);
        while (true) {
            humanPlay();
            System.out.println(board);

            if (board.isWin(human)) {
                System.out.println("Human wins");
                break;
            }
            if (board.isWithdraw()) {
                System.out.println("Draw");
                break;
            }
            computerPlay();
            System.out.println("_____Computer Turn______");
            System.out.println(board);
            if (board.isWin(computer)) {
                System.out.println("Computer wins!");
                break;
            }
            if (board.isWithdraw()) {
                System.out.println("Draw");
                break;
            }
        }

    }

    //         ************** YOUR CODE HERE ************            \\
    private void computerPlay() {
        // this is a random move, you should change this code to run you own code
        List<Object> result = maxMove(board);
        board = (Connect4Game) result.get(1); 
      

    }

    /**
     * Human plays
     *
     * @return the column the human played in
     */
    private void humanPlay() {
        Scanner s = new Scanner(System.in);
        int col;
        while (true) {
            System.out.print("Enter column: ");
            col = s.nextInt();
            System.out.println();
            if ((col > 0) && (col - 1 < board.getWidth())) {
                if (board.play(human, col - 1)) {
                    return;
                }
                System.out.println("Invalid Column: Column " + col + " is full!, try agine");
            }
            System.out.println("Invalid Column: out of range " + board.getWidth() + ", try agine");
        }
    }

    private List<Object> maxMove(Connect4Game b) {
        // the fuction returns list of object the first object is the evaluation (type Integer), the second is the state with the max evaluation
        //         ************** YOUR CODE HERE ************            \\
        int maxEval = Integer.MIN_VALUE;
        Connect4Game bestMove = null;

        for (Connect4Game nextMove : b.allNextMoves(computer)) {
            int evaluation = nextMove.evaluate(human); 
            if (evaluation > maxEval) {
                maxEval = evaluation;
                bestMove = nextMove;
            }
        }

        List<Object> result = new ArrayList<>();
        result.add(maxEval);
        result.add(bestMove);
        return result;
        
    }

    private List<Object> minMove(Connect4Game b) {
        // the fuction returns list of object the first object is the evaluation (type Integer), the second is the state with the min evaluation
        //         ************** YOUR CODE HERE ************            \\
        int minEval = Integer.MAX_VALUE;
        Connect4Game bestMove = null;

        for (Connect4Game nextMove : b.allNextMoves(human)) {
            int evaluation = nextMove.evaluate(human);
            if (evaluation < minEval) {
                minEval = evaluation;
                bestMove = nextMove;
            }
        }

        List<Object> result = new ArrayList<>();
        result.add(minEval);
        result.add(bestMove);
        return result;

    }

 
 

    public static void main(String[] args) {
        Controller g = new Controller();
        g.play();
    }

}
