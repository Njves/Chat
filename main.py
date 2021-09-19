import msvcrt

while True:
    pressedKey = msvcrt.getch()
    if ord(pressedKey) == ord('q'):
       print("exit")
    else:
       print ("Key Pressed:", ord(pressedKey))
