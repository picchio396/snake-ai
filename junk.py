import time
for i in range(10):
    print('Attempt {0} of 10 Attempt {1} of 10'.format(i,i), end='\r')
    time.sleep(1)