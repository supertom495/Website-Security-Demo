
from bottle import route, get, run, post
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from pathlib import Path
import random
import shutil
import os
import numpy as np
from os import rename, listdir


# Important globals
host = "localhost"
port = "8079"
waf_port = 8078

# Our "Database"
user = {}
currentUser = ""
waf_string = "http://{address}:{port}".format(address=host, port=waf_port)

# -----------------------------------------------------------------------------
#WAF Check attack
def check_attack(attack_vector):
        # Check for malicious code
        response = requests.post("{target}/waf/detect/{attack_vector}"
            .format(target=waf_string, attack_vector=attack_vector))

        # Rather than redirecting, you can attempt to sanitise the string
        attacked = response.text

        if attacked != "True":
            redirect('/invalid')
        else:
            return attacked
#-----------------------------------------------------------------------------

# Hash password function (with salt) TODO
def hash(string):
    salt = string[-4:] + "!(*%#@)"
    salted_string = string + salt
    hashed_string = MD5.new(salted_string.encode()).hexdigest()
    return hashed_string


# Encryption function using AES TODO
def encrypt(string):
    # while len(string) % 16 != 0:
    #     string = string + ' '
    key = 'key99887 hArd lIfe'
    mode = AES.MODE_CBC
    IV = 'IV77 liFe ToUgh'
    encryptor = AES.new(key, mode, IV)
    cipher_text = encryptor.encrypt(string)
    return cipher_text


# Decryption function using AES TODO
def decrypt(string):
    key = b'asdfghjkl1234567'
    mode = AES.MODE_CBC
    IV = b'asdfghjkl1234567'
    decryptor = AES.new(key, mode, IV)
    plain_text = decryptor.decrypt(string)
    return plain_text.strip().decode('utf-8')


# API calls
@post('/api/useradd/<username:path>/<password:path>/<email:path>/<memberType:path>/<TFnumber:path>')
def useradd(username, password, email, memberType, TFnumber):

    cakepath="data/"+ username + "/"

    if not os.path.exists(cakepath):
        os.makedirs(cakepath)

    rel_path = "data/" + username + "/" + username + ".txt"
    file = open(rel_path, mode='w')

    file.write('{}${}${}${}'.format(password, email, memberType, TFnumber))

    file.close()

    return None


# return "User added"


@post('/api/check_login/<username:path>/<password:path>/<authentication:path>')
def check_login(username, password, authentication):
    if check_existence(username):
        # file exists
        get_details(username, ".txt")
        if password != user[username][0] or authentication != user[username][3]:
            return False
    else:  # Wrong Username
        return False

    return True

@post('/api/logOut')
def logOut():
    global currentUser
    currentUser = ""

@post('/api/reset')
def reset():
    reset_file()

@post('/api/setCurrentUser/<username:path>')
def setCurrentUser(username):
    global currentUser
    currentUser = username
    user[currentUser] = (user[currentUser][0], user[currentUser][1], user[currentUser][2], get_auth_number())
    write_details(currentUser, ".txt")


@post('/api/check_existence/<username:path>')
def check_existence(username):
    path = "data/" + username + "/" + username + ".txt"
    my_file = Path(path)
    if my_file.is_file():
        return True
    else:
        return False

@post('/api/check_existenceport/<port:path>')
def check_existenceport(port):
    path = "data/" + "honeyport" + "/" + port
    my_file = Path(path)
    if my_file.is_file():
        return True
    else:
        return False


@post('/api/getCurrentUser')
def getCurrentUser():
    return currentUser


@post('/api/userget/<username:path>')
def userget(username):

    if username in user:
        rel_path = "data/" + username + "/" + username + ".txt"
        info = open(rel_path).read()
        return info
    else:
        return "User does not exist!"

@post('/api/check_license')
def check_license():

    path1 = "data/" + currentUser + ".apply"
    path2 = "data/" + currentUser + ".license"

    if not Path(path1).is_file() and not Path(path2).is_file():
        # you do not have license, you can apply # write to a file to request the license
        write_details(currentUser, ".apply")
        return True

    else:
        # you already have a license
        return False

@post('/api/check_renew_license')
def check_renew_license():

    path = "data/" + currentUser + ".license"
    if Path(path).is_file():
        if check_license_vaild_year() == 0:
            return True
        else:
            # "Your license do not need renew, its still valid"
            return False

    else:
        # you do not have license, You need a license before u renew it
        # write_details(currentUser, ".apply")
        return False

