from bottle import route, get, run, post, request, static_file
import re

import requests

host_addr = "localhost"
backend_port = 8079
waf_port = 8078

backend_str = "http://{host}:{port}".format(host=host_addr, port=backend_port)
waf_string = "http://{address}:{port}".format(address=host_addr, port=waf_port) 


# -----------------------------------------------------------------------------
# This class loads html files from the "template" directory and formats them using Python.
# If you are unsure how this is working, just
class FrameEngine:
    def __init__(this,
                 template_path="templates/",
                 template_extension=".html",
                 **kwargs):
        this.template_path = template_path
        this.template_extension = template_extension
        this.global_renders = kwargs

    def load_template(this, filename):
        path = this.template_path + filename + this.template_extension
        file = open(path, 'r')
        text = ""
        for line in file:
            text += line
        file.close()
        return text

    def simple_render(this, template, **kwargs):
        template = template.format(**kwargs)
        return template

    def render(this, template, **kwargs):
        keys = this.global_renders.copy()  # Not the best way to do this, but backwards compatible from PEP448, in Python 3.5+ use keys = {**this.global_renters, **kwargs}
        keys.update(kwargs)
        template = this.simple_render(template, **keys)
        return template

    def load_and_render(this, filename, header="header", tailer="tailer", **kwargs):
        template = this.load_template(filename)
        rendered_template = this.render(template, **kwargs)
        rendered_template = this.load_template(header) + rendered_template
        rendered_template = rendered_template + this.load_template(tailer)
        return rendered_template


# -----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='img/')


# Allow CSS
@route('/css/<css>')
def serve_css(css):
    return static_file(css, root='css/')


# Allow javascript
@route('/js/<js>')
def serve_js(js):
    return static_file(js, root='js/')



# ----------------------------------------------------------------------------
#Generate a random port, and perhaps a cookie or two for everyone ;
def randomport(default, maxuser):
    
    miniload=default
    overload=default+maxuser
    
    
    for default in range(miniload, overload):

        #response = requests.post("{target}/api/check_existence/{port}".format(target=backend_str, port=str(default))

        potter="honeyport"+str(default)
        response = requests.post("{target}/api/check_existenceport/{port}".format(target=backend_str, port=potter))
        isExist = response.text
              
        if not isExist:
            #write_port("honeyport", str(default))
            response = requests.post("{target}/api/write_port/{honeyport}/{candyport}"
                .format(target=backend_str, honeyport="honeyport", candyport=str(default)))
            return default

        else:
            default+=1
    else:
       print ("our server is cureently overloaded, please try again later")  
# -----------------------------------------------------------------------------
#WAF Check attack
def check_attack(attack_vector):
        # Check for malicious code
        response = requests.post("{target}/waf/detect/{attack_vector}"
            .format(target=waf_string, attack_vector=attack_vector))
        
        # Rather than redirecting, you can attempt to sanitise the string
        attacked = response.text
        
        return attacked
#-----------------------------------------------------------------------------


# Check the login credentials
def check_login(username, password, authentication):
    
    login = False
    
    if check_attack(username) == "True":
        if check_attack(password) == "True":
            if check_attack(authentication) == "True":
                
                

                login = requests.post("{target}/api/check_login/{username}/{password}/{authentication}"
                    .format(target=backend_str, username=username, password=password, authentication=authentication)).text

                if login:
                    return "Logged in!", login
                else:
                    return "Incorrect detail", login
            else:
                return "you are attempting to attack our site, may fire rain upon you!", login
        else:
            return "you are attempting to attack our site, may fire rain upon you!", login
    else:
        return "you are attempting to attack our site, may fire rain upon you!", login


# -----------------------------------------------------------------------------
def check_password(username, password, confirm, email):
    valid = False
    if username == '':
        err_str = 'please enter a username'
        return err_str, valid
    if password != confirm:
        err_str = 'Confirm password is not identical to the password'
        return err_str, valid
    if len(password) < 8:
        err_str = 'password length must be at least 8 characters long'
        return err_str, valid
    if re.search(r'[a-z]', password) == False:
        err_str = 'password must contain at least one lowercase character'
        return err_str, valid
    if re.search(r'[A-Z]', password) == False:
        err_str = 'password must contain at least one uppercase character'
        return err_str, valid
    if re.search(r'[0-9]', password) == False:
        err_str = 'password must contains at least one number'
        return err_str, valid
    if password == username:
        err_str = 'password too similar to username'
        return err_str, valid


    r = re.compile('.*@.*.com')
    if r.match(email) is None:
        err_str = "Format of the email is not correct"
        return err_str, valid
    valid = True
    login_str = 'Success'
    return login_str, valid


