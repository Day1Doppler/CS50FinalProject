import cs50

def main():
    while True:
        height = cs50.get_int("Height: ")
        if height >= 0 and height <= 23:
            break
    pyramid(height)    
        
def pyramid(height):
    for i in range (height):
        left_side_row(i, height)
        print(" ", end = "")
        right_side_row(i)

def left_side_row(row, height):
    for i in range(height):
        if i + row + 1 < height:
            print(" ", end = "")
        else:
            print("#", end = "")
    

def right_side_row(row):
    for i in range(row + 1):
        print("#", end = "")
    print("\n", end = "")    
    

if __name__ == "__main__":
    main()