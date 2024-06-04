import math  

# n = int(input("Enter the number of valueables = "))
# m = int(input("Enter the number of condition = "))
# z = input("enter the objective function is max or min : ")
# C = list(map(int,input("enter C = ").split()))

# A = []
# for i in range(m):
#     a = list(map(int,input(f'enter A{i+1} = ').split()))
#     A.append(a)

# B = list(map(int,input("enter B = ").split()))

# sign = []
# for i in range(1, m+1):
#     s1 = input(f"enter sign of {i} condition : ")
#     sign.append(s1)
    
# sign_x = []  
# for i in range(1, n+1):
#     s2 = input(f"enter sign of x{i} : ")
#     sign_x.append(s2)

n = 3
m = 3
z = "min"
C = [5 , 0 ,0 ]
A = [[1,5 ,0],[1, 0 ,-3],[2,3,4]]
B = [7,6,1]
sign = ["<=","<=","="]
sign_x = [">=", "<=", "free"]
method = input("enter which method to use : (simplex) or (big m) or (dofaz) : ")

# standard form

for i in range(n):
    if sign_x[i] == ">=":
        continue

    elif sign_x[i] == "<=":
        C[i]*=(-1)
        for j in range(m):
            A[j][i]*=(-1)

    elif sign_x[i] == "free":
        C.insert(i+1, C[i]*(-1))        
        for j in range(m):
            A[j].insert(i+1, A[j][i]*(-1))
          

if method == "simplex":  
    cj = []
    for i in range(m):
        if sign[i] == "=":
            continue

        elif sign[i] == "<=":
            for j in range(m):
                if i == j :
                    A[i].append(1)
                    cj.append(f"s{i}")
            
                else:
                    A[i].append(0)            

        elif sign[i] == ">=":
            for j in range(m):
                if i == j :
                    A[i].append(-1)
                else:
                    A[i].append(0)
        C.append(0)

    xi = []
    for i in range(n):
        xi.append(f"x{i}")
    for i in range(m):
        xi.append(f"s{i}") 

    index_base = []
    for i in range(len(xi)):
        for j in range(len(cj)):
            if xi[i] == cj[j]:
                index_base.append(i) 
    print(index_base)             

    Cb = C[n: ] 

    print("Cb  Cj",end="   ")
    for i in range(len(xi)):
        print(xi[i],end="  ")
    print("  ","RHS \n")
    for i in range(m):
        print(Cb[i],end='   ')
        print(cj[i],end="   ")
        for j in range(len(xi)):
            print(A[i][j] , end='   ')
        print("  ",B[i],'\n')
    

    C_ = []
    for i in range(len(C)):
        sum = 0
        for j in range(m):
            sum += Cb[j]*A[j][i]
        if abs(C[i] - sum) < 0.1:
            C_.append(0)
        else:
            C_.append(C[i]-sum)

    Z = 0
    for i in range(m):
        Z += Cb[i]*B[i]
    
    print('C_  -> ' , end='   ')
    for i in range(len(C_)):
        print(C_[i] , end='   ')
    print("  ",Z)
    print(" _ " *20)      


    while True:  

        if 0 in B:
            print("Tabahidegi rokh dade")

        if z == "max":
            s = 0
            for i in range(len(C_)):
                if C_[i] <= 0:
                    s+=1
            if s < len(C_):    
                index_col = C_.index(max(C_))
            else:
                break 

        elif z == "min":
            s = 0
            for i in range(len(C_)):
                if C_[i] >= 0:
                    s+=1
            if s < len(C_):
                index_col = C_.index(min(C_)) 
            else:
                break  

        RHS = []
        for i in range(len(C)):
            for j in range(m):             
                if A[j][index_col] != 0:           
                    RHS.append(B[j]/A[j][index_col] )  

        positive_RHS = [i for i in RHS if i >= 0]
        index_row = RHS.index(min(positive_RHS))
        print("motagheur vorudy , khorojy",end=" = ")
        print("(",index_col,",",index_row,")\n")

        index_base[index_row] = index_col
        Cb[index_row] = C[index_col]
        B[index_row]/=A[index_row][index_col]

        for j in range(len(C)):
            if j != index_col:
                A[index_row][j]/=A[index_col][index_row]

        A[index_row][index_col] = 1  
        for i in range(m):
            if i == index_row:
                continue
            else:
                e = A[i][index_col]/((-1)*A[index_row][index_col])
                for j in range(len(C)):
                    A[i][j]+= e * A[index_row][j]
                B[i]+=B[index_row]* e 

        C_ = []
        for i in range(len(C)):
            sum = 0
            for j in range(m):
                sum += Cb[j]*A[j][i]
            if abs(C[i] - sum) < 0.1:
                C_.append(0)
            else:
                C_.append(C[i]-sum) 

        Z = 0
        for i in range(m):
            Z += Cb[i]*B[i] 

        cj = []
        for i in range(m):
            cj.append(xi[index_base[i]])  

        print("Cb  Cj",end="   ")
        for i in range(len(xi)):
            print(xi[i],end="  ")
        print("  ","RHS \n")

        for i in range(m):
            print(Cb[i],end='   ')
            print(cj[i],end="   ")
            for j in range(len(xi)):
                print(A[i][j] , end='   ')
            print("  ",B[i],'\n')

        print('C_  -> ' , end='   ')
        for i in range(len(C_)):
            print(C_[i] , end='   ')
        print("  ",Z)
        print(" _ " *20)               


