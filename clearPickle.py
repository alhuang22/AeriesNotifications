import pickle

def clear_all():
    count = 1
    for i in range(6):
        path = '/Users/alexhuang/Desktop/aeriesNotifications/data/' + 'period' + str(count) + '.p'
        empty = []
        with open(path,'wb') as handle:
            pickle.dump(empty, handle)
        count += 1
    print('All periods cleared!')

def clear_specific(period):
    path = '/Users/alexhuang/Desktop/aeriesNotifications/data/' + 'period' + str(period) + '.p'
    empty = []
    with open(path,'wb') as handle:
        pickle.dump(empty, handle)
    print('Period ' + str(period) + ' cleared!')
        

clear_all()
#clear_specific(2)