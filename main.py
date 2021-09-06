def nod(a, b):
    if b == 0:
        return a
    else:
        return nod(b, a % b)


def nok(a, b):
    return a * b // nod(a, b)

print(nok(82, 1082))