elif method == "big m":
    break_while = False

    positive_inf = math.inf
    negative_inf = -math.inf

    xi = []
    cj = []
    for i in range(m):
        if sign[i] == "=":
            xi.append(f"R{i}")
            cj.append(f"R{i}")

        elif sign[i] == "<=":
            xi.append(f"S{i}")
            cj.append(f"S{i}")

        elif sign[i] == ">=":
            xi.append(f"S{i}")
            xi.append(f"R{i}") 
            cj.append(f"R{i}")

    for i in range(m):
        if sign[i] == "<=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    A[i].append(1)
                else:
                    A[i].append(0)  

        elif sign[i] == ">=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    A[i].append(1)
                elif i == j:
                    A[i].append(-1)
                else:
                    A[i].append(0)

        elif sign[i] == "=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    A[i].append(1)
                else:
                    A[i].append(0) 

    for i in range(n):
        xi.insert(i ,f"x{i}")     

    index_M = []
    for i in range(len(xi)):
        if xi[i] == "R":
            index_M.append(i)

    index_base = []
    for i in range(len(cj)):
        if sign[i] == "<=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    index_base.append(j)

        elif sign[i] == ">=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    index_base.append(j)

        elif sign[i] == "=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    index_base.append(j) 
    
    if z == "min":
        Cb = []
        for i in range(m):
            if sign[i] == ">=":
                Cb.append(positive_inf)
                C.append(0)
                C.append(positive_inf)
            elif sign[i] == "=":
                Cb.append(positive_inf)
                C.append(positive_inf)
            else:
                Cb.append(0) 
                C.append(0) 

    elif z == "max":
        Cb = []
        for i in range(m):
            if sign[i] == ">=":
                Cb.append(negative_inf)
                C.append(0)
                C.append(negative_inf)
            elif sign[i] == "=":
                Cb.append(negative_inf)
                C.append(negative_inf)
            else:
                Cb.append(0) 
                C.append(0)             

    print("Cb     Cj",end="     ")
    for i in range(len(xi)):
        print(xi[i],end="   ")
    print("     ","RHS \n")
    for i in range(m):
        print(Cb[i],end='     ')
        print(cj[i],end="    ")
        for j in range(len(xi)):
            print(A[i][j] , end='    ')
        print("   ",B[i],'\n')

    C_ = []
    for i in range(len(C)):
        sum = 0
        for j in range(m):
            sum += Cb[j]*A[j][i]
        if abs(C[i] - sum) < 0.1:
            C_.append(0)
        else:
            C_.append(C[i]-sum)

    Z = 0
    for i in range(m):
        Z += Cb[i]*B[i]
    
    print('C_    -> ' , end='    ')
    for i in range(len(C_)):
        print(C_[i] , end='    ')
    print("   ",Z)
    print(" _ " *20)          
    

    while True:  

        if 0 in B:
            print("Tabahidegi rokh dade")

        if z == "max":
            s = 0
            for i in range(len(C_)):
                if C_[i] <= 0:
                    s+=1
            if s < len(C_):    
                index_col = C_.index(max(C_))
            else:
                break 

        elif z == "min":
            s = 0
            for i in range(len(C_)):
                if C_[i] >= 0:
                    s+=1
            if s < len(C_):
                index_col = C_.index(min(C_)) 
            else:
                break  

        RHS = []
        for i in range(len(C)):
            for j in range(m):             
                if A[j][index_col] != 0:           
                    RHS.append(B[j]/A[j][index_col] )  

        positive_RHS = [i for i in RHS if i >= 0]
        index_row = RHS.index(min(positive_RHS))
        print("motagheur vorudy , khorojy",end=" = ")
        print("(",index_col,",",index_row,")\n")
        
        index_base[index_row] = index_col
        Cb[index_row] = C[index_col]
        B[index_row]/=A[index_row][index_col]

        for j in range(len(C)):
            if j != index_col and A[index_col][index_row] != 0:
                A[index_row][j]/=A[index_col][index_row]

        A[index_row][index_col] = 1  
        for i in range(m):
            if i == index_row:
                continue
            else:
                e = A[i][index_col]/((-1)*A[index_row][index_col])
                for j in range(len(C)):
                    A[i][j]+= e * A[index_row][j]
                B[i]+=B[index_row]* e 

        C_ = []
        for i in range(len(C)):
            sum = 0
            for j in range(m):
                sum += Cb[j]*A[j][i]
            if abs(C[i] - sum) < 0.1:
                C_.append(0)
            else:
                C_.append(C[i]-sum)       

        Z = 0
        for i in range(m):
            Z += Cb[i]*B[i]

        cj = []
        for i in range(m):
            cj.append(xi[index_base[i]])  

        print("Cb     Cj",end="     ")
        for i in range(len(xi)):
            print(xi[i],end="   ")
        print("       ","RHS \n")

        for i in range(m):
            print(Cb[i],end='    ')
            print(cj[i],end="      ")
            for j in range(len(xi)):
                print(A[i][j] , end='    ')
            print("      ",B[i],'\n')

        print('C_    -> ' , end='    ')
        for i in range(len(C_)):
            print(C_[i] , end='    ')
        print("   ",Z)
        print(" _ " *20)              


    for i in index_M:
        if i in index_base:
            print('The articial valuable has not been remove so problem is impossible!')     
            break_while = True
            break       


