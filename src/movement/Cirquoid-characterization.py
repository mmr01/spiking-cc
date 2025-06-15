# MM 2023-08-31
import random
import serial
import time
import re
import numpy as np

# 5x4 digits: 
#  https://www.shutterstock.com/image-vector/pixel-art-numbers-mathematical-signs-vector-125350547
# 5x5 letters:
#  https://i.stack.imgur.com/e9t23.png

# shapes = {
# '0': [[0, 2, 3, 0],
#       [1, 0, 0, 4],
#      [10, 0, 0, 5],
#       [9, 0, 0, 6],
#       [0, 8, 7, 0]],

# '1': [[0, 0, 0, 3],
#       [0, 0, 2, 4],
#       [0, 1, 0, 5],
#       [0, 0, 0, 6],
#       [0, 0, 0, 7]],

# '2': [[0, 2, 3, 0],
#       [1, 0, 0, 4],
#       [0, 0, 5, 0],
#       [0, 6, 0, 0],
#       [7, 8, 9,10]],

# '3': [[0, 2, 3, 0],
#       [1, 0, 0, 4],
#       [0, 0, 5, 0],
#       [9, 0, 0, 6],
#       [0, 8, 7, 0]],

# '4': [[0, 0, 5, 6],
#       [0, 4, 0, 7],
#       [3, 2, 1, 8],
#       [0, 0, 0, 9],
#       [0, 0, 0,10]],

# '5': [[9,10,11,12],
#       [8, 7, 6, 0],
#       [0, 0, 0, 5],
#       [1, 0, 0, 4],
#       [0, 2, 3, 0]],

# '6': [[0, 0, 1, 0],
#       [0, 2, 0, 0],
#       [3, 9, 8, 0],
#       [4, 0, 0, 7],
#       [0, 5, 6, 0]],

# '7': [[1, 2, 3, 4],
#       [0, 0, 0, 5],
#       [0, 0, 6, 0],
#       [0, 7, 0, 0],
#       [8, 0, 0, 0]],

# '8': [[0, 2, 3, 0],
#       [1, 0, 0, 4],
#       [0, 6, 5, 0],
#       [7, 0, 0,10],
#       [0, 8, 9, 0]],

# '9': [[0, 4, 5, 0],
#       [3, 0, 0, 6],
#       [0, 2, 1, 7],
#       [0, 0, 8, 0],
#       [0, 9, 0, 0]],
# }

# L = 2 #.4E3 # low frequency: 2.46 kHz
# H = 9 #.2E3 # high frequency: 9.26 kHz

# f =  [[L, H, L, H],
#       [L, H, L, H],
#       [L, H, L, L],
#       [L, H, H, H],
#       [L, L, L, L]]

v = 1 # it takes the stylus 1 s to move to an adjacent, non-diagonal cell

def computePath(arr, zPen, zEmpty, scaleXY, offsetX, offsetY):
    idx = 1
    found = True
    lastColIdx = 0
    lastRowIdx = 0
    totalDistance = 0
    totalTime = 0
    path = []
    pathEmpty = []
    maxRow = len(arr)
    maxCol = len(arr[0]) 
    path.append("G54")
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
                    x = offsetX + scaleXY * colIdx;
                    y = offsetY + scaleXY * (maxRow - rowIdx)
                    z = zPen 
                    path.append(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f}". format(x, y, z))
                    z = zEmpty
                    pathEmpty.append(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f}". format(x, y, z))
    path.insert(1, pathEmpty.pop(0))
    path.append(pathEmpty.pop())
 
    return path

def printSpikesForDictionary(dict, zPen, zEmpty, scaleXY, offsetX, offsetY): 
    for key, value in dict.items(): 
            path = computePath(value, zPen, zEmpty, scaleXY, offsetX, offsetY)
            output = "; {0}\n{1}".format(key, "\n".join(path))
            print(output)

def printSpikesForNumber(dict, zPen, zEmpty, scaleXY, offsetX, offsetY, key): 
    value = dict[key]
    path = computePath(value, zPen, zEmpty, scaleXY, offsetX, offsetY)
    output = "; {0}\n{1}".format(key, "\n".join(path))
    print(output)

def get_first_int(input_string):
    match = re.search(r'\d+', input_string)
    if match:
        return int(match.group())
    return None

