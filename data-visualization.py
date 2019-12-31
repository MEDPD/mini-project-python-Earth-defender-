from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


data = {'left': [1],'right': [50], 'up': [80], 'down': [30]}
df = pd.DataFrame(data)
# df.to_csv(index= False,path_or_buf='./data/data.csv', mode='w')
dataFirePosition = pd.read_csv('./data/dataFirePosition.csv')
dataXY = pd.read_csv('./data/dataXY.csv')


# fig, ax = plt.subplots(1, 1)
plt.figure(figsize=(10, 5))
plt.subplot(121)

# max_nbOf_bullet = max([max(dataFirePosition['LEFT']), max(dataFirePosition['RIGHT']), max(dataFirePosition['UP']), max(dataFirePosition['DOWN'])])
# plt.yticks(np.arange(0, max_nbOf_bullet+1, 2.0))
plt.ylabel('Bullet Number')
dataFirePosition.iloc[-1].plot.bar(rot=0)

plt.subplot(122)
plt.axis((0, 800, 0, 600))
x = dataXY['x']
y = dataXY['y']

# plt.xticks(50)
plt.yticks(np.arange(0, 600+1, 50.0))

plt.plot(x, y)

plt.show()









# # plt.subplot(131)
# plt.ylabel("Bullets Number")
# plt.bar(names, values)
# # plt.subplot(132)
# # plt.scatter(names, values)
# # plt.subplot(133)
# # plt.plot(names, values)
# # plt.suptitle('Categorical Plotting')
# plt.show()