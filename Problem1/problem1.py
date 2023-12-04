import pandas as pd
import openpyxl
import math
import random
import numpy as np
import gamspy as gp
import sys

# ## Read data from Excel
filename = "problem1.xlsx"

productsData = pd.read_excel(
    io=filename,
    sheet_name="products"
)
# print(productsData.set_index("product"))

partsData = pd.read_excel(
    io=filename,
    sheet_name="parts"
)
# print(partsData.set_index("part"))

manufactureData = pd.read_excel(
    io=filename,
    sheet_name="manufacture"
).set_index("part")
# print(manufactureData)


# ## Generate data for `demand` follows Bin(10, 0.5)
# - Create probability set of values in range[0,10]
values = list(range(11))
probValues = []
for v in values:
    probValues.append(math.comb(10, v)*pow(0.5, v)*pow(0.5, 10-v))
# print(probValues)

# - Random values for $d^1$ and $d^2$ where probability of each value follows `probValues`
# d1 = random.choices(values, probValues, k=8)
d1 = [7, 4, 3, 2, 4, 5, 1, 8]
# print(d1)

# d2 = random.choices(values, probValues, k=8)
d2 = [5, 6, 7, 0, 5, 9, 8, 6]
# print(d2)

# - Add demand values to `productsData`
productsData["demand 1"] = d1
productsData["demand 2"] = d2
# print(productsData)

# ## Symbol Declaration
# ### Container
m = gp.Container()

# ### Set (indices)

# - $i$ = products
# - $j$ = parts

i = gp.Set(
    container=m,
    name="i",
    description="products",
    records=productsData["product"]
)
# print(i.records)


j = gp.Set(
    container=m,
    name="j",
    description="parts",
    records=partsData["part"]
)
# print(j.records)


# ### Parameter (given data)

# - $b_j$ = preorder cost of part $j$

b = gp.Parameter(
    container=m,
    name="b",
    domain=j,
    description="preorder cost of part j",
    records=partsData[["part", "preorder cost"]]
)
# print(b.records)


# - $l_i$ = assembly cost of product $i$

l = gp.Parameter(
    container=m,
    name="l",
    domain=i,
    description="assembly cost of product i",
    records=productsData[["product", "assembly cost"]]
)
# print(l.records)


# - $q_i$ = selling price of product $i$

q = gp.Parameter(
    container=m,
    name="q",
    domain=i,
    description="selling price of product i",
    records=productsData[["product", "selling price"]]
)
# print(q.records)


# - $s_j$ = salvage value of part $j$

s = gp.Parameter(
    container=m,
    name="s",
    domain=j,
    description="salvage value of part j",
    records=partsData[["part", "salvage value"]]
)
# print(s.records)


# - $a_{ij}$ = amount of part $j$ needed to make a product $i$

a = gp.Parameter(
    container=m,
    name="a",
    domain=[i,j],
    description="amount of part j needed to make a product i",
    records=manufactureData.to_numpy()
)
# print(a.records)


# - $d_i^1$ = demand of product $i$ in scenario 1
# - $d_i^2$ = demand of product $i$ in scenario 2

d1 = gp.Parameter(
    container=m,
    name="d1",
    domain=i,
    description="demand of product i in scenario 1",
    records=productsData[["product", "demand 1"]]
)
# print(d1.records)


d2 = gp.Parameter(
    container=m,
    name="d2",
    domain=i,
    description="demand of product i in scenario 2",
    records=productsData[["product", "demand 2"]]
)
# print(d2.records)


# ### Variable (decision variables)

# - $x_j$ = amount of preorder part $j$ (no negative, integer)

x = gp.Variable(
    container=m,
    name="x",
    domain=j,
    type="integer",
    description="amount of preorder part j"
)

# - $y_j$ = amount of left part $j$ after production (no negative, integer)
#     - $y^1$ for scenario 1
#     - $y^2$ for scenario 2

y1 = gp.Variable(
    container=m,
    name="y1",
    domain=j,
    type="integer",
    description="amount of left part j in scenario 1"
)

y2 = gp.Variable(
    container=m,
    name="y2",
    domain=j,
    type="integer",
    description="amount of left part j in scenario 2"
)


# - $z_i$ = amount of product $i$ to manufacture (no negative, integer)
#     - $z^1$ for scenario 1
#     - $z^2$ for scenario 2

z1 = gp.Variable(
    container=m,
    name="z1",
    domain=i,
    type="integer",
    description="amount of product i in scenario 1"
)

z2 = gp.Variable(
    container=m,
    name="z2",
    domain=i,
    type="integer",
    description="amount of product i in scenario 2"
)


# ### Equation (constaints)

# - Production satisfy demand as much as possible
production1 = gp.Equation(
    container=m,
    name="production1",
    domain=i,
    description="production satisfy a portion of demand i in scenario 1"
)

production2 = gp.Equation(
    container=m,
    name="production2",
    domain=i,
    description="production satisfy a portion of demand i in scenario 2"
)

production1[i] = z1[i] <= d1[i]
production2[i] = z2[i] <= d2[i]

# - Left parts calculation
redundance1 = gp.Equation(
    container=m,
    name="redundance1",
    domain=j,
    description="calculate left parts after production in scenario 1"
)

redundance2 = gp.Equation(
    container=m,
    name="redundance2",
    domain=j,
    description="calculate left parts after production in scenario 2"
)

redundance1[j] = y1[j] == (x[j] - gp.Sum(i, a[i,j]*z1[i]))
redundance2[j] = y2[j] == (x[j] - gp.Sum(i, a[i,j]*z2[i]))

# ### Object Function

# We want to minimize the total cost of the manufacturing,
# the negative result of `obj` is expected so that some profit exist
obj = gp.Sum(j, b[j]*x[j]) + 0.5*(gp.Sum(i, (l[i]-q[i])*z1[i]) - gp.Sum(j, s[j]*y1[j])) + 0.5*(gp.Sum(i, (l[i]-q[i])*z2[i]) - gp.Sum(j, s[j]*y2[j]))

# ### Model
problem1 = gp.Model(
    container=m,
    name="problem1",
    equations=m.getEquations(),
    problem="MIP",
    sense=gp.Sense.MIN,
    objective=obj
)

# ## Solve
problem1.solve(output=sys.stdout)

# ### Viewing Optimal Solution

# - Variable Values
print("[ x values ]")
print(x.records.set_index("j"))

print("\n[ z1 values ]")
print(z1.records.set_index("i"))

print("\n[ y1 values ]")
print(y1.records.set_index("j"))

print("\n[ z2 values ]")
print(z2.records.set_index("i"))

print("\n[ y2 values ]")
print(y2.records.set_index("j"))

# - Optimal Value
print("\n[ optimal value ]")
print(problem1.objective_value)