@post('/api/approve/<apply:path>')
def apprrove(apply):
    todelete = open('data/' + apply +'.vehicleRegister')
    lines = todelete.read()
    todelete.close()
    os.remove('data/' + apply +'.vehicleRegister')
    rel_path = 'data/' + apply + '.vehicle'
    f = open(rel_path, 'w+')
    f.write(lines)
    f.close()

@post('/api/readApproveVehicleRegister')
def readApproveVehicleRegister():
    applylist = []
    data = os.listdir('data/')
    for d in data:
        if d.endswith('.vehicleRegister'):
            applylist.append(d[:-16] + '$')
    return applylist

@post('/api/APLA')
def APLA():
    applylist = []
    data = os.listdir('data/')
    for d in data:
        if d.endswith('.apply'):
            applylist.append(d[:-6] + '$')
    return applylist




@post('/api/check_sale/<registration:path>/<purchaser:path>/<amount:path>')
def check_sale(registration, purchaser, amount):
    if not check_existence(purchaser):
        # "Purchaser does not exist"
        return False
    else:
        # User exist
        # write the sale detail to output
        # registration exist still need
        # "Infomation uploaded, wait the staff to apprrove"
        data = os.listdir('data/')
        destory = data.endswith('.destory')
        for d in destory:
            m = d.split('.')
            if registration is m[0]:
                # "The vehicle is destoried"
                return False
        vehicle = data.endswith('.vehicle')
        noReg = True
        for v in vehicle:
            str = v.split('.')
            if registration == str[0] and currentUser == str[1]:
                newName = v - v[-8:] + '.sale'
                os.rename(v, newName)
                # "Infomation uploaded, wait the staff to apprrove"
                return True
            elif registration == str[0]:
                # "This vehicle does not belong to you"
                return False

        return True

@post('/api/check_car/<username:path>/<carNumber:path>/<brand:path>/<model:path>/<color:path>/<safetycheck:path>')
def check_car(username, carNumber, brand, model, color, safetycheck):

    isDestory = checkVehicleDestory(carNumber)

    if isDestory:
        # this car has been destoried
        return True
    else:
        CarForm(username, carNumber, brand, model, color, safetycheck)
        # car exist, wait to procced
        return False



# Write account information from database
# information -> [0]password [1]email [2]account_type

def write_details(username, type):

    cakepath="data/"+ username + "/"

    if not os.path.exists(cakepath):
        os.makedirs(cakepath)

    rel_path = "data/" + username + "/" + username + type
    file = open(rel_path, mode='w')
    isFirst = True

    if type == ".apply":
        file.close()
        return

    for item in user[username]:
        if isFirst:
            file.write("%s" % item)
            isFirst = False
        else:
            file.write("$%s" % item)

    file.close()

#----------------------------------------------------
#a fuction to write port files
@post('/api/write_port/<honeyport:path>/<candyport:path>')
def write_port(honeyport, candyport):

    cakepath="data/"+ honeyport + "/"

    if not os.path.exists(cakepath):
        os.makedirs(cakepath)

    rel_path = "data/" + honeyport + "/" + honeyport + candyport
    file = open(rel_path, mode='w')


#----------------------------------------------------

# Read account information from database
# information -> [0]password [1]email [2]account_type
# format of data file | (password) + '$' + (email) + '$' +(account_type)
def get_details(username, type):
    rel_path = "data/" + username + "/" + username + type
    info = open(rel_path).read().split('$')
    user[username] = info

# return information

def get_auth_number():
    return "aa"
    return hash(random.choice('abcdefghij') + random.choice('klmnopqrstuvwxyz'))[:2]

def reset_file():
    global currentUser
    currentUser = "admin"
    shutil.rmtree('data')
    if not os.path.exists("data"):
        os.makedirs("data")
    user["admin"] = ("admin", "admin@gmail.com", "admin", get_auth_number())
    write_details("admin", ".txt")

def check_license_vaild_year():
    rel_path = "data/" + currentUser + ".license"
    info = open(rel_path).read()
    year = int(info)
    return year

def checkVehicleDestory(carNumber):
    data = os.listdir('data/')
    destory = []
    for s in data:
        if s.endswith('destory'):
            destory.append(s)
    for d in destory:
        if carNumber in d:
            return True
    return False

def CarForm(username, cnumber, cbrand, cmodel, ccolor, ischeck):
    type = ".vehicleRegister"
    rel_path = "data/" + cnumber + '.' + username + type
    file = open(rel_path, mode='w')

    file.write(
        username + "$" + cnumber + '$' + cbrand + "$" + cmodel + "$" + ccolor + "$" + ischeck + '$' + '0' + '$' + '0' + '$' + '0')
    file.close()




# Run the server
run(host=host, port=port)
