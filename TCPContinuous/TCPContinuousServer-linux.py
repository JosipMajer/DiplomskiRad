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
motor_is_running = False    # zastavica za jesu li motori upaljeni
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

# Funkcija za zaustaviti motore
def stopMotors():
    pin_head_right.set_value(1)
    pin_head_left.set_value(1)
    pin_hand_right_up.set_value(1)
    pin_hand_right_down.set_value(1)
    pin_hand_left_up.set_value(1)
    pin_hand_left_down.set_value(1)   


# Main program

IP_addres = obtainIpLinux()

# Od dodjeljene adrese napraviti brodcast addresu
UDP_BRODCAST = IP_addres.split('.')
UDP_BRODCAST[-1] = '255'
UDP_BRODCAST = '.'.join(UDP_BRODCAST)

# Setup za udp 
# Stvaranje socketa
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

# Trazenje TIOSA
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

# Vrijeme
rememberTime = 0

# Postavljanje socketa u mod provjeri jeli ima poruke ako ne exception
client_socket.settimeout(0)

# Petlja za primanje poruka
while (True):
    try:
        # Primi paket
        data, addr = client_socket.recvfrom(32)
        # Dekodiraj poruku 
        data = data.decode()

        # Za glavu
        if (data == 'GlavaLeft'):
            if (time() - rememberTime < 0.07):
                rememberTime = time()
                continue
            rememberTime = time()
            motor_is_running = True
            pin_head_left.set_value(0)
            print("Glava u lijevo")
            continue
        if (data == 'GlavaRight'):
            if (time() - rememberTime < 0.07):
                rememberTime = time()
                continue
            rememberTime = time()
            motor_is_running = True
            pin_head_right.set_value(0)
            print("Glava u desno")
            continue
        # Za ruke
        if (data == 'LArmUp'):
            if (time() - rememberTime < 0.07):
                rememberTime = time()
                continue
            rememberTime = time()
            motor_is_running = True
            pin_hand_left_up.set_value(0)
            print("Lijeva ruka gore")
            continue
        if (data == 'LArmDown'):
            if (time() - rememberTime < 0.07):
                rememberTime = time()
                continue
            rememberTime = time()
            motor_is_running = True
            pin_hand_left_down.set_value(0)
            print("Lijeva ruka dolje")
            continue
        if (data == 'RArmUp'):
            if (time() - rememberTime < 0.07):
                rememberTime = time()
                continue
            rememberTime = time()
            motor_is_running = True
            pin_hand_right_up.set_value(0)
            print("Desna ruka gore")
            continue
        if (data == 'RArmDown'):
            if (time() - rememberTime < 0.07):
                rememberTime = time()
                continue
            rememberTime = time()
            motor_is_running = True
            pin_hand_right_down.set_value(0)
            print("Desna ruka dolje")
            continue
        if (data == 'RArmHold'):
            if (time() - rememberTime < 0.2):
                continue
            rememberTime = time()
            if (not right_arm_hold):
                print("Desna ruka pusti")
                right_arm_hold = True
                pin_hand_right_hold.set_value(0)
                continue
            if (right_arm_hold):
                print("Desna ruka stisni")
                right_arm_hold = False
                pin_hand_right_hold.set_value(1)
                continue
        if (data == 'LArmHold'):
            if (time() - rememberTime < 0.2):
                continue
            rememberTime = time()
            if (not left_arm_hold):
                print("Lijeva ruka stisni")
                left_arm_hold = True
                pin_hand_left_hold.set_value(0)
                continue
            if (left_arm_hold):
                print("Lijeva ruka pusti")
                left_arm_hold = False
                pin_hand_left_hold.set_value(1)
                continue
 
    except:
        if (time() - rememberTime > 0.2 and motor_is_running):
            print("Ugasi")
            motor_is_running = False
            stopMotors()
        continue



# Zatvori socket
sock.close()


