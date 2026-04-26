import serial
import struct
import os
import sys
import glob

Flash_HAL_OK                                        = 0x00
Flash_HAL_ERROR                                     = 0x01
Flash_HAL_BUSY                                      = 0x02
Flash_HAL_TIMEOUT                                   = 0x03
Flash_HAL_INV_ADDR                                  = 0x04

#BL Commands
COMMAND_BL_GET_VER                                  = 0x80
COMMAND_BL_FLASH_ERASE                              =0x81
COMMAND_BL_MEM_WRITE                                =0x83
COMMNAD_BL_MEM_VERIFY                               =0x84



#len details of the command
COMMAND_BL_GET_VER_LEN                              =1
COMMAND_BL_FLASH_ERASE_LEN                          =3


verbose_mode = 1
mem_write_active =0

#----------------------------- file ops----------------------------------------

def calc_file_len(filename):
    size = os.path.getsize(filename)
    return size

def open_the_file(filename):
    global bin_file
    bin_file = open(filename,'rb')
    #read = bin_file.read()
    #global file_contents = bytearray(read)

def read_the_file():
    pass

def close_the_file():
    bin_file.close()




#----------------------------- utilities----------------------------------------

def word_to_byte(addr, index , lowerfirst):
    value = (addr >> ( 8 * ( index -1)) & 0x000000FF )
    return value

#----------------------------- Serial Port ----------------------------------------
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def Serial_Port_Configuration(port):
    global ser
    try:
        ser = serial.Serial(port,115200,timeout=2)
    except:
        print("\n   Oops! That was not a valid port")
        
        port = serial_ports()
        if(not port):
            print("\n   No ports Detected")
        else:
            print("\n   Here are some available ports on your PC. Try Again!")
            print("\n   ",port)
        return -1
    if ser.is_open:
        print("\n   Port Open Success")
    else:
        print("\n   Port Open Failed")
    return 0

              
def read_serial_port(length):
    read_value = ser.read(length)
    return read_value

def Close_serial_port():
    pass
def purge_serial_port():
    ser.reset_input_buffer()
    
def Write_to_serial_port(value, *length):
        data = struct.pack('>B', value)
        if (verbose_mode):
            value = bytearray(data)
            #print("   "+hex(value[0]), end='')
            print("   "+"0x{:02x}".format(value[0]),end=' ')
        if(mem_write_active and (not verbose_mode)):
                print("#",end=' ')
        ser.write(data)


        
#----------------------------- command processing----------------------------------------

def process_COMMAND_BL_GET_VER(length):
    ver=read_serial_port(1)
    value = bytearray(ver)
    print("\n   Bootloader Ver. : ",hex(value[0]))
        

