import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
california_data = fetch_california_housing(as_frame=True)
data = california_data.frame
correlation_matrix = data.corr()
sns.heatmap(correlation_matrix,annot=True)
plt.title('Correlation Matrix of California Housing Features')
plt.show()
sns.pairplot(data)
plt.suptitle('Pair Plot of California Housing Features', y=1.02)
plt.show()