num = 5
x = 50
match num:
    case 0:
        print("It is zero")
    case n if n < 100 and x > 40:
        print(n, "less than 100 but bigger than zero")
    case _:
        print("A really big number")
