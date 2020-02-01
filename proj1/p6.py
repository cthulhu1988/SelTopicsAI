#!/usr/bin/env python3
import math, sys
import numpy as np

class pathObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sub_x = None
        self.sub_y = None
    def __sub__(self, obj):
        self.sub_x = (self.x - obj.x)
        self.sub_y = (self.y - obj.y)

    def print_stats(self):
        print("X {} and Y {}".format(self.x, self.y))

    def print_sub(self):
        print("sub X {} and sub Y {}".format(self.sub_x, self.sub_y))


class TraceObj(object):
    def __init__(self, x, y):
        self.direction_list =[]
        self.x = x
        self.y = y
        self.left = None
        self.up = None
        self.diag = None
        self.previous = None
        self.prev_x = None
        self.prev_y = None

    def set_dir(self):
        if "diag" in self.direction_list:
            self.diag = [self.x-1, self.y-1]
        if "up" in self.direction_list:
            self.up = [self.x, self.y-1]
        if "left" in self.direction_list:
            self.left = [self.x-1, self.y]
        if self.up:
            self.previous = self.up
            self.prev_x = self.previous[0]
            self.prev_y = self.previous[1]
        if self.left:
            self.previous = self.left
            self.prev_x = self.previous[0]
            self.prev_y = self.previous[1]
        if self.diag:
            self.previous = self.diag
            self.prev_x = self.previous[0]
            self.prev_y = self.previous[1]
    def print_stats(self):
        print("current point -> x {} y {} ::: next point - > x {} y {} ".format(self.x, self.y, self.prev_x, self.prev_y))

match_value = int(sys.argv[1])
mismatch_penalty = int(sys.argv[2])
gap_penalty = int(sys.argv[3])
data = sys.stdin.readlines()

def main():
    back_track_list = []
    #############INIT #################################
    top_seq_col = data[0].strip()
    left_seq_row = data[1].strip()

    ## init empty matrix ###
    topCol = len(top_seq_col)+1 ; sideRow = len(left_seq_row)+1
    score_matrix = np.zeros((sideRow, topCol), dtype=int)
    score_matrix[0,:] = 0
    score_matrix[:,0] = 0

    traceback_list = []
    counter = 0

    node_list = []
    for Y_row in range(1,topCol):
        for X_col in range(1,sideRow):
            counter +=1
            max, trace_line, node = return_max(score_matrix, Y_row, X_col, top_seq_col, left_seq_row, counter)
            score_matrix[X_col][Y_row] = max
            traceback_list.append(trace_line)
            node_list.append(node)

    path_list = []
    node_list.reverse()

    node = node_list[0]
    path_obj = pathObj(node.x, node.y)
    path_list.append(path_obj)
    pre_x = node.prev_x ; pre_y = node.prev_y
    for x in range(1,len(node_list)):
        node = node_list[x]
        if node.x == pre_x and node.y == pre_y:
            pre_x = node.prev_x ; pre_y = node.prev_y
            path_obj = pathObj(node.x, node.y)
            path_list.append(path_obj)

    path_obj = pathObj(node.prev_x, node.prev_y)
    path_list.append(path_obj)

#########################################################

    final_seq1, final_seq2 = traceback(path_list, top_seq_col, left_seq_row)
    final_seq1 = final_seq1[::-1]
    final_seq2 = final_seq2[::-1]
    print(final_seq1)
    print(final_seq2)

def traceback(path_list, top_seq_col, left_seq_row):
    new_seq1 = ""
    new_seq2 = ""

    seq1 = "Z";seq2 = "Z"
    seq1 += top_seq_col ; seq2 += left_seq_row
    seq1_len = len(seq1) ; seq2_len = len(seq2)

    path_node = path_list[0]
    for idx in range(1,len(path_list)):
        path_node - path_list[idx]
        if path_node.sub_x == 1:
            new_seq1 += (seq1[path_node.x])
        else:
            new_seq1 += "-"
        if path_node.sub_y == 1:
            new_seq2 += (seq2[path_node.y])
        else:
            new_seq2 += "-"
        path_node = path_list[idx]
    return new_seq1, new_seq2

def return_max(matrix,i,j, top_seq_col, left_seq_row, counter):
    new_row_dict = {}
    new_row = []
    if top_seq_col[i-1] == left_seq_row[j-1]:
        add = match_value
    else:
        add = mismatch_penalty

    diag = (matrix[j-1,i-1] + add)
    left = (matrix[j,i-1] + gap_penalty)
    up = (matrix[j-1,i] + gap_penalty)
    new_row_dict ={"left":left,"up":up,"diag":diag}
    max_val = -1000
    key_value = ""
    for k,v in new_row_dict.items():
        if v > max_val:
            max_val = v
            key_value = k
    for key, value in new_row_dict.items():
        if value == max_val:
            new_row.append(key)

    node = TraceObj(i,j)
    node.direction_list = new_row
    node.set_dir()
    new_row.append(i)
    new_row.append(j)

    highest_val = max(diag, left, up)
    return highest_val, new_row, node

def print_matrix(score_matrix, top_seq_col, left_seq_row):
    leng = len(left_seq_row)
    print("    G A A T T C A G T T A")
    for i in range(score_matrix.shape[0]):
        if i == 0:
            print("  ", end="")
        else:
            print(left_seq_row[i-1], end=" ")
        for j in range(score_matrix.shape[1]):
            num = score_matrix[i,j]
            if num < 0:
                print(score_matrix[i,j],end='')
            else:
                print(score_matrix[i,j],end=' ')
        print()
    print()

if __name__ == '__main__':
    main()
