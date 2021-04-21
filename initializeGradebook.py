import pickle

empty = []

for i in range(6):
    name = '/Users/alexhuang/Desktop/aeriesNotifications/data' + 'period' + '%d' % (i+1)
    name = name + '.p'
    print(name)
    with open(str(name), 'wb') as handle:
        pickle.dump(empty,handle)