def sendSpikesForNumber(serial, stm, dict, zPen, zEmpty, scaleXY, offsetX, offsetY, key):
    measurements = []
    within = 0 
    value = dict[key]
    path = computePath(value, zPen, zEmpty, scaleXY, offsetX, offsetY)
    for item in path:
        if item == path[-1]:
            within = 0 #measurement end
            result = ';'.join(measurements)
            print(result)
        if item == path[3]:
            within = 1 #measurement start
            measurements = [key]
        serial.write(bytes(item + '\r\n', 'utf-8'))
        if item == path[1]:
            time.sleep(1)#maybe longer for other numbers    
        # print(item + '\r\n')
        second_pass_time = time.time() + 0.9
        # time.sleep(0.9)
        while time.time() < second_pass_time:
            if within == 1:
                stm.flushInput()
                s = stm.readline()
                s = s.decode('utf-8')
                i = get_first_int(s)
                if i:
                    measurements.append(str(i))

    # output = "; {0}\n{1}".format(key, "\n".join(path))
    # print(output)

HEIGHT = 50
WIDTH = 50
z = -2.5
RANDOM = True
if __name__ == '__main__':
    ser = serial.Serial('COM4', 38400)
    stm = serial.Serial('COM5', 1000000)
    characteristic = []
    for i in range(HEIGHT):
        aux = []
        if i%2 == 0:
            for j in range(WIDTH):
                aux.append(HEIGHT*i+j+1)
        else:
            for j in range(WIDTH):
                aux.append(HEIGHT*i+WIDTH-j)
        characteristic.append(aux)

    # zero = np.array(zero)[0]
    characteristic = np.array(characteristic)
    if RANDOM:
        sh = characteristic.shape
        characteristic = characteristic.flatten()
        np.random.shuffle(characteristic)
        characteristic = characteristic.reshape(sh)

    sizes = [18.0, 63.0, 108.0, 155.0]
    sensor_height = abs(sizes[1] - sizes[0]) / (HEIGHT-1)
    sensor_width = (sizes[3] - sizes[2]) / (WIDTH-1)
    sensor = np.empty((HEIGHT, WIDTH), dtype=object)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            sensor[i][j]=(round(sizes[0] + sensor_height * i, 2), round(sizes[2] + sensor_width * j,2))
    index = 1
    ser.write(bytes("G54\r\n", 'utf-8'))
    first_row = 0
    prev_x, prev_y = 0,0
    while (np.argwhere(characteristic == index).shape[0]):
            msg = ''
            x, y = (sensor[np.argwhere(characteristic == index)[0][0]][np.argwhere(characteristic == index)[0][1]])
            # print(x,y)
            ser.write(bytes(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f}\r\n". format(x, y, z), 'utf-8'))
            msg = 'pall['+str(np.argwhere(characteristic == index)[0][0]+1)+','+str(np.argwhere(characteristic == index)[0][1]+1)+'] = mean(c('
            stm.flushInput()
            if first_row == 0 or abs(prev_x - x) > 35 or abs(prev_y - y) > 35:
                time.sleep(5)
                first_row = 1
            elif abs(prev_x - x) > 20 or abs(prev_y - y) > 20:
                time.sleep(3.5)
            else:
                if RANDOM:
                    time.sleep(2)
                else:
                    time.sleep(0.5)
            first = 0
            prev_x = x
            prev_y = y
            for i in range(50):
                stm.flushInput()
                s = stm.readline()
                s = s.decode('utf-8')
                ints = list(map(int, re.findall(r'\d+', s)))
                if len(ints) > 0:
                    if first != 0:
                        msg += ','
                    msg += str(ints[0])
                    first = 1

            msg += '), na.rm=TRUE)'
            print(msg)
            # msg += str(x)
            # msg += ' '
            # msg += str(y)
            # msg += ' '
            # index += 1
            # msg += str(x)
            # msg += ' '
            # msg += str(y)
            # msg += ' '
            # msg += str(z)
            index += 1
    # # printSpikesForDictionary(shapes, 0, 5, 8, 24, 110)
    # print("Number;Time between spikes")
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2.5, 5, 8, 29, 110, '0')
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2.5, 5, 8, 29, 110, '1')
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2, 5, 8, 24, 110, '2')
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2, 5, 8, 24, 110, '3')
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2, 5, 8, 24, 110, '4')
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2, 5, 8, 24, 110, '5')
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2, 5, 8, 24, 110, '7')
    # for i in range(50):
    #     sendSpikesForNumber(ser, stm, shapes, -2, 5, 8, 24, 110, '8')
        
    ser.close()
    stm.close()
