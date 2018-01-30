CMPUT 496 Assignment1

In this assignment, you extend a copy of our Go1 program from class by adding a scoring function. A scoring function is called after a game ends. It determines who won the game, and by how many points. The main steps are:

1.Find connected components of empty points on the given Go board.

2.For each component, determine whether it is black territory, white territory, or neutral space.

3.Count how many points each player has achieved.

4.Combine the counts of both players, plus the komi, to compute the score of the game.

5.Implement a new GTP command score for the Go1 player, which computes the score as above, and prints it in a human readable format as specified below.

Designated submitter: Brad Hanasyk 

Group members    Name & Student ID:

Colin D'Amore       1502819

Brad Hanasyk        hanasyk1

Peixuan Li          peixuan1

