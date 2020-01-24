import cutdown as cd
import ReceiveData as rd

ERROR_VALUE = 99

while(True):
    inputVal = input()
    retVal = rd.data_receive_callback(inputVal)

    if retVal == ERROR_VALUE:
        print("Cutting down the balloon\n")
        cd.cut_down()
