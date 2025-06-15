# MM 2023-08-02
import random

# 5x4 digits: 
#  https://www.shutterstock.com/image-vector/pixel-art-numbers-mathematical-signs-vector-125350547
# 5x5 letters:
#  https://i.stack.imgur.com/e9t23.png

CSV_SEPARATOR = ";"
#FLOAT_FORMAT = "0.5f"
FLOAT_FORMAT = "0.0f"

shapes = {
'0': [[0, 2, 3, 0],
      [1, 0, 0, 4],
     [10, 0, 0, 5],
      [9, 0, 0, 6],
      [0, 8, 7, 0]],

'1': [[0, 0, 0, 3],
      [0, 0, 2, 4],
      [0, 1, 0, 5],
      [0, 0, 0, 6],
      [0, 0, 0, 7]],

'2': [[0, 2, 3, 0],
      [1, 0, 0, 4],
      [0, 0, 5, 0],
      [0, 6, 0, 0],
      [7, 8, 9,10]],

'3': [[0, 2, 3, 0],
      [1, 0, 0, 4],
      [0, 0, 5, 0],
      [9, 0, 0, 6],
      [0, 8, 7, 0]],

'4': [[0, 0, 5, 6],
      [0, 4, 0, 7],
      [3, 2, 1, 8],
      [0, 0, 0, 9],
      [0, 0, 0,10]],

'5': [[9,10,11,12],
      [8, 7, 6, 0],
      [0, 0, 0, 5],
      [1, 0, 0, 4],
      [0, 2, 3, 0]],

'6': [[0, 0, 1, 0],
      [0, 2, 0, 0],
      [3, 9, 8, 0],
      [4, 0, 0, 7],
      [0, 5, 6, 0]],

'7': [[1, 2, 3, 4],
      [0, 0, 0, 5],
      [0, 0, 6, 0],
      [0, 7, 0, 0],
      [8, 0, 0, 0]],

'8': [[0, 2, 3, 0],
      [1, 0, 0, 4],
      [0, 6, 5, 0],
      [7, 0, 0,10],
      [0, 8, 9, 0]],

'9': [[0, 4, 5, 0],
      [3, 0, 0, 6],
      [0, 2, 1, 7],
      [0, 0, 8, 0],
      [0, 9, 0, 0]],
}

L = 2 #.4E3 # low frequency: 2.46 kHz
H = 9 #.2E3 # high frequency: 9.26 kHz

f =  [[L, H, L, H],
      [L, H, L, H],
      [L, H, L, L],
      [L, H, H, H],
      [L, L, L, L]]

v = 1 # it takes the stylus 1 s to move to an adjacent, non-diagonal cell

def computePath(arr):
    idx = 1
    found = True
    lastColIdx = 0
    lastRowIdx = 0
    totalDistance = 0
    totalTime = 0
    path = []
    maxRow = len(arr)
    maxCol = len(arr[0]) 
    while found:
        found = False
        for rowIdx in range(len(arr)):
            for colIdx in range(len(arr[rowIdx])):
                if idx == arr[rowIdx][colIdx]:
                    found = True 
                    if idx == 1:
                        d = 1 # start from the center of the pixel
                    else:
                        d = (lastRowIdx - rowIdx) * (lastRowIdx - rowIdx) + (lastColIdx - colIdx) * (lastColIdx - colIdx)
                    lastColIdx = colIdx
                    lastRowIdx = rowIdx
                    idx = idx + 1
                    path.append("({0}, {1})". format(colIdx, maxRow - rowIdx))
    return path

def printSpikesForDictionary(dict): 
    for key, value in dict.items(): 
            path = computePath(value)
            first = path.pop(0)
            last = path.pop()
            output = "\\pth{{{0}}}{{{1}}}{{{2}}} % {3}".format(first, " ".join(path), last, key)
            print(output)

if __name__ == '__main__':
    printSpikesForDictionary(shapes)

