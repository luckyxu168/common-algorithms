def knapsack(cap,item):
    value_bag = []
    weight = list(item.keys())
    values = list(item.values())
    weight.insert(0,0)
    values.insert(0,0)
    for i in range(0,cap+1):
        value_bag.append(0)
    for i in range(1,len(item)+1):
        for j in range(1,cap+1):
            if weight[i]<=j:
                value_bag[j] = max(value_bag[j],value_bag[j-weight[i]]+values[i])
    return value_bag[-1]

item = {6:30,3:14,4:16,2:9}                     #物品，格式为键值对，键代表重量，值代表价值
cap = 10                                        #背包可以容纳的重量
print(knapsack(cap,item))

