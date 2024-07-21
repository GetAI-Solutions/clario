import pandas as pd

data = pd.read_csv("data.csv")

with open("products/product1.txt") as f:
  data1 = f.read()

with open("products/product2.txt") as f:
  data2 = f.read()

with open("products/product3.txt") as f:
  data3 = f.read()

with open("products/product4.txt") as f:
  data4 = f.read()


data["details"] = [data1, data3, data2, data4]
data.to_csv("data.csv")