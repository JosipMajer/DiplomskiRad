# Biblioteke
import socket # Za slanje i primanje paketa
from time import time # Za praćenje vremena
import os # Za implementaciju na raspberry ipu
import gpiod # Upravljanje pinovima


# Zastavice
UDP_PORT = 5005 # port za UDP komunikaciju
TCP_PORT = 5006 # port za TCP komunikaciju
left_arm_hold = False   # zastavica za hvataljku lijeve ruke
right_arm_hold = False  # zastavica za hvataljku desne ruke
CHIP_PATH = 'gpiochip4' # adresiranje GPIO kontrolera
# Na koje su pinovi motori spojeni
HEAD_RIGHT = 16 
HEAD_LEFT = 25
HAND_RIGHT_UP = 17
HAND_RIGHT_DOWN = 27
HAND_LEFT_UP = 24
HAND_LEFT_DOWN = 22
HAND_RIGHT_HOLD = 23
HAND_LEFT_HOLD = 26


# Funkcije

# Uzmi ip adresu za linux
def obtainIpLinux ():
    # Ugl otvori terminal opali naredbu za konfiguraciju i iz nje izvadi ip adresu
    gw = os.popen("ip -4 route show default").read().split()
    return gw[8]

# Funkcija za spajanje na kontroler
def lookingForConnection():
    # Postavljanje socketa u mod cekanja poruke
    # None -> ceka
    # 0 -> provijeri i baci exception
    # > 0 -> cekanje u sekundama
    TCP_socket.settimeout(1)
    # glavna petlja
    while True:
        # Javi se da si tu
        UDP_socket.sendto(b"ThisIsTIOSS", (UDP_BRODCAST, UDP_PORT))
        # Cekaj tcp connection
        try:
            client_socket, client_addres = TCP_socket.accept()
            print("Client connected")
            return client_socket
        except:
            print("Client not found")
            continue  

# Wait funkcija
def customWait(wait_time):
    client_socket.settimeout(wait_time)
    try:
        data = client_socket.recv(32)
        data = data.decode()
        if (data == "Cancle"):
            print("Cancled")
            client_socket.settimeout(None)
            return
    except:
        print("Gotovo cekanje")
        client_socket.settimeout(None)

# Main program

IP_addres = obtainIpLinux()

# Od dodjeljene adrese napraviti brodcast addresu
UDP_BRODCAST = IP_addres.split('.')
UDP_BRODCAST[-1] = '255'
UDP_BRODCAST = '.'.join(UDP_BRODCAST)

# Setup za udp brodcast
UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# dodjela porta i ip adrese socetu
UDP_socket.bind((IP_addres,UDP_PORT))
# Omogućavanje slanje brodcasta
UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Setup za tcp connection
# Stvaranje socketa
TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# dodjela porta i ip adrese socetu
TCP_socket.bind((IP_addres,TCP_PORT))
# omoguci spajanje
TCP_socket.listen()

# Trazenje kontrolera
client_socket = lookingForConnection()

# Inicijalizacija Raspberry pinova
pin_head_right = gpiod.Chip(CHIP_PATH).get_line(HEAD_RIGHT)
pin_head_right.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)
pin_head_left = gpiod.Chip(CHIP_PATH).get_line(HEAD_LEFT)
pin_head_left.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)
pin_hand_right_up = gpiod.Chip(CHIP_PATH).get_line(HAND_RIGHT_UP)
pin_hand_right_up.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)
pin_hand_right_down = gpiod.Chip(CHIP_PATH).get_line(HAND_RIGHT_DOWN)
pin_hand_right_down.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)
pin_hand_left_up = gpiod.Chip(CHIP_PATH).get_line(HAND_LEFT_UP)
pin_hand_left_up.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)
pin_hand_left_down = gpiod.Chip(CHIP_PATH).get_line(HAND_LEFT_DOWN)
pin_hand_left_down.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)
pin_hand_right_hold = gpiod.Chip(CHIP_PATH).get_line(HAND_RIGHT_HOLD)
pin_hand_right_hold.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)
pin_hand_left_hold = gpiod.Chip(CHIP_PATH).get_line(HAND_LEFT_HOLD)
pin_hand_left_hold.request(consumer = "PIN", type=gpiod.LINE_REQ_DIR_OUT)

# Postavljanje inicijalnih vrijednosti Raspberry pinova
pin_head_right.set_value(1)
pin_head_left.set_value(1)
pin_hand_right_up.set_value(1)
pin_hand_right_down.set_value(1)
pin_hand_left_up.set_value(1)
pin_hand_left_down.set_value(1)
pin_hand_right_hold.set_value(1)
pin_hand_left_hold.set_value(1)

# Postavljanje socketa u mod cekanja poruke
client_socket.settimeout(None)

# Petlja za primanje poruka
while (True):
    try:
        # Primi paket
        data = client_socket.recv(32)
        # Dekodiraj poruku 
        data = data.decode()
        data = data.split('.')

        # Za glavu
        if (data[0] == 'GlavaLeft'):
            print("Glava u lijevo")
            pin_head_left.set_value(0)
            customWait(int(data[1]) * 2)
            pin_head_left.set_value(1)
            continue
        if (data[0] == 'GlavaRight'):
            print("Glava u desno")
            pin_head_right.set_value(0)
            customWait(int(data[1]) * 2)
            pin_head_right.set_value(1)
            continue
        # Za ruke
        if (data[0] == 'LArmUp'):
            print("Lijeva ruka gore")
            pin_hand_left_up.set_value(0)
            customWait(int(data[1]) * 2)
            pin_hand_left_up.set_value(1)
            continue
        if (data[0] == 'LArmDown'):
            print("Lijeva ruka dolje")
            pin_hand_left_down.set_value(0)
            customWait(int(data[1]) * 2)
            pin_hand_left_down.set_value(1)
            continue
        if (data[0] == 'RArmUp'):
            print("Desna ruka gore")
            pin_hand_right_up.set_value(0)
            customWait(int(data[1]) * 2)
            pin_hand_right_up.set_value(1)
            continue
        if (data[0] == 'RArmDown'):
            print("Desna ruka dolje")
            pin_hand_right_down.set_value(0)
            customWait(int(data[1]) * 2)
            pin_hand_right_down.set_value(1)
            continue
        if (data[0] == 'RArmHold'):
            if (not right_arm_hold):
                print("Desna ruka pusti")
                right_arm_hold = True
                pin_hand_right_hold.set_value(0)
                customWait(int(data[1]))
                continue
            if (right_arm_hold):
                print("Desna ruka stisni")
                right_arm_hold = False
                pin_hand_right_hold.set_value(1)
                customWait(int(data[1]))
                continue
        if (data[0] == 'LArmHold'):
            if (not left_arm_hold):
                print("Lijeva ruka stisni")
                left_arm_hold = True
                pin_hand_left_hold.set_value(0)
                customWait(int(data[1]))
                continue
            if (left_arm_hold):
                print("Lijeva ruka pusti")
                left_arm_hold = False
                pin_hand_left_hold.set_value(1)
                customWait(int(data[1]))
                continue
 
    except:
        continue



# Zatvori socket
sock.close()
