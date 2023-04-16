import numpy as np
from sklearn.linear_model import LinearRegression

f = open("linreg_nodupes.txt", "r")

xvars = np.empty([1, 5])
yvars = np.array([[]])


for line in f:
    vals = list(map(int, line.split(';')))
    xvars = np.append(xvars, [vals[:5]], axis=0)
    yvars = np.append(yvars, int(vals[5]))
xvars = np.delete(xvars, 0, 0)

model = LinearRegression().fit(xvars, yvars)

r_sq = model.score(xvars, yvars)
print(r_sq)

print(f"coefficients: {model.coef_}")