def decode_menu_command_code(command):
    ret_value = 0
    data_buf = [0] * 258
    
    if(command  == 0 ):
        print("\n   Exiting...!")
        raise SystemExit
    elif(command == 1):
        print("\n   Command == > BL_GET_VER")
        COMMAND_BL_GET_VER_LEN              = 1
        data_buf[0] = COMMAND_BL_GET_VER
        
        Write_to_serial_port(data_buf[0],1)

        ret_value = read_bootloader_reply(data_buf[0])
        
    elif(command == 2):
        print("\n   Command == > BL_FLASH_ERASE")
        data_buf[0] = COMMAND_BL_FLASH_ERASE
        data_buf[1] = 0x08
        data_buf[2] = 0x08
        for i in data_buf[0:COMMAND_BL_FLASH_ERASE_LEN]:
            Write_to_serial_port(i,COMMAND_BL_FLASH_ERASE_LEN)
        
        ret_value = read_bootloader_reply(data_buf[0])
        
    elif(command == 3):
        print("\n   Command == > BL_MEM_WRITE")
        bytes_remaining=0
        t_len_of_file=0
        bytes_so_far_sent = 0
        len_to_read=0
        current_frame = 0

        data_buf[0] = COMMAND_BL_MEM_WRITE

        #First get the total number of bytes in the .bin file.
        t_len_of_file =calc_file_len("Application.bin")

        #keep opening the file
        open_the_file("Application.bin")

        bytes_remaining = t_len_of_file - bytes_so_far_sent

        global mem_write_active
        while(bytes_remaining):
            current_frame += 1
            data_buf[1] = current_frame
            mem_write_active=1
            if(bytes_remaining >= 256):
                len_to_read = 256
            else:
                len_to_read = bytes_remaining
            #get the bytes in to buffer by reading file
            for x in range(len_to_read):
                file_read_value = bin_file.read(1)
                file_read_value = bytearray(file_read_value)
                data_buf[2+x]= int(file_read_value[0])
            
            mem_write_cmd_total_len = 258

            Write_to_serial_port(data_buf[0],1)
        
            for i in data_buf[1:mem_write_cmd_total_len]:
                Write_to_serial_port(i,mem_write_cmd_total_len)

            bytes_so_far_sent+=len_to_read
            bytes_remaining = t_len_of_file - bytes_so_far_sent
            print("\n   bytes_so_far_sent:{0} -- bytes_remaining:{1}\n".format(bytes_so_far_sent,bytes_remaining)) 
        
            ret_value = read_bootloader_reply(data_buf[0])
        
        #First get the total number of bytes in the .bin file.
        t_len_of_file =calc_file_len("Application.sig")
        print("\n   t_len_of_file :{0}\n".format(t_len_of_file))

        #keep opening the file
        open_the_file("Application.sig")

        data_buf[0] = COMMNAD_BL_MEM_VERIFY

        for x in range(t_len_of_file):
                file_read_value = bin_file.read(1)
                file_read_value = bytearray(file_read_value)
                data_buf[1+x]= int(file_read_value[0])
        
        Write_to_serial_port(data_buf[0],1)

        for i in data_buf[1:(t_len_of_file+1)]:
            Write_to_serial_port(i,(t_len_of_file+1))

        ret_value = read_bootloader_reply(data_buf[0])


        mem_write_active=0

    else:
        print("\n   Please input valid command code\n")
        return

    if ret_value == -2 :
        print("\n   TimeOut : No response from the bootloader")
        print("\n   Reset the board and Try Again !")
        return

def read_bootloader_reply(command_code):

    if(command_code) == COMMAND_BL_GET_VER:
        ack=read_serial_port(2) 
        value=bytearray(ack)
        print("\n   Bootloader Ver. : ",hex(value[1]))

    elif(command_code) == COMMAND_BL_FLASH_ERASE:
        ack=read_serial_port(2) 
        value=bytearray(ack)
        print("\n   Bootloader Erase Status. : ",hex(value[1]))

    elif(command_code) == COMMAND_BL_MEM_WRITE:
        ack=read_serial_port(3) 
        value=bytearray(ack)
        print("\n   Frame Number Flashed : ",hex(value[1]))
        print("\n   Write Success : ",hex(value[2]))

    elif((command_code) == COMMNAD_BL_MEM_VERIFY):
        ack=read_serial_port(2) 
        value=bytearray(ack)
        print("\n   Continue with write command : ",hex(value[1]))

    ret = 0
        
    return ret

            
            

#----------------------------- Ask Menu implementation----------------------------------------


name = input("Enter the Port Name of your device(Ex: COM3):")
ret = 0
ret=Serial_Port_Configuration(name)
if(ret < 0):
    decode_menu_command_code(0)
    

    
  
while True:
    print("\n +==========================================+")
    print(" |               Menu                       |")
    print(" |         STM32F4 BootLoader v1            |")
    print(" +==========================================+")

  
    
    print("\n   Which BL command do you want to send ??\n")
    print("   BL_GET_VER                            --> 1")
    print("   BL_FLASH_ERASE                        --> 2")
    print("   BL_MEM_WRITE                          --> 3")
    print("   MENU_EXIT                             --> 0")

    #command_code = int(input("\n   Type the command code here :") )

    command_code = input("\n   Type the command code here :")

    if(not command_code.isdigit()):
        print("\n   Please Input valid code shown above")
    else:
        decode_menu_command_code(int(command_code))

    input("\n   Press any key to continue  :")
    purge_serial_port()





    

def check_flash_status():
    pass

def protection_type():
    pass

