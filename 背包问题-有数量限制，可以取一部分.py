def knapsack(cap,item):
    weight = list(item.keys())
    values = list(item.values())
    unit_value = []
    for k,v in item.items():
        unit_value.append(v/k)      #计算每种物品的单价
    bag_values = []
    while cap!=0:
        m = max(unit_value)         #找到单价最大的物品
        if cap>=weight[unit_value.index(m)]:        #如果放的下
            bag_values.append(values[unit_value.index(m)])         #就装入背包
            cap-=weight[unit_value.index(m)]
            unit_value[unit_value.index(m)] = 0         #删掉此物品
        else:
            bag_values.append((cap/weight[unit_value.index(m)])*values[unit_value.index(m)])    #如果放不下，就取一部分
            cap = 0         #此时背包已装满
    return sum(bag_values)

item = {4:20,3:18,2:14}     #物品，格式为键值对，键代表重量，值代表价值
cap = 7                     #背包可以容纳的重量
print(knapsack(cap,item))
