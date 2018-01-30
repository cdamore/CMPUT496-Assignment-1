"""
Module for playing games of Go using GoTextProtocol

This code is based off of the gtp module in the Deep-Go project
by Isaac Henrion and Aamos Storkey at the University of Edinburgh.
"""
import traceback
import sys
import os
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, FLOODFILL
import gtp_connection
import numpy as np
import re

class GtpConnectionGo1(gtp_connection.GtpConnection):

    def __init__(self, go_engine, board, outfile = 'gtp_log', debug_mode = False):
        """
        GTP connection of Go1

        Parameters
        ----------
        go_engine : GoPlayer
            a program that is capable of playing go by reading GTP commands
        komi : float
            komi used for the current game
        board: GoBoard
            SIZExSIZE array representing the current board state
        """
        gtp_connection.GtpConnection.__init__(self, go_engine, board, outfile, debug_mode)
        self.commands["hello"] = self.hello_cmd
        self.commands["score"] = self.score_cmd
    

    def hello_cmd(self, args):
        """ Dummy Hello Command """
        self.respond("Hello! " + self.go_engine.name)
        
    def score_cmd(self, args):
        """Calculate the score of the current board state"""
        #replicate current board state
        goBoard = self.board.get_twoD_board()
        #print('Current Go board state:')
        #print(goBoard)
        # initailize score and correct it for komi (+ score means black wins, - score means white wins)
        score = -(self.komi)
        row_num = 0
        self.total = []
        #for each spot on the board, if white stone: score--, if black stone: score++, 
        #if no stone: call recusive function checkEmptys()
        for row in goBoard:
            num_count = 0
            for num in row:
                if (num == 1):
                    score += 1
                elif (num == 2):
                    score -= 1
                elif (num == 0):
                    #add total = (self.che...)
                    cur_color = self.checkEmptys(goBoard, row_num, num_count, 'i', 0)
                    self.total.append([row_num, num_count, cur_color, False])
                num_count += 1
            row_num += 1
            
        sections = []
        self.sections_index = 0
        
        for empty_spot in self.total:
            if (empty_spot[3] == False):
                empty_spot[3] = True
                self.s_list = []
                self.s_list.append(empty_spot)
                self.calculateEmptys(empty_spot)
                sections.append(self.s_list)
         
        """for emptys in sections:
            print(emptys)"""
            
        for emptys in sections:
            cur_len = len(emptys)
            territory_color = self.get_territory(emptys)
            if (territory_color == 'b'):
                score = score + cur_len 
            if (territory_color == 'w'):
                score = score - cur_len 
            #print("color: " + str(territory_color) + ", score: " + str(cur_len))
               
                        
        #print('score: ' + str(score))
        
        if (score == 0):
            print("= 0")
        elif (score > 0):
            print("= B+" + str(score))
        elif (score < 0):
            print("= W+" + str(abs(score)))
            
       
    def get_territory(self, emptys):
        cur_color = emptys[0][2]
        for item in emptys:
            if (cur_color != 'n'): 
                if (item[2] == 'b'):
                    if (cur_color == 'w'):
                        cur_color = 'n'
                    else:
                        cur_color = 'b'
                elif (item[2] == 'w'):
                    if (cur_color == 'b'):
                        cur_color = 'n'
                    else:
                        cur_color = 'w'
        return cur_color

    def calculateEmptys(self, empty_spot):
        for empty_spot2 in self.total:
            if (empty_spot2[3] == False):
                if (empty_spot[1] == empty_spot2[1] and abs(empty_spot[0] - empty_spot2[0]) == 1):
                    empty_spot2[3] = True
                    self.s_list.append(empty_spot2)
                    self.calculateEmptys(empty_spot2)
                if (empty_spot[0] == empty_spot2[0] and abs(empty_spot[1] - empty_spot2[1]) == 1):
                    empty_spot2[3] = True
                    self.s_list.append(empty_spot2)
                    self.calculateEmptys(empty_spot2)
                    
    def checkEmptys(self, goBoard, row, num, color, count):
        #Get possible moves from the position of empty spot called
        pos_moves = self.getPossibleMoves(row, num)
        #Set current board position to -1 so it doesn't get double counted 
        goBoard[row][num] = -1
        #print('possible moves for point (' + str(num) + ', ' + str(row) + '): '  + str(pos_moves))
        #For each move in the possible moves, 'b' means it is black territory, 'w' means it is in white territoty, and 'n' means it is in neutral terriorty becasue it has both a white and a black stone surronding it. 'i' is the init value when the function is first called. 
        for moves in pos_moves:
            #This code is to keep track of the territory 
            if (color != 'n'):
                if (goBoard[moves[1]][moves[0]] == 1):
                    if (color == 'w'): 
                        color = 'n'
                    else:
                        color = 'b'
                elif (goBoard[moves[1]][moves[0]] == 2):
                    if (color == 'b'):
                        color = 'n'
                    else:
                        color = 'w'

        return color 
        
    def getPossibleMoves(self, row, num):
        pos_moves = []
        if num > 0:
            pos_moves.append([num-1, row])
        if row > 0:
            pos_moves.append([num, row-1])
        if num < self.board.size-1:
            pos_moves.append([num+1, row])
        if row < self.board.size-1:
            pos_moves.append([num, row+1])
        return pos_moves
