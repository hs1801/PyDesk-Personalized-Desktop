
import os
clear = lambda: os.system("cls")

d = {1:['Player 2','O'] , 0:['Player 1','X']}

def check():
    if a[0]==a[1]==a[2] or a[3]==a[4]==a[5] or a[6]==a[7]==a[8] or a[0]==a[3]==a[6] or a[1]==a[4]==a[7] or\
        a[2]==a[5]==a[8] or a[0]==a[4]==a[8] or a[2]==a[4]==a[6] :
        return(False)
    else:
        return(True)
def pattern():
    print('Player 1 = X\t Player 2 = O\n\n\t\t ',a[0],' |  ',a[1],'  | ',a[2],\
          '\n\t\t-----+-------+-----\n\t\t ',a[3],' |  ',a[4],'  | ',a[5],\
          '\n\t\t-----+-------+-----\n\t\t ',a[6],' |  ',a[7],'  | ',a[8])
c='y'          
while c=='y':
    a = [1,2,3,4,5,6,7,8,9]
    i = 0
    used = []
    pattern()
    while check() and len(used) != 9:
        try:
            print(d[i%2][0],':')
            pawn = int (input('\t'))
            if pawn not in used and (pawn):
                a[pawn-1] = d[i%2][1]
                used += [pawn]
                i += 1
                clear()
                pattern()
            else:
                continue
        except:
            continue
    if len(used)==9:
        print("It's a Draw")
    else:
        print ('The Winner is:',d[(i-1)%2][0])
    c = input("Enter 'y' to restart, any other key to end... ")
