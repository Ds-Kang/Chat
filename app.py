from tornado.ioloop import IOLoop
from tornado.web import Application,RequestHandler,url
import myutil
import time
import pickle

history = []

class user:
    def __init_(self,name,pw):
        self.name=name;
        self.pw=pw;

class MainHandler(RequestHandler):
    def get(self):
        self.render('main.html')
    def post(self):
        name = self.get_body_argument('name')
        pw = self.get_body_argument('pw')
        check = self.get_body_argument('check')
        if(pw!=check):
            self.render('register')
            return
        self.render('main.html')

class JoinHandler(RequestHandler):
    def post(self):
        name = self.get_body_argument('name')
        pw = self.get_body_argument('pw')
        self.render('join.html', name=name)
class RegisterHandler(RequestHandler):
    def get(self):
        self.render('register.html')
        
class LoginHandler(RequestHandler):
    def get(self):
        self.render('login.html')
class TalkHandler(RequestHandler):
    def post(self):
        global history
        name = self.get_body_argument('name')
        mesg = self.get_body_argument('mesg')
        ip = self.request.remote_ip
        d = {'name': name, 'mesg': mesg, 'time':time.asctime(),'ip': ip}
        history.append(d)
        self.render('talk.html', name=name, history=history)
class AdminHandler(RequestHandler):
    def get(self):
        global history
        self.render('admin.html', history=history)
    def post(self):
        global history
        cmd = self.get_body_argument('cmd')
        if cmd == 'dump':
            f = open('talk.hist', 'wb')
            pickle.dump(history,f)
            f.close()
        elif cmd == 'load':
            f = open('talk.hist', 'rb')
            history = pickle.load(f)
            f.close()
        self.render('admin.html', history=history)
def make_app():
    handlers = []
    handlers.append(url(r"/",MainHandler))
    handlers.append(url(r'/join',JoinHandler))
    handlers.append(url(r'/talk',TalkHandler))
    handlers.append(url(r'/admin',AdminHandler))
    handlers.append(url(r'/register',RegisterHandler))
    handlers.append(url(r'/login',LoginHandler))
    
    return Application(handlers)
if __name__ == "__main__":
    fs = myutil.FastStop()
    fs.enable()
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()
