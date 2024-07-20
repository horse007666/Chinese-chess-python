#/bin/tcsh
# -*- coding: utf-8 -*-
import time,os,sys
import random,copy

dict={
	1:"将",
	2:"士",
	3:"相",
	4:"马",
	5:"车",
	6:"包",
	7:"兵",
	-1:"帅",
	-2:"仕",
	-3:"象",
	-4:"馬",
	-5:"車",
	-6:"炮",
	-7:"卒",
        0:"  ",
}

current=[[0]*9 for j in range(10)]
def init(current):
    for i in range(9):    
        current[0][i]=1+abs(i-4)
        current[9][i]=-current[0][i]
    current[2][1]=6
    current[2][7]=6
    
    current[7][1]=-6
    current[7][7]=-6

    for i in range(0,9,2):
        current[3][i]=7
        current[6][i]=-7

def print_chess(current,now=(0,0),blink=False):
    #os.system("clear")
    for i in range(10):
        if i==5:
            print("\n"+"-"*35)
        for j in range(9):
            index_i=9-i     
            character=dict[current[index_i][j]]
            if blink and (index_i,j)==now:
                bb=5
            else:
                bb=1
            if current[index_i][j]>0:
                color="31"
            else:
                color="30"

            #print "\033[%d;%sm;47 %s\033[0m|" % (bb,color,character), 
            print( "\033[%d;%sm%s\033[0m|" % (bb,color,character), end="" )

        print("\n"+"-"*35)
    print("~"*35)
#now=(0,0)
#next=[(),(),(),()]

def moverule(current,now):
    i,j=now
    index=abs(current[i][j])

    next=[]
    if index==0: 
        next=[]
    if index==1:
        next=[(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        for k,l in copy.deepcopy(next):
            if k not in(0,1,2,7,8,9) or l not in (3,4,5):
                next.remove((k,l))
        start={1:[0,1,2],-1:[7,8,9]}
        mystart=start[current[i][j]]
        enemystart=start[-current[i][j]]

        enemy_i=-10
        for k in enemystart:
              if current[k][j]==-current[i][j]:
                  enemy_i=k
        nums=0
        for k in range(min(i,enemy_i)+1,max(i,enemy_i)): 
            if (enemy_i!=-10 and current[k][j]!=0):    
                nums+=1
        if nums==0 and enemy_i!=-10:
            next.append((enemy_i,j))
                

    if index==2:
        next=[(i-1,j-1),(i+1,j-1),(i-1,j+1),(i+1,j+1)]
        for k,l in copy.deepcopy(next):
            if k not in (0,1,2,7,8,9) or l not in(3,4,5):
                next.remove((k,l)) 
    if index==3:
        next=[(i-2,j-2),(i+2,j-2),(i-2,j+2),(i+2,j+2)]
        for k,l in copy.deepcopy(next):
            if (k-4.5)*(i-4.5)<0 or k<0 or k>9 or l<0 or l>8 :
                next.remove((k,l))      
        for k,l in copy.deepcopy(next):
            if current[(i+k)//2][(j+l)//2]!=0:
                next.remove((k,l))
    if index==4:
        next=[(i-2,j+1),(i-2,j-1),(i-1,j+2),(i-1,j-2),(i+2,j-1),(i+2,j+1),(i+1,j+2),(i+1,j-2)] 
        for k,l in copy.deepcopy(next):
            if k<0 or k>9 or l<0 or l>8 :
                next.remove((k,l))
        for k,l in copy.deepcopy(next):
            biejiao_i=(i if abs(k-i)==1 else (i+k)//2 )
            biejiao_j=(j if abs(l-j)==1 else (j+l)//2)
            if current[biejiao_i][biejiao_j]!=0:
                next.remove((k,l))

    if index==5 or index==6:
        for k,l in [(k,j) for k in range(10)]+[(i,k) for k in range(9)]:
            if (k,l)==(i,j):
                continue
            nums=0
            for (k_try,l_try) in [(i,l_try) for l_try in range(min(j,l)+1,max(j,l))]+[(k_try,j) for k_try in range(min(i,k)+1,max(i,k))]: 
                if current[k_try][l_try]!=0:
                    nums+=1

            if index==5 and nums==0:
                next.append((k,l))
            if index==6:
                if (current[k][l]==0  and nums==0) or ( current[k][l]!=0 and nums==1 ):
                    next.append((k,l))
               

    if index==7:
        value=current[i][j]//index
        if value*(i-4.5)<0:
            next=[(i+value,j)]
        else:
            next=[(i+value,j),(i,j-1),(i,j+1)]
            for k,l in copy.deepcopy(next):
                if k<0 or k>9 or l<0 or l>8 :
                    next.remove((k,l))
    for k,l in copy.deepcopy(next):    
        if(current[i][j]*current[k][l]>0):
            next.remove((k,l))
    return next

# if ismemove=1 then me move,
# if ismemove=-1 then rival move
def domove(current,ismemove):
    mypawn=[]
    for i in range(10): 
        for j in range(9):
            if (ismemove*current[i][j]>0):
                mypawn.append((i,j)) 
# choose which pawn to move
    choose_index=int(random.uniform(0,len(mypawn))) 
    now=mypawn[choose_index] 
    next=moverule(current,now)
    if (next==[]):
        return domove(current,ismemove)
    next_choose_index=int(random.uniform(0,len(next)))
    next_step=next[next_choose_index]

    (i,j)=now
    for (k_try,l_try) in next:
        if current[i][j]*current[k_try][l_try]<0 :
            next_step=(k_try,l_try)
    (k,l)=next_step
    os.system("clear")
    print("\033[H\033[J",end='')
    print_chess(current,(i,j),True)
    current[k][l]=current[i][j]
    current[i][j]=0
    time.sleep(3)
    os.system("clear")
    print("\033[H\033[J",end='')
    print_chess(current)
    time.sleep(3)
    return

def gameover(current):
    isover=0
    redwin=0
    blackwin=0
    for i in range(10): 
        for j in range(9):
            if current[i][j]==1:
                isover+=1 
                redwin=1
            if current[i][j]==-1:
                isover+=1
                blackwin=1 
    if isover!=2 and redwin:
        print("RED Wins!!!!")
    if isover!=2 and blackwin:
        print("BLACK Wins!!!")
    return isover!=2 

init(current)
ismemove=1
while(not gameover(current)):
    #print_chess(current)
    #time.sleep(1)
    domove(current,ismemove)
    ismemove=-1*ismemove





