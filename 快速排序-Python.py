def partition(A):               #分割：把比第一个数大的数放到后面
    x = A[0]
    j = 0
    for i in range(1,len(A)):
        if x>=A[i]:
            j+=1
            A[j],A[i] = A[i],A[j]
    A[0],A[j] = A[j],A[0]
    return j
def quick_sort(A):          #快速排序
    if len(A)<2:            #空列表与只含一个元素的列表无需排序，直接返回
        return A
    p = partition(A)
    return quick_sort(A[0:p])+[A[p]]+quick_sort(A[p+1:len(A)])




import random as r      #随机快速排序
def randomized_quick_sort(A):
    if len(A)<2:
        return A
    k= r.randint(0,len(A)-1)        #在列表中随机选取一个元素
    A[0],A[k]=A[k],A[0]
    p=partition(A)
    return randomized_quick_sort(A[0:p])+[A[p]]+randomized_quick_sort(A[p+1:len(A)])