# -----------------------------------------------------------------------------

# Check the register detail
def check_register(username, password, confirmPassword, email, type):
    
    if check_attack(username) == "True":
        if check_attack(password) == "True":
            if check_attack(confirmPassword) == "True":
                if check_attack(email) == "True":
                    

                

                    login_str, register = check_password(username, password, confirmPassword, email)

    
    # isExist = check_existence(username, ".txt")

                    response = requests.post("{target}/api/check_existence/{username}"
    	                .format(target=backend_str, username=username))

                    isExist = response.text

                    if isExist:
                        err_str = 'Username already exist'
                        return err_str, False
                    if register:
                        response = requests.post("{target}/api/useradd/{username}/{password}/{email}/{memberType}/{TFnumber}"
                            .format(target=backend_str, username=username, password=password, email=email, memberType=type, TFnumber = username[0] + username[-1]))

                    return login_str, register
                
                else:
                    return "you are attempting to attack our site, may fire rain upon you!", False
            else:
                return "you are attempting to attack our site, may fire rain upon you!", False
        else:
            return "you are attempting to attack our site, may fire rain upon you!", False
    else:
        return "you are attempting to attack our site, may fire rain upon you!", False            


def check_edit(username, password, confirmPassword, email, type):
    edit_str, edit = check_password(username, password, confirmPassword, email)
    if edit:
        response = requests.post("{target}/api/useradd/{username}/{password}/{email}/{memberType}/{TFnumber}"
            .format(target=backend_str, username=username, password=password, email=email, memberType=type, TFnumber = username[0] + username[-1]))

    return edit_str, edit


def check_license():

    response = requests.post("{target}/api/check_license"
    	.format(target=backend_str)).text
    if response:
        return "You successfully send the request", response
    else:
        # you already have a license
        return "You already have a license or applied a license", response



# -----------------------------------------------------------------------------
# Redirect to login
@route('/')
@route('/home')
def index():
    return fEngine.load_and_render("index")


# Display the login page
@get('/login')
def login():
    currentUser = requests.post("{target}/api/getCurrentUser"
	   .format(target=backend_str)).text

    if currentUser is not "":
        user = requests.post("{target}/api/userget/{username}"
    	   .format(target=backend_str, username=currentUser)).text
        info = user.split('$')
        return fEngine.load_and_render("profile", username=currentUser, email=info[1],
                                       type=info[2], auth=info[3])
    else:
        return fEngine.load_and_render("login")


# Attempt the login
@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    authentication = request.forms.get('authentication')
    err_str, login = check_login(username, password, authentication)
    if login:
        response = requests.post("{target}/api/setCurrentUser/{username}"
        	.format(target=backend_str, username=username))
        user = requests.post("{target}/api/userget/{username}"
    	   .format(target=backend_str, username=username)).text
        info = user.split('$')
        return fEngine.load_and_render("profile", username=username, email=info[1],
                                       type=info[2], auth=info[3])
    else:
        return fEngine.load_and_render("invalid", reason=err_str)


# Display the Main page
@get('/main')
def main():


    currentUser = requests.post("{target}/api/getCurrentUser"
	   .format(target=backend_str)).text

    if currentUser is not "":
        user = requests.post("{target}/api/userget/{username}"
    	   .format(target=backend_str, username=currentUser)).text
        info = user.split('$')
        memberType = info[2]
        if memberType == "road safety officers":
            return fEngine.load_and_render("main-officers")
        if memberType == "admin":
            return fEngine.load_and_render("main-admin")
        if memberType == "public":
            return fEngine.load_and_render("main-pubic")
        if memberType == "staff":
            return fEngine.load_and_render("main-staff")
    else:
        return fEngine.load_and_render("main")




# a temp site for fun
@post('/destory')
def destory():
    return fEngine.load_and_render("destory")

@post("/checkForm")
def check_form():
    return fEngine.load_reander("checkForm")    

# Attempt the sale
@post('/saleCar')
def do_saleCar():
    return fEngine.load_and_render("saleCar")


@post('/do_sale')
def do_sale():
    registration = request.forms.get("registration")
    purchaser = request.forms.get("purchaser")
    amount = request.forms.get("amount")

    response = requests.post("{target}/api/check_sale/{registration}/{purchaser}/{amount}"
    	.format(target=backend_str, registration=registration, purchaser=purchaser, amount=amount)).text

    if response:
        return fEngine.load_and_render("valid", flag="Infomation uploaded, wait the staff to apprrove")
    else:
        return fEngine.load_and_render("invalid", reason="Infomation invalid")


