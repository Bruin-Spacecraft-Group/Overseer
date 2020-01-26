import cutdown as cd
import ReceiveData as rd

ERROR_VALUE = 99
#the following code works
#while True:
#   ser.write(str.encode('Hello  User))
#   incoming = ser.readline().strip()
#   print('Received:' + incoming)
while(True):
    print("receiving data")
    inputVal = input()
    retVal = rd.data_receive_callback(inputVal)

    if retVal == ERROR_VALUE:
        print("Cutting down the balloon\n")
        cd.cut_down()
