import pickle
import copy
def readfile(filename):
    f = open(filename,'rb')
    result = pickle.load(f)
    f.close()
    result_tmp = copy.deepcopy(result)
    for i in range(len(result_tmp)):
        if len(result_tmp[i]) == 1:
            result.remove(result_tmp[i])
    return result

if __name__ == '__main__':
    result = readfile('result38.bin')
    for i in range(len(result)):
        print("")
        for j in range(len(result[i])):
            print(result[i][j])