# Attempt the apply the license page
@post('/apply_License')
def go_apply_page():
    return fEngine.load_and_render("apply_License")


@post('/do_apply')
def do_apply():
    info_str, is_apply = check_license()
    if is_apply:
        return fEngine.load_and_render("valid", flag=info_str)
    else:
        return fEngine.load_and_render("invalid", reason=info_str)


# Attempt the renew the license page
@post('/renew_License')
def go_apply_page():
    return fEngine.load_and_render("renew_License")


@post('/do_renew')
def do_renew():

    response = requests.post("{target}/api/check_renew_license"
    	.format(target=backend_str)).text

    if response:
        return fEngine.load_and_render("valid", flag="You renew request has been send")
    else:
        return fEngine.load_and_render("invalid", reason="You can not renew for reasons")



# Display the logout page
@get('/logout')
def logout():
    response = requests.post("{target}/api/logOut"
        .format(target=backend_str))

    return fEngine.load_and_render("login")


# Display the register page
@get('/register')
def register():
    return fEngine.load_and_render("register")


# Attempt the register
@post('/register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirmPassword = request.forms.get('confirmPassword')
    email = request.forms.get('email')
    memberType = request.forms.get("member type")

    err_str, register = check_register(username, password, confirmPassword, email, memberType)

    if register:
        return fEngine.load_and_render("valid", flag=err_str)
    else:
        return fEngine.load_and_render("invalid", reason=err_str)


# show edit page
@get('/edit')
def show_edit():
    currentUser = requests.post("{target}/api/getCurrentUser"
	   .format(target=backend_str)).text
    return fEngine.load_and_render("edit", username=currentUser)

@post('/edit')
def do_edit():
    password = request.forms.get('password')
    confirmPassword = request.forms.get('confirmPassword')
    email = request.forms.get('email')
    memberType = request.forms.get("member type")

    currentUser = requests.post("{target}/api/getCurrentUser"
	   .format(target=backend_str)).text
    err_str, register = check_edit(currentUser, password, confirmPassword, email, memberType)
    if register:
        return fEngine.load_and_render("valid", flag=err_str)
    else:
        return fEngine.load_and_render("invalid", reason=err_str)

@post('/ApplyCarForm')
def do_CarForm():
    username = request.forms.get('UserName')
    carNumber = request.forms.get('carNumber')
    brand = request.forms.get('Brand')
    model = request.forms.get('Model')
    color = request.forms.get('Color')
    safetycheck = request.forms.get('SafetyCheck')

    isDestory = requests.post("{target}/api/check_car/{username}/{carNumber}/{brand}{model}/{color}/{safetycheck}"
    	.format(target=backend_str, username=username, carNumber=carNumber, brand=brand, model=model, color=color, safetycheck=safetycheck)).text

    if isDestory:
        return fEngine.load_and_render('invalid', reason='This vehicle is destoried')
    else:
        return fEngine.load_and_render('valid', flag="Wait for staff to check")


@get('/RL')
def RevokeLicense():
    return fEngine.load_and_render("RL")

@post('/CarForm')
def go_Carapply_page():
    return fEngine.load_and_render("carForm")



@get('/APLA')
def APLA():

    applylist = requests.post("{target}/api/APLA"
    	.format(target=backend_str)).text.split('$')
    applylist = applylist[:-1]

    if (len(applylist)) == 0:
        toreturn = '''<p>There is no user apply for license</p>'''
        return fEngine.load_and_render("APLA") + toreturn
    toreturn = '''<form action="/APLA" method="post">'''
    for apply in applylist:
        toreturn += apply
        toreturn += '''<select name="''' + apply + '''"><option value="approve">approve</option><option value="reject">reject</option></select></br>'''
    toreturn += '''<input value="submit" type="submit" /></form>'''
    return fEngine.load_and_render("APLA") + toreturn


@get('/ApproveVehicleRegister')
def ApproveVehicleRegister():
    approve = []

    applylist = requests.post("{target}/api/readApproveVehicleRegister"
    	.format(target=backend_str)).text.split('$')
    applylist = applylist[:-1]

    if (len(applylist)) == 0:
        toreturn = '''<p>There is no user register vehicle</p>'''
        return fEngine.load_and_render("ApproveVehicleRegister") + toreturn
    toreturn = '''<form action="/ApproveVehicleRegister" method="post">'''
    for apply in applylist:
        s = apply.split('.')
        cnumber = s[0]
        user = s[1]
        return_str = 'username: ' + user + ' car number: ' + cnumber
        toreturn += return_str
        toreturn += '''<select name="''' + cnumber + '''"><option value="approve">approve</option><option value="reject">reject</option></select></br>'''
    toreturn += '''<input value="submit" type="submit" /></form>'''
    return fEngine.load_and_render("ApproveVehicleRegister") + toreturn


@post('/ApproveVehicleRegister')
def do_ApproveVehicleRegister():

    approve = []

    applylist = requests.post("{target}/api/readApproveVehicleRegister"
    	.format(target=backend_str)).text.split('$')
    applylist = applylist[:-1]


    for apply in applylist:
        s = apply.split('.')
        cnumber=s[0]
        if request.forms.get(cnumber) == 'approve':
            approve.append(apply)
    for apply in approve:
        response = requests.post("{target}/api/approve/{apply}"
        	.format(target=backend_str, apply=apply))

    if (len(applylist)) == 0:
        toreturn = '''<p>There is no user register vehicle</p>'''
        return fEngine.load_and_render("ApproveVehicleRegister") + toreturn
    toreturn = '''<form action="/ApproveVehicleRegister" method="post">'''
    for apply in applylist:
        print(apply)
        s = apply.split('.')
        print(s[0],s[1])
        cnumber = s[0]
        user = s[1]
        return_str = 'username: ' + user + ' car number: ' + cnumber
        toreturn += return_str
        toreturn += '''<select name="''' + cnumber + '''"><option value="approve">approve</option><option value="reject">reject</option></select></br>'''
    toreturn += '''<input value="submit" type="submit" /></form>'''
    return fEngine.load_and_render("ApproveVehicleRegister") + toreturn


# Reset everything
@post('/reset')
def reset():
    response = requests.post("{target}/api/reset"
        .format(target=backend_str))
    return fEngine.load_and_render("index")


@get('/about')
def about():
    return fEngine.load_and_render("about")


# -----------------------------------------------------------------------------

fEngine = FrameEngine()
chosenone = randomport(8080, 100)
run(host=host_addr, port=chosenone)



# @get('/AP')
# def ApprovePayment():
#     data = os.listdir('data/')
#     vlist = []
#     paymentdict = {}
#     for d in data:
#         if d.endswith('.vehicle'):
#             vlist.append('data/' + d)
#     toreturn = None
#     for rel_path in vlist:
#         f = open(rel_path, 'r')
#         line = f.read()
#         f.close()
#         s = line.split('$')
#         if int(s[7]) != 0:
#             paymentdict[rel_path] = (s[0], s[1], s[7], s[8])
#     if (len(paymentdict)) == 0:
#         toreturn = '''<p>There is no user need to pay their fine</p>'''
#         return fEngine.load_and_render("ApproveVehicleRegister") + toreturn
#     toreturn = '''<form action="/AP" method="post">'''
#     for rel_path in paymentdict.keys():
#         return_str = 'username: ' + payment[rel_path][0] + ' car number: ' + payment[rel_path][1] + ' fine: ' + \
#                      payment[rel_path][2] + ' pay: ' + payment[rel_path][3]
#         toreturn += return_str
#         toreturn += '''<select name="''' + cnumber + '''"><option value="approve">approve</option><option value="reject">reject</option></select></br>'''
#     toreturn += '''<input value="submit" type="submit" /></form>'''
#     return fEngine.load_and_render("AP") + toreturn
#
#
# @post('/AP')
# def ApprovePayment():
#     approve = []
#     data = os.listdir('data/')
#     vlist = []
#     paymentdict = {}
#     for d in data:
#         if d.endswith('.vehicle'):
#             vlist.append('data/' + d)
#     toreturn = None
#     for rel_path in vlist:
#         f = open(rel_path, 'r')
#         line = f.read()
#         f.close()
#         s = line.split('$')
#         if int(s[7]) != 0:
#             paymentdict[rel_path] = (s[0], s[1], s[7], s[8])
#
#     if (len(paymentdict)) == 0:
#         toreturn = '''<p>There is no user need to pay their fine</p>'''
#         return fEngine.load_and_render("ApproveVehicleRegister") + toreturn
#     toreturn = '''<form action="/AP" method="post">'''
#     for rel_path in paymentdict.keys():
#         return_str = 'username: ' + payment[rel_path][0] + ' car number: ' + payment[rel_path][1] + ' fine: ' + \
#                      payment[rel_path][2] + ' pay: ' + payment[rel_path][3]
#         toreturn += return_str
#         toreturn += '''<select name="''' + cnumber + '''"><option value="approve">approve</option><option value="reject">reject</option></select></br>'''
#     toreturn += '''<input value="submit" type="submit" /></form>'''
#     return fEngine.load_and_render("AP") + toreturn
#
