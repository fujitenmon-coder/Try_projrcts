from calendar import c
from PIL import Image
import numpy as np
import tqdm

yet_list=[]

datalist=[
    [1111,1111,1111,0000,0000,1111,1111,1111,1111,1111],
    [1111,1111,0000,1111,0000,1111,1111,1111,1111,0000],
    [1111,0000,1111,1111,0000,1111,1111,1111,0000,0000],
    [1111,0000,1111,1111,0000,1111,1111,0000,0000,1111],
    [1111,1111,1111,1111,0000,1111,1111,0000,1111,1111],
    [0000,0000,0000,0000,0000,1111,1111,0000,1111,1111],
    [1111,1111,1111,1111,1111,1111,0000,0000,1111,1111],
    [1111,1111,1111,0000,1111,0000,0000,0000,1111,0000],
    [1111,1111,0000,0000,0000,0000,1111,1111,1111,1111],
    [1111,1111,0000,1111,1111,1111,1111,1111,1111,1111]
    ]


def llen(l):
    return range(len(l))


for i in llen(datalist):
    yet_list.append([])
for yy in range(len(datalist)):
    for xx in range(len(datalist[yy])):
        if datalist[yy][xx] > 0:
            yet_list[yy].append(xx)


def count_elements(lis):
    count = 0
    for sublist in lis:
        count += len(sublist)
    return count

def serch_first(lis):
    for li in llen(lis):
        if lis[li] == []:
            pass
        else:
            return (lis[li][0],li)

def research_four_direction(lis,Zaho):
    X=Zaho[0]
    Y=Zaho[1]
    re_list=[]
    if X+1 in lis[Y]:
        re_list.append((X+1,Y))
    if X-1 in lis[Y]:
        if X-1>=0:
            re_list.append((X-1,Y))
    if Y+1<len(lis):
        if X in lis[Y+1]:
            re_list.append((X,Y+1))
    if Y-1>=0:
        if X in lis[Y-1]:
            re_list.append((X,Y-1))
    return re_list

G_list=[]
whi=count_elements(yet_list)
first_element=whi
while whi>0:
    whi=count_elements(yet_list)
    if whi==0:
        break
    even=[]
    odd=[]
    together=[]
    even.append(serch_first(yet_list))
    yet_list[even[0][1]].remove(even[0][0])
    together.append(even[0])
    while len(even)+len(odd)>0:
        for ev in even: 
            app=research_four_direction(yet_list,ev)
            if app!=[]:
                for a in app:
                    odd.append(a)
                    yet_list[a[1]].remove(a[0])
                    together.append(a)
        print("  yet_list length:", count_elements(yet_list),"/",whi)
        even.clear()
         
        for od in odd:
            app=research_four_direction(yet_list,od)
            if app!=[]:
                for a in app:
                    even.append(a)
                    yet_list[a[1]].remove(a[0])
                    together.append(a)
        print("  yet_list length:", count_elements(yet_list),"/",whi)
        odd.clear()
    G_list.append(together)

print("G_list:", G_list)
print("lenG_list:", len(G_list))
Gds=[]
coods=[]
for g in G_list:
    for gg in g:
        Gds.append(gg[0]*10+gg[1])
        coods.append(gg)
    
print("Gds",sorted(Gds))
print("coods",coods)


