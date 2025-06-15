# MM 2023-08-28
import csv

CSV_SEPARATOR = ";"
#FLOAT_FORMAT = "0.5f"
FLOAT_FORMAT = "0.0f"
DIGIT = 0

FILENAME = '../data/2023-08-31-69.csv'

def printSpikes(spikes, adjust = 0):
    if adjust > 0:
        cpy = []
        while len(cpy) < adjust:        
            for x in spikes:
                cpy.append(x)
        while len(cpy) > adjust:
            cpy.pop()
        spikes = cpy
    output = CSV_SEPARATOR.join(format(x, FLOAT_FORMAT) for x in spikes)
    print(DIGIT, output, sep=CSV_SEPARATOR)
    #print(len(spikes))


if __name__ == '__main__':
    with open(FILENAME) as file:
        csvreader = csv.reader(file, delimiter=CSV_SEPARATOR)
        prev = 0 
        sequence = []
        first = 0
        for row in csvreader:
            if first != 0: 
                digit = int(row[0].strip())
                sequence.clear()
                if digit == 6:
                    DIGIT = 0
                else:
                    DIGIT = 1
                for index in range(1, len(row)):
                    try:
                        sequence.append(int(row[index].strip()))
                    except:
                        pass
                printSpikes(sequence, 3460)
            else:
                first = 1
            # if digit == 0 and prev != 0:
            #     printSpikes(sequence, 3457)
            #     sequence.clear()
            # elif digit == 0 and prev == 0:
            #     continue
            # elif digit != 0: 
            #     sequence.append(delay)
            # prev = digit
