# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.

li=[1,2,3,4,5,6,7]
li.append(9);print(li)
li.extend([10,"a"]);print(li)
li.insert(9,"b") ;print(li)
li.remove("a") ;print(li)
li.pop(-1) ; print(li)
li.sort(reverse = True) ; print(li)
a = li.index(5,0,-1) ;print("index",a)
pi = li.copy() ;pi[0]="z";print(li,pi)
count=li.count(2) ;print("count",count)
li.clear();print(li)
pi = pi[1:-1]
si = sorted(pi ,key=None ,reverse = False) ; print(si)
max = max(pi) ;print(max)
min = min(pi) ;print(min)
sum = sum(pi) ;print(sum)
