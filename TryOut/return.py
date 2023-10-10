def ret():
    data = (1, 3, 5, 7, 9)
    (result, *_) = data if data else None
    return result


def ret2(data):
    # if data:
    #     (x, *_) = data
    # else:
    #     x = None
    x = data[0] if data else None
    return x


print(ret2((1, 3, 5, 7, 9)))

print(f"{ret2(None)}")
