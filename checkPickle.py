import pickle
count = 1

for i in range(6):
    path = './data/' + 'period' + str(count) + '.p'
    with open(path,'rb') as handle:
        lis = pickle.load(handle)
    print(count)
    count += 1

    print(lis)