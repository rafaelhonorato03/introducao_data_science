import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [1, 2, 3, 4, 2, 6, 7, 8, 9, 10]

plt.scatter(x, y)
plt.show()

x1 = np.arange(-100, 100, 1)

plt.plot(x1, x1**2)
plt.show()

plt.plot(x1, (x1**2) -2000)
plt.show()