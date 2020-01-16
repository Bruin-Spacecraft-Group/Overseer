import cutdown as cd
import ReceiveData as rd

ERROR_VALUE = 99

while(True):
    inputVal = input()
    retVal = rd.data_receive_callback(inputVal)

    if retVal == ERROR_VALUE:
        cd.cut_down()
