                # SINGLE LINE CALCULATOR - REPEATABLE
x=1
r=0
print("------WELCOME TO REPEATABLE SINGLE-LINE CALCULATOR------")
while x==1 or x==2:
    i=0
    if x==1:        #For Repetition
        str=input("Enter a operation: ")

        while True:
            if str[i] in ['+','-','%','*','/']:
                break
            i+=1
        op=str[i]
        a=str[0:i]
        b=str[i+1:len(str)+1]

        if str[i] in ['*','/']:
            if str[i]==str[i+1]:
                op=str[i]*2
                b=str[i+2:len(str)+1]
            
        a=float(a)
    if x==2:        #For Continution
        str=input("Enter continued operation: ")
        a=r
        if str[0] in ['+','-','%']:
            op=str[0]
            b=str[1:len(str)+1]
        elif str[0] in ['*','/']:
            if str[1]==str[0]:
                op=str[0]*2
                b=str[2:len(str)+1]
            else:
                op=str[0]
                b=str[1:len(str)+1]
    b=float(b)
    if a%1==0:
        a=int(a)
    if b%1==0:
        b=int(b)
                    #Overall Calculations
    print(a,op,b,'=',end=' ')
    opi={'+':a+b,'-':a-b,'*':a*b,'**':a**b,'/':a/b,'//':a//b,'%':a%b}

    if op in opi:
        r=opi[op]
        print(r)
                    #Menu
    x=int(input("Enter 1 to restart\n\t2 two continue last result\n\tAny other key to end:\t"))
    