elif method == "dofaz": 

    xi = []
    cj = []
    for i in range(m):
        if sign[i] == "=":
            xi.append(f"R{i}")
            cj.append(f"R{i}")

        elif sign[i] == "<=":
            xi.append(f"S{i}")
            cj.append(f"S{i}")

        elif sign[i] == ">=":
            xi.append(f"S{i}")
            xi.append(f"R{i}") 
            cj.append(f"R{i}")

    for i in range(m):
        if sign[i] == "<=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    A[i].append(1)
                else:
                    A[i].append(0)  
            C.append(0)

        elif sign[i] == ">=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    A[i].append(1)
                elif i == j:
                    A[i].append(-1)
                else:
                    A[i].append(0)
            C.append(0)
            C.append(0)

        elif sign[i] == "=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    A[i].append(1)
                else:
                    A[i].append(0) 
            C.append(0)                       
    
    for i in range(n):
        xi.insert(i ,f"x{i}")
        

    index_base = []
    for i in range(len(cj)):
        if sign[i] == "<=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    index_base.append(j)

        elif sign[i] == ">=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    index_base.append(j)

        elif sign[i] == "=":
            for j in range(len(xi)):
                if cj[i] == xi[j]:
                    index_base.append(j)                

    Cw = []
    Cb = []
    for i in range(m):
        if sign[i] == ">=":
            Cb.append(1)
            Cw.append(0)
            Cw.append(1)
        elif sign[i] == "=":
            Cb.append(1)
            Cw.append(1)
        else:
            Cb.append(0) 
            Cw.append(0) 
    for i in range(n):
        Cw.insert(i ,0) 
                      
    print("Cb    Cj",end="     ")
    for i in range(len(xi)):
        print(xi[i],end="   ")
    print("       ","RHS \n")
    for i in range(m):
        print(Cb[i],end='    ')
        print(cj[i],end="      ")
        for j in range(len(xi)):
            print(A[i][j] , end='    ')
        print("      ",B[i],'\n')  

    xi = []
    for i in range(m):
        if sign[i] == "=":
            xi.append("R")
            cj.append("R")

        elif sign[i] == "<=":
            xi.append("S")
            cj.append("S")

        elif sign[i] == ">=":
            xi.append("S")
            xi.append("R") 
            cj.append("R")

    for i in range(n):
        xi.insert(i ,"x")

    index_R =[]
    for i in range(len(xi)):
        if xi[i] == "R":
            index_R.append(i)      
    
    C_w = []
    for i in range(len(Cw)):
        sum = 0
        for j in range(m):
            sum += Cb[j]*A[j][i]
        if abs(Cw[i] - sum) < 0.1:
            C_w.append(0)
        else:
            C_w.append(Cw[i]-sum) 

    for i in range(len(Cw)):
        W = 0
        for j in range(m):
            W += Cb[j]*A[j][i]

    print('C_w  -> ' , end='    ')
    for i in range(len(C_w)):
        print(C_w[i] , end='    ')
    print("   ",W)
    print(" _ " *20)    


    while True:
        break_while = False
        if 0 in B:
            print("Tabahidegi rokh dade")

        s = 0
        for i in range(len(C_w)):
            if C_w[i] >= 0:
                s+=1
        if s < len(C_w):
            index_col = C_w.index(min(C_w)) 
        else:
            print("The problem is not answered")
            break

        RHS = []
        for i in range(len(Cw)):
            for j in range(m):
                if A[j][index_col] != 0:           
                    RHS.append(B[j]/A[j][index_col] )   
        positive_RHS = [i for i in RHS if i >= 0]
        index_row = RHS.index(min(positive_RHS))
        print("motagheur vorudy , khorojy",end=" = ")
        print("(",index_col,",",index_row,")\n")

        index_base[index_row] = index_col
        Cb[index_row] = Cw[index_col]

        B[index_row]/=A[index_row][index_col]
        for j in range(len(Cw)):
            if j != index_col and A[index_col][index_row] != 0:
                A[index_row][j]/=A[index_col][index_row]
        A[index_row][index_col] = 1  
        for i in range(m):
            if i == index_row:
                continue
            else:
                e = A[i][index_col]/((-1)*A[index_row][index_col])
                for j in range(len(Cw)):
                    A[i][j]+= e * A[index_row][j]
                B[i]+=B[index_row]* e 
            
        C_w = []
        for i in range(len(Cw)):
            sum = 0
            for j in range(m):
                sum += Cb[j]*A[j][i]
            if abs(Cw[i] - sum) < 0.1:
                C_w.append(0)
            else:
                C_w.append(Cw[i]-sum)         


        for i in range(len(Cw)):
            W = 0
            for j in range(m):
                W += Cb[j]*A[j][i]

        cj = []
        for i in range(m):
            cj.append(xi[index_base[i]])  

        print("Cb   Cj",end="     ")
        for i in range(len(xi)):
            print(xi[i],end="   ")
        print("      ","RHS \n")

        for i in range(m):
            print(Cb[i],end='    ')
            print(cj[i],end="      ")
            for j in range(len(xi)):
                print(A[i][j] , end='    ')
            print("     ",B[i],'\n')

        print('C_W  -> ' , end='    ')
        for i in range(len(C_w)):
            print(C_w[i] , end='    ')
        print("   ",W)
        print(" _ " *20)                     
        if W == 0:
            break 

    for i in index_R:
        if i in index_base:
            print('The articial valuable has not been remove so problem is impossible!')     
            break_while = True
            break   
             
    if not break_while:
        print("end of phase 1 \n")

        c = len(Cb)
        Cb = []
        for i in range(c):
            Cb.append(C[index_base[i]])
    

        count_R = 0 
        for i in range(len(xi)):
            if xi[i] == "R":
                count_R +=1
        for i in range(count_R):
            C.pop()
        

        indices = [i for i in range(len(xi)) if xi[i] == "R"]
        for i in range(m):
            for j in reversed(indices):
                if j < len(A[i]):
                    del A[i][j]

        C_ = []
        for i in range(len(C)):
            sum = 0
            for j in range(m):
                sum += Cb[j]*A[j][i]
            if abs(C[i] - sum) < 0.1:
                C_.append(0)
            else:
                C_.append(C[i]-sum)

        Z = 0
        for i in range(m):
            Z += Cb[i]*B[i]            
                
        cj = []
        for i in range(m):
            cj.append(xi[index_base[i]])  

        print("Cb     Cj",end="     ")
        for i in range(len(xi)):
            print(xi[i],end="   ")
        print("      ","RHS \n")

        for i in range(m):
            print(Cb[i],end='    ')
            print(cj[i],end="      ")
            for j in range((len(xi))-count_R):
                print(A[i][j] , end='    ')
            print("     ",B[i],'\n')

        print('C_  -> ' , end='    ')
        for i in range(len(C_)):
            print(C_[i] , end='    ')
        print("   ",Z)
        print(" _ " *20)     

        while True:

            if 0 in B:
                print("Tabahidegi rokh dade")        

            if z == "max":
                s = 0
                for i in range(len(C_)):
                    if C_[i] <= 0:
                        s+=1
                if s < len(C_):    
                    index_col = C_.index(max(C_))
                else:
                    break     
            elif z == "min":
                s = 0
                for i in range(len(C_)):
                    if C_[i] >= 0:
                        s+=1
                if s < len(C_):
                    index_col = C_.index(min(C_)) 
                else:
                    break     
            RHS = []
            for i in range(len(C)):
                for j in range(m):             
                    if A[j][index_col] != 0:           
                        RHS.append(B[j]/A[j][index_col] )  
            positive_RHS = [i for i in RHS if i >= 0]
            index_row = RHS.index(min(positive_RHS))
            print("motagheur vorudy , khorojy",end=" = ")
            print("(",index_col,",",index_row,")\n")

            Cb[index_row] = C[index_col]
            if A[index_row][index_col] != 0:
                B[index_row]/=A[index_row][index_col]
            for j in range(len(C)):
                if j != index_col:
                    A[index_row][j]/=A[index_col][index_row]
            A[index_row][index_col] = 1  
            for i in range(m):
                if i == index_row:
                    continue
                else:
                    e = A[i][index_col]/((-1)*A[index_row][index_col])
                    for j in range(len(C)):
                        A[i][j]+= e * A[index_row][j]
                    B[i]+=B[index_row]* e 
                    C_ = []
            for i in range(len(C)):
                sum = 0
                for j in range(m):
                    sum += Cb[j]*A[j][i]
                if abs(C[i] - sum) < 0.1:
                    C_.append(0)
                else:
                    C_.append(C[i]-sum)  

        Z = 0
        for i in range(m):
            Z += Cb[i]*B[i]                  

        cj = []
        for i in range(m):
            cj.append(xi[index_base[i]])  

        print("Cb   Cj",end="     ")
        for i in range(len(xi)):
            print(xi[i],end="   ")
        print("      ","RHS \n")

        for i in range(m):
            print(Cb[i],end='    ')
            print(cj[i],end="      ")
            for j in range((len(xi))-count_R):
                print(A[i][j] , end='    ')
            print("     ",B[i],'\n')

        print('C_  -> ' , end='    ')
        for i in range(len(C_)):
            print(C_[i] , end='    ')
        print("   ",Z)
        print(" _ " *20)    