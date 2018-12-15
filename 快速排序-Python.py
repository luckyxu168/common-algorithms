def partition(A):
    x = A[0]
    j = 0
    for i in range(1,len(A)):
        if x>=A[i]:
            j+=1
            A[j],A[i] = A[i],A[j]
    A[0],A[j] = A[j],A[0]
    return j
def quick_sort(A):
    if len(A)<2:
        return A
    p = partition(A)
    return quick_sort(A[0:p])+[A[p]]+quick_sort(A[p+1:len(A)])

print(quick_sort([7,8,6,4,9,2,6,7,6,6,6]))

import random as r
def randomized_quick_sort(A):
    if len(A)<2:
        return A
    k= r.randint(0,len(A)-1)
    A[0],A[k]=A[k],A[0]
    p=partition(A)
    return randomized_quick_sort(A[0:p])+[A[p]]+randomized_quick_sort(A[p+1:len(A)])
print(randomized_quick_sort([7,8,6,4,9,2,6,7,6,6,6]))