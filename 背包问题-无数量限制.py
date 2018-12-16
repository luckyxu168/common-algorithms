#问题描述：有一个能装10kg物品的背包，现有A、B、C、D四种物品，重量weight分别为6、3、4、2，价值values分别为30、14、16、9，请你设计一种算法，
#使得背包装入物品的价值最大，每种物品的数量不限。


def knapsack(cap,item):
    value_bag = []      #记录背包可以容纳的重量
    weight = list(item.keys())
    values = list(item.values())
    weight.insert(0,0)       #由于没有可以容纳的重量为0的背包，所以weight和value的前面需要补0
    values.insert(0,0)
    for i in range(0,cap+1):    #把各种大小的背包初始化为0
        value_bag.append(0)
    for i in range(1,len(item)+1):      #对物品item的索引循环，从第一个物品开始循环
        for j in range(1,cap+1):        #对背包大小从1开始循环
            if weight[i]<=j:
                value_bag[j] = max(value_bag[j],value_bag[j-weight[i]]+values[i])#把可以容纳的重量为j的背包所能容纳的最大重量与一个小背包与相对应的物品的和比较，取较大的值
    return value_bag[-1]    #循环结束后得到的value_bag列表记录了可以容纳的重量从1到cap的背包所能容纳的最大价值

item = {6:30,3:14,4:16,2:9}                     #物品，格式为键值对，键代表重量，值代表价值
cap = 10                                        #背包可以容纳的重量
print(knapsack(cap,item))

#说明：本题使用动态规划算法，算法时间复杂度为O(n*W),n为背包可以容纳的重量，W为物品种类的数量
