import sys
import sqlite3

from random import choice
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtWidgets import QLineEdit, QApplication
from PyQt5.QtGui import QPixmap

connection = sqlite3.connect('DB/reglog.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Data
               (ID INT, Login TEXT, Password TEXT, Avatar TEXT, LevelsComplite TEXT NOT NULL)''')

count = cursor.execute("""SELECT COUNT(ID) FROM Data""").fetchall()

for k in count:
    countid = k[0]

connection.commit()


class RegLogED(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setGeometry(750, 400, 181, 220)
        self.setWindowTitle('Login')

        self.backgrl = QPixmap('Pictures/backgroundreglog.png')
        self.image_backgrl = QLabel(self)
        self.image_backgrl.setPixmap(self.backgrl)
        self.image_backgrl.resize(181, 220)

        self.labeloglog = QLabel('Введите логин', self)
        self.labeloglog.move(30, 10)

        self.labepaslog = QLabel('Введите пароль', self)
        self.labepaslog.move(30, 70)

        self.labelerrorlog = QLabel(self)
        self.labelerrorlog.move(16, 123)
        self.labelerrorlog.resize(151, 20)
        self.labelerrorlog.setStyleSheet("color: rgb(255, 30, 50)")

        self.textlogin = QLineEdit(self)
        self.textlogin.move(30, 30)
        self.textlogin.resize(121, 31)

        self.textpassword = QLineEdit(self)
        self.textpassword.move(30, 90)
        self.textpassword.resize(121, 31)
        self.textpassword.setEchoMode(QLineEdit.Password)

        self.pblogin = QPushButton('Войти', self)
        self.pblogin.move(50, 147)
        self.pblogin.resize(81, 31)
        self.pblogin.clicked.connect(self.next)

        self.pbregister = QPushButton('Регистрация', self)
        self.pbregister.move(50, 180)
        self.pbregister.resize(81, 31)
        self.pbregister.clicked.connect(self.reg)

    def next(self):
        self.levels = cursor.execute(f"""SELECT LevelsComplite FROM Data WHERE Login = '{self.textlogin.text()}'""")
        global lstcomlvl
        lstcomlvl = []
        for flesports in self.levels:
            lstcomlvl.append(*flesports)

        ans = cursor.execute("""SELECT Login FROM Data""").fetchall()

        lst_log = []
        for i in ans:
            lst_log.append(*i)

        self.passw = cursor.execute(f"""SELECT Password FROM Data 
                                    WHERE Login = '{self.textlogin.text()}'""")
        for m in self.passw:
            self.passw = m[0]
        if self.textlogin.text() in lst_log and self.passw == self.textpassword.text():
            global login
            login = self.textlogin.text()
            self.hide()
            self.s = StartED()
            self.s.show()
        elif not self.textlogin.text() and not self.textpassword.text():
            self.labelerrorlog.move(30, 123)
            self.labelerrorlog.setText('Введите логин и пароль')
        elif not self.textlogin.text():
            self.labelerrorlog.move(53, 123)
            self.labelerrorlog.setText('Введите логин')
        elif not self.textpassword.text():
            self.labelerrorlog.move(53, 123)
            self.labelerrorlog.setText('Введите пароль')
        elif self.textlogin.text() not in lst_log:
            self.labelerrorlog.move(16, 123)
            self.labelerrorlog.setText('Пользователя не существует')
        elif self.passw != self.textpassword.text():
            self.labelerrorlog.move(46, 123)
            self.labelerrorlog.setText('Неверный пароль')

    def reg(self):
        self.hide()
        self.regwin = RegisterED()
        self.regwin.show()


class RegisterED(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setGeometry(680, 380, 309, 274)
        self.setWindowTitle('Регистрация')

        #фон и аватарка
        self.backg = QPixmap('Pictures/backgroundreg.png')
        self.image_backg = QLabel(self)
        self.image_backg.setPixmap(self.backg)

        self.fname = 'AvatarPics/avatarka.jpg'
        self.pixbeh = QPixmap(self.fname)
        self.image_pixbeh = QLabel(self)
        self.image_pixbeh.resize(90, 90)
        self.image_pixbeh.move(185, 35)
        self.image_pixbeh.setPixmap(self.pixbeh)
        self.image_pixbeh.setScaledContents(True)

        self.register_ok = QPushButton("Зарегистрироваться", self)
        self.register_ok.move(20, 230)
        self.register_ok.resize(121, 31)
        self.register_ok.clicked.connect(self.next) #пока что

        self.backs = QPushButton('Вернуться', self)
        self.backs.move(170, 230)
        self.backs.resize(121, 31)
        self.backs.clicked.connect(self.logag) #тоже временно

        self.avatar = QPushButton("Выбрать аватар", self)
        self.avatar.move(170, 160)
        self.avatar.resize(121, 31)
        self.avatar.clicked.connect(self.fnamefun)

        self.labellog = QLabel('Введите логин', self)
        self.labellog.move(20, 0)
        self.labellog.resize(191, 16)

        self.labellogif = QLabel('(не менее 4 символов)', self)
        self.labellogif.move(20, 15)

        self.labelpas = QLabel('Введите пароль', self)
        self.labelpas.move(20, 70)
        self.labelpas.resize(191, 16)

        self.labelpasif = QLabel('(не менее 8 символов)', self)
        self.labelpasif.move(20, 85)

        self.labelpasag = QLabel('Повторите пароль', self)
        self.labelpasag.move(20, 140)
        self.labelpasag.resize(101, 16)

        self.labelerror = QLabel(self)
        self.labelerror.move(22, 210)
        self.labelerror.resize(271, 20)
        self.labelerror.setStyleSheet("color: rgb(255, 30, 50)")

        self.linelogin = QLineEdit(self)
        self.linelogin.move(20, 30)
        self.linelogin.resize(121, 31)

        self.linepas = QLineEdit(self)
        self.linepas.move(20, 100)
        self.linepas.resize(121, 31)
        self.linepas.setEchoMode(QLineEdit.Password)

        self.linepasag = QLineEdit(self)
        self.linepasag.move(20, 160)
        self.linepasag.resize(121, 31)
        self.linepasag.setEchoMode(QLineEdit.Password)

    def next(self):
        ans = cursor.execute("""SELECT Login FROM Data""").fetchall()

        lst_log = []
        for i in ans:
            lst_log.append(*i)

        if len(self.linelogin.text()) >= 4 and len(self.linepas.text()) >= 8 and self.linepas.text() \
                == self.linepasag.text() and self.linelogin.text() not in lst_log\
                and " " not in self.linelogin.text() and " " not in self.linepas.text():
            cursor.execute(f'''INSERT INTO Data (ID, Login, Password, Avatar, LevelsComplite)
            VALUES ({int(countid) + 1}, "{self.linelogin.text()}", "{self.linepas.text()}", "{self.fname}", "0")''')
            connection.commit()
            self.hide()
            self.s1 = RegLogED()
            self.s1.show()
        elif ' ' in self.linelogin.text() or ' ' in self.linepas.text():
            self.labelerror.setText('Использован пробел, уберите его!')
        elif self.linelogin.text() in lst_log:
            self.labelerror.setText('Пользователь с таким логином уже существует')
        elif self.linepas.text() != self.linepasag.text():
            self.labelerror.setText('Пароли не совпадают')
        elif len(self.linelogin.text()) < 4 and len(self.linepas.text()) < 8:
            self.labelerror.setText('Логин и пароль меньше допустимой длины')
        elif len(self.linelogin.text()) < 4:
            self.labelerror.setText('Логин короче 4 символов')
        elif len(self.linepas.text()) < 8:
            self.labelerror.setText('Пароль короче 8 символов')

    def logag(self):
        self.hide()
        self.s2 = RegLogED()
        self.s2.show()

    def fnamefun(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать аватар', '', '(*.jpg);;(*.png);;(*.jpeg)')[0]
        self.pixbeh = QPixmap(self.fname)
        self.image_pixbeh.setScaledContents(True)
        self.image_pixbeh.setPixmap(self.pixbeh)


class StartED(QWidget):           #берет окно UI для выбором режима.
    def __init__(self):
        super().__init__()
        self.pixbeh = QPixmap('Pictures/pixbeh.png')
        self.image_pixbeh = QLabel(self)
        self.image_pixbeh.resize(400, 350)
        self.image_pixbeh.setPixmap(self.pixbeh)
        uic.loadUi('UIC/start.ui', self)
        self.pushb1.clicked.connect(self.choose_lvl)
        self.pushb2.clicked.connect(self.user_change)
        self.pushb3.clicked.connect(self.exit)


    def choose_lvl(self):         #после нажатия на "начать", открывается окно выбора уровня.
        self.hide()
        self.w2 = ChooseED()
        self.w2.show()

    def user_change(self):        #пока ничего не делает.
        self.hide()
        self.log = RegLogED()
        self.log.show()

    def exit(self):                #при нажатии на "выход", закрывается приложение.
        sys.exit(app.exec_())


class ChooseED(QWidget):           #создает окно выбора уровня
    def __init__(self, *args):
        super().__init__()
        self.beh = QPixmap('Pictures/beh.png')
        self.image_beh = QLabel(self)
        self.image_beh.resize(400, 350)
        self.image_beh.setPixmap(self.beh)

        self.bind = cursor.execute(f"""SELECT Avatar FROM Data
                                    WHERE Login = '{login}'""")
        for g in self.bind:
            self.bind = g[0]

        self.ava = QPixmap(self.bind)
        self.image_ava = QLabel(self)
        self.image_ava.resize(50, 50)
        self.image_ava.move(12, 12)
        self.image_ava.setPixmap(self.ava)
        self.image_ava.setScaledContents(True)

        uic.loadUi('UIC/choose.ui', self)
        self.back.clicked.connect(self.back_to_start)
        self.pblevel1.clicked.connect(self.level1)
        self.pblevel2.clicked.connect(self.level2)
        self.pblevel3.clicked.connect(self.level3)
        self.pblevel4.clicked.connect(self.level4)
        self.pblevel5.clicked.connect(self.level5)
        self.pblevel6.clicked.connect(self.level6)
        self.pblevel7.clicked.connect(self.level7)
        self.pronounse.clicked.connect(self.wordslearb)

        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()

        self.ansik = cursor.execute(f"""SELECT LevelsComplite FROM Data WHERE Login = '{login}'""")
        for i in self.ansik:
            self.ansik = ''.join(i)

        if "1" in self.ansik:
            self.label.show()

        if "2" in self.ansik:
            self.label_2.show()

        if "3" in self.ansik:
            self.label_3.show()

        if "4" in self.ansik:
            self.label_4.show()

        if "5" in self.ansik:
            self.label_5.show()

        if "6" in self.ansik:
            self.label_6.show()

        if "7" in self.ansik:
            self.label_7.show()

    def back_to_start(self):            #возвращение в главное меню.
        self.hide()
        self.w = StartED()
        self.w.show()

    def wordslearb(self):               #перекидывает на таблицу со словами для обучения
        self.hide()
        self.w = Learn_window()
        self.w.show()

    def level1(self):                   #перекидывает на первый уровень
        self.hide()
        self.lvl1 = Level1()
        self.lvl1.show()

    def level2(self):                   #перекидывает на второй уровень
        self.hide()
        self.lvl2 = Level2()
        self.lvl2.show()

    def level3(self):                   #перекидывает на третий уровень
        self.hide()
        self.lvl3 = Level3()
        self.lvl3.show()

    def level4(self):                   #перекидывает на четвертый уровень
        self.hide()
        self.lvl4 = Level4()
        self.lvl4.show()

    def level5(self):                   #перекидывает на пятый уровень
        self.hide()
        self.lvl5 = Level5()
        self.lvl5.show()

    def level6(self):                   #перекидывает на шетсой уровень
        self.hide()
        self.lvl6 = Level6()
        self.lvl6.show()

    def level7(self):                   #перекидывает на седьмой уровень
        self.hide()
        self.lvl7 = Level7()
        self.lvl7.show()


class Learn_window(QWidget):               #берет окно UI, в котором рисует таблицу слов для обучения
    def __init__(self):
        super().__init__()
        self.wrdlrn = QPixmap('Pictures/wordlearn.jpg')
        self.image_wrdlrn = QLabel(self)
        self.image_wrdlrn.resize(750, 480)
        self.image_wrdlrn.move(0, 0)
        self.image_wrdlrn.setPixmap(self.wrdlrn)
        uic.loadUi('UIC/wordslearn.ui', self)
        self.pushback.clicked.connect(self.back_to_start)

    def back_to_start(self):           #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class Level1(QWidget):                  #создает первый уровень

    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):                   #создание всех виджетов в окне
        self.wordslvl1 = {'I': 'Я', 'You': 'Ты', 'He': 'Он', 'She': 'Она', 'It': 'Он, Она, Они', 'We': 'Мы'}
        self.wordvalue = [i for i in self.wordslvl1.values()]
        self.wordkey = [i for i in self.wordslvl1.keys()]
        self.pic_hp = ['Pictures/hp0.png', 'Pictures/hp1of6.png', 'Pictures/hp2of6.png', 'Pictures/hp3of6.png',
                       'Pictures/hp4of6.png', 'Pictures/hp5of6.png', 'Pictures/hp100.png']

        self.setGeometry(640, 270, 400, 450)
        self.setWindowTitle('LEVEL 1')

        self.place = QPixmap('Pictures/place.png')
        self.image_place = QLabel(self)
        self.image_place.resize(400, 250)
        self.image_place.setPixmap(self.place)

        self.placedown = QPixmap('Pictures/placedown.png')
        self.image_placedown = QLabel(self)
        self.image_placedown.resize(400, 250)
        self.image_placedown.move(0, 250)
        self.image_placedown.setPixmap(self.placedown)

        self.player = QPixmap('Pictures/player.png')
        self.image_player = QLabel(self)
        self.image_player.resize(400, 250)
        self.image_player.move(55, 61)
        self.image_player.setPixmap(self.player)

        self.boss = QPixmap('Pictures/boss.png')
        self.image_boss = QLabel(self)
        self.image_boss.resize(400, 250)
        self.image_boss.move(280, 66)
        self.image_boss.setPixmap(self.boss)

        self.count = 6
        self.hp = QPixmap(self.pic_hp[self.count])
        self.image_hp = QLabel(self)
        self.image_hp.resize(400, 50)
        self.image_hp.move(277, 15)
        self.image_hp.setPixmap(self.hp)

        self.choice_word = choice(self.wordkey)
        self.label_word = QLabel(self.choice_word, self)
        self.label_word.move(10, 215)
        self.label_word.resize(150, 20)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_word.setFont(font)
        self.label_word.setStyleSheet("color: rgb(128, 166, 255)")

        self.tipword = QLabel("Переведите местоименее выше", self)
        self.tipword.move(10, 250)
        self.tipword.resize(200, 15)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.tipword.setFont(font2)
        self.tipword.setStyleSheet("color: rgb(128, 166, 255)")

        self.count_los = 0
        self.label_los = QLabel(f'Ошибок: {self.count_los}', self)
        self.label_los.move(320, 420)
        self.label_los.resize(100, 15)
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(10)
        self.label_los.setFont(self.font1)
        self.label_los.setStyleSheet("color: rgb(90, 146, 100)")

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)
        self.back.setStyleSheet("color: rgb(255, 255, 255); background: rgb(68, 49, 32);")

        self.pushbuttonword1 = QPushButton(self.wordvalue[0], self)
        self.pushbuttonword1.move(50, 300)
        self.pushbuttonword1.resize(100, 50)
        self.pushbuttonword1.clicked.connect(self.pushbut1)
        self.pushbuttonword1.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword2 = QPushButton(self.wordvalue[1], self)
        self.pushbuttonword2.move(50, 350)
        self.pushbuttonword2.resize(100, 50)
        self.pushbuttonword2.clicked.connect(self.pushbut2)
        self.pushbuttonword2.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword3 = QPushButton(self.wordvalue[2], self)
        self.pushbuttonword3.move(150, 300)
        self.pushbuttonword3.resize(100, 50)
        self.pushbuttonword3.clicked.connect(self.pushbut3)
        self.pushbuttonword3.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword4 = QPushButton(self.wordvalue[3], self)
        self.pushbuttonword4.move(150, 350)
        self.pushbuttonword4.resize(100, 50)
        self.pushbuttonword4.clicked.connect(self.pushbut4)
        self.pushbuttonword4.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword5 = QPushButton(self.wordvalue[4], self)
        self.pushbuttonword5.move(250, 300)
        self.pushbuttonword5.resize(100, 50)
        self.pushbuttonword5.clicked.connect(self.pushbut5)
        self.pushbuttonword5.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword6 = QPushButton(self.wordvalue[5], self)
        self.pushbuttonword6.move(250, 350)
        self.pushbuttonword6.resize(100, 50)
        self.pushbuttonword6.clicked.connect(self.pushbut6)
        self.pushbuttonword6.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

    def pushbut1(self):               #при нажатии на первую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl1[self.choice_word] == self.pushbuttonword1.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword1.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("1")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut2(self):               #при нажатии на вторую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl1[self.choice_word] == self.pushbuttonword2.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword2.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("1")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut3(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl1[self.choice_word] == self.pushbuttonword3.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword3.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("1")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut4(self):            #при нажатии на четвертую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl1[self.choice_word] == self.pushbuttonword4.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword4.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("1")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut5(self):               #при нажатии на пятую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl1[self.choice_word] == self.pushbuttonword5.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword5.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("1")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut6(self):               #при нажатии на шестую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl1[self.choice_word] == self.pushbuttonword6.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword6.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("1")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def back_to_start(self):               #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class Level2(QWidget):                     #создает второй уровень
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.wordslvl2 = {'You': 'Вы', 'They': 'Они', 'Me': 'Мне, меня', 'Him': 'Его, ему', 'Her': 'Ей, её',
                          'It': 'Его, ее, ему'}
        self.wordvalue = [i for i in self.wordslvl2.values()]
        self.wordkey = [i for i in self.wordslvl2.keys()]
        self.pic_hp = ['Pictures/hp0.png', 'Pictures/hp1of6.png', 'Pictures/hp2of6.png', 'Pictures/hp3of6.png',
                       'Pictures/hp4of6.png', 'Pictures/hp5of6.png', 'Pictures/hp100.png']

        self.setGeometry(640, 270, 400, 450)
        self.setWindowTitle('LEVEL 2')

        self.place = QPixmap('Pictures/place.png')
        self.image_place = QLabel(self)
        self.image_place.resize(400, 250)
        self.image_place.setPixmap(self.place)

        self.placedown = QPixmap('Pictures/placedown.png')
        self.image_placedown = QLabel(self)
        self.image_placedown.resize(400, 250)
        self.image_placedown.move(0, 250)
        self.image_placedown.setPixmap(self.placedown)

        self.player = QPixmap('Pictures/player.png')
        self.image_player = QLabel(self)
        self.image_player.resize(400, 250)
        self.image_player.move(55, 61)
        self.image_player.setPixmap(self.player)

        self.boss = QPixmap('Pictures/boss.png')
        self.image_boss = QLabel(self)
        self.image_boss.resize(400, 250)
        self.image_boss.move(280, 66)
        self.image_boss.setPixmap(self.boss)

        self.count = 6
        self.hp = QPixmap(self.pic_hp[self.count])
        self.image_hp = QLabel(self)
        self.image_hp.resize(400, 50)
        self.image_hp.move(277, 15)
        self.image_hp.setPixmap(self.hp)

        self.choice_word = choice(self.wordkey)
        self.label_word = QLabel(self.choice_word, self)
        self.label_word.move(10, 215)
        self.label_word.resize(150, 20)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_word.setFont(font)
        self.label_word.setStyleSheet("color: rgb(128, 166, 255)")

        self.tipword = QLabel("Переведите местоименее выше", self)
        self.tipword.move(10, 250)
        self.tipword.resize(200, 15)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.tipword.setFont(font2)
        self.tipword.setStyleSheet("color: rgb(128, 166, 255)")

        self.count_los = 0
        self.label_los = QLabel(f'Ошибок: {self.count_los}', self)
        self.label_los.move(320, 420)
        self.label_los.resize(100, 15)
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(10)
        self.label_los.setFont(self.font1)
        self.label_los.setStyleSheet("color: rgb(90, 146, 100)")

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)
        self.back.setStyleSheet("color: rgb(255, 255, 255); background: rgb(68, 49, 32);")

        self.pushbuttonword1 = QPushButton(self.wordvalue[0], self)
        self.pushbuttonword1.move(50, 300)
        self.pushbuttonword1.resize(100, 50)
        self.pushbuttonword1.clicked.connect(self.pushbut1)
        self.pushbuttonword1.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword2 = QPushButton(self.wordvalue[1], self)
        self.pushbuttonword2.move(50, 350)
        self.pushbuttonword2.resize(100, 50)
        self.pushbuttonword2.clicked.connect(self.pushbut2)
        self.pushbuttonword2.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword3 = QPushButton(self.wordvalue[2], self)
        self.pushbuttonword3.move(150, 300)
        self.pushbuttonword3.resize(100, 50)
        self.pushbuttonword3.clicked.connect(self.pushbut3)
        self.pushbuttonword3.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword4 = QPushButton(self.wordvalue[3], self)
        self.pushbuttonword4.move(150, 350)
        self.pushbuttonword4.resize(100, 50)
        self.pushbuttonword4.clicked.connect(self.pushbut4)
        self.pushbuttonword4.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword5 = QPushButton(self.wordvalue[4], self)
        self.pushbuttonword5.move(250, 300)
        self.pushbuttonword5.resize(100, 50)
        self.pushbuttonword5.clicked.connect(self.pushbut5)
        self.pushbuttonword5.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword6 = QPushButton(self.wordvalue[5], self)
        self.pushbuttonword6.move(250, 350)
        self.pushbuttonword6.resize(100, 50)
        self.pushbuttonword6.clicked.connect(self.pushbut6)
        self.pushbuttonword6.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

    def pushbut1(self):               #при нажатии на первую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl2[self.choice_word] == self.pushbuttonword1.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword1.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("2")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut2(self):               #при нажатии на вторую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl2[self.choice_word] == self.pushbuttonword2.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword2.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("2")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut3(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl2[self.choice_word] == self.pushbuttonword3.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword3.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("2")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut4(self):            #при нажатии на четвертую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl2[self.choice_word] == self.pushbuttonword4.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword4.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("2")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut5(self):               #при нажатии на пятую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl2[self.choice_word] == self.pushbuttonword5.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword5.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("2")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut6(self):               #при нажатии на шестую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl2[self.choice_word] == self.pushbuttonword6.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword6.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("2")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def back_to_start(self):               #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class Level3(QWidget):                     #создает третий уровень
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.wordslvl3 = {'Us': 'Нам, нас', 'You': 'Тебе, тебя', 'Them': 'Их, им',
                          'My': 'Мой', 'Your': 'Твой', 'Him': 'Его'}
        self.wordvalue = [i for i in self.wordslvl3.values()]
        self.wordkey = [i for i in self.wordslvl3.keys()]
        self.pic_hp = ['Pictures/hp0.png', 'Pictures/hp1of6.png', 'Pictures/hp2of6.png', 'Pictures/hp3of6.png',
                       'Pictures/hp4of6.png', 'Pictures/hp5of6.png', 'Pictures/hp100.png']

        self.setGeometry(640, 270, 400, 450)
        self.setWindowTitle('LEVEL 3')

        self.place = QPixmap('Pictures/place.png')
        self.image_place = QLabel(self)
        self.image_place.resize(400, 250)
        self.image_place.setPixmap(self.place)

        self.placedown = QPixmap('Pictures/placedown.png')
        self.image_placedown = QLabel(self)
        self.image_placedown.resize(400, 250)
        self.image_placedown.move(0, 250)
        self.image_placedown.setPixmap(self.placedown)

        self.player = QPixmap('Pictures/player.png')
        self.image_player = QLabel(self)
        self.image_player.resize(400, 250)
        self.image_player.move(55, 61)
        self.image_player.setPixmap(self.player)

        self.boss = QPixmap('Pictures/boss.png')
        self.image_boss = QLabel(self)
        self.image_boss.resize(400, 250)
        self.image_boss.move(280, 66)
        self.image_boss.setPixmap(self.boss)

        self.count = 6
        self.hp = QPixmap(self.pic_hp[self.count])
        self.image_hp = QLabel(self)
        self.image_hp.resize(400, 50)
        self.image_hp.move(277, 15)
        self.image_hp.setPixmap(self.hp)

        self.choice_word = choice(self.wordkey)
        self.label_word = QLabel(self.choice_word, self)
        self.label_word.move(10, 215)
        self.label_word.resize(150, 20)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_word.setFont(font)
        self.label_word.setStyleSheet("color: rgb(128, 166, 255)")

        self.tipword = QLabel("Переведите местоименее выше", self)
        self.tipword.move(10, 250)
        self.tipword.resize(200, 15)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.tipword.setFont(font2)
        self.tipword.setStyleSheet("color: rgb(128, 166, 255)")

        self.count_los = 0
        self.label_los = QLabel(f'Ошибок: {self.count_los}', self)
        self.label_los.move(320, 420)
        self.label_los.resize(100, 15)
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(10)
        self.label_los.setFont(self.font1)
        self.label_los.setStyleSheet("color: rgb(90, 146, 100)")

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)
        self.back.setStyleSheet("color: rgb(255, 255, 255); background: rgb(68, 49, 32);")

        self.pushbuttonword1 = QPushButton(self.wordvalue[0], self)
        self.pushbuttonword1.move(50, 300)
        self.pushbuttonword1.resize(100, 50)
        self.pushbuttonword1.clicked.connect(self.pushbut1)
        self.pushbuttonword1.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword2 = QPushButton(self.wordvalue[1], self)
        self.pushbuttonword2.move(50, 350)
        self.pushbuttonword2.resize(100, 50)
        self.pushbuttonword2.clicked.connect(self.pushbut2)
        self.pushbuttonword2.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword3 = QPushButton(self.wordvalue[2], self)
        self.pushbuttonword3.move(150, 300)
        self.pushbuttonword3.resize(100, 50)
        self.pushbuttonword3.clicked.connect(self.pushbut3)
        self.pushbuttonword3.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword4 = QPushButton(self.wordvalue[3], self)
        self.pushbuttonword4.move(150, 350)
        self.pushbuttonword4.resize(100, 50)
        self.pushbuttonword4.clicked.connect(self.pushbut4)
        self.pushbuttonword4.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword5 = QPushButton(self.wordvalue[4], self)
        self.pushbuttonword5.move(250, 300)
        self.pushbuttonword5.resize(100, 50)
        self.pushbuttonword5.clicked.connect(self.pushbut5)
        self.pushbuttonword5.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword6 = QPushButton(self.wordvalue[5], self)
        self.pushbuttonword6.move(250, 350)
        self.pushbuttonword6.resize(100, 50)
        self.pushbuttonword6.clicked.connect(self.pushbut6)
        self.pushbuttonword6.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

    def pushbut1(self):               #при нажатии на первую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl3[self.choice_word] == self.pushbuttonword1.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword1.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("3")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut2(self):               #при нажатии на вторую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl3[self.choice_word] == self.pushbuttonword2.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword2.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("3")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut3(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl3[self.choice_word] == self.pushbuttonword3.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword3.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("3")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut4(self):            #при нажатии на четвертую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl3[self.choice_word] == self.pushbuttonword4.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword4.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("3")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut5(self):               #при нажатии на пятую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl3[self.choice_word] == self.pushbuttonword5.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword5.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("3")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut6(self):               #при нажатии на шестую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl3[self.choice_word] == self.pushbuttonword6.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword6.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("3")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def back_to_start(self):               #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class Level4(QWidget):                     #создает четвертый уровень
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.wordslvl4 = {'Her': 'Её', 'You': 'Вам, вас', 'Its': 'Его, её', 'Our': 'Наш', 'Your': 'Ваш', 'Their': 'Их'}
        self.wordvalue = [i for i in self.wordslvl4.values()]
        self.wordkey = [i for i in self.wordslvl4.keys()]
        self.pic_hp = ['Pictures/hp0.png', 'Pictures/hp1of6.png', 'Pictures/hp2of6.png', 'Pictures/hp3of6.png',
                       'Pictures/hp4of6.png', 'Pictures/hp5of6.png', 'Pictures/hp100.png']

        self.setGeometry(640, 270, 400, 450)
        self.setWindowTitle('LEVEL 4')

        self.place = QPixmap('Pictures/place.png')
        self.image_place = QLabel(self)
        self.image_place.resize(400, 250)
        self.image_place.setPixmap(self.place)

        self.placedown = QPixmap('Pictures/placedown.png')
        self.image_placedown = QLabel(self)
        self.image_placedown.resize(400, 250)
        self.image_placedown.move(0, 250)
        self.image_placedown.setPixmap(self.placedown)

        self.player = QPixmap('Pictures/player.png')
        self.image_player = QLabel(self)
        self.image_player.resize(400, 250)
        self.image_player.move(55, 61)
        self.image_player.setPixmap(self.player)

        self.boss = QPixmap('Pictures/boss.png')
        self.image_boss = QLabel(self)
        self.image_boss.resize(400, 250)
        self.image_boss.move(280, 66)
        self.image_boss.setPixmap(self.boss)

        self.count = 6
        self.hp = QPixmap(self.pic_hp[self.count])
        self.image_hp = QLabel(self)
        self.image_hp.resize(400, 50)
        self.image_hp.move(277, 15)
        self.image_hp.setPixmap(self.hp)

        self.choice_word = choice(self.wordkey)
        self.label_word = QLabel(self.choice_word, self)
        self.label_word.move(10, 215)
        self.label_word.resize(150, 20)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_word.setFont(font)
        self.label_word.setStyleSheet("color: rgb(128, 166, 255)")

        self.tipword = QLabel("Переведите местоименее выше", self)
        self.tipword.move(10, 250)
        self.tipword.resize(200, 15)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.tipword.setFont(font2)
        self.tipword.setStyleSheet("color: rgb(128, 166, 255)")

        self.count_los = 0
        self.label_los = QLabel(f'Ошибок: {self.count_los}', self)
        self.label_los.move(320, 420)
        self.label_los.resize(100, 15)
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(10)
        self.label_los.setFont(self.font1)
        self.label_los.setStyleSheet("color: rgb(90, 146, 100)")

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)
        self.back.setStyleSheet("color: rgb(255, 255, 255); background: rgb(68, 49, 32);")

        self.pushbuttonword1 = QPushButton(self.wordvalue[0], self)
        self.pushbuttonword1.move(50, 300)
        self.pushbuttonword1.resize(100, 50)
        self.pushbuttonword1.clicked.connect(self.pushbut1)
        self.pushbuttonword1.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword2 = QPushButton(self.wordvalue[1], self)
        self.pushbuttonword2.move(50, 350)
        self.pushbuttonword2.resize(100, 50)
        self.pushbuttonword2.clicked.connect(self.pushbut2)
        self.pushbuttonword2.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword3 = QPushButton(self.wordvalue[2], self)
        self.pushbuttonword3.move(150, 300)
        self.pushbuttonword3.resize(100, 50)
        self.pushbuttonword3.clicked.connect(self.pushbut3)
        self.pushbuttonword3.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword4 = QPushButton(self.wordvalue[3], self)
        self.pushbuttonword4.move(150, 350)
        self.pushbuttonword4.resize(100, 50)
        self.pushbuttonword4.clicked.connect(self.pushbut4)
        self.pushbuttonword4.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword5 = QPushButton(self.wordvalue[4], self)
        self.pushbuttonword5.move(250, 300)
        self.pushbuttonword5.resize(100, 50)
        self.pushbuttonword5.clicked.connect(self.pushbut5)
        self.pushbuttonword5.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword6 = QPushButton(self.wordvalue[5], self)
        self.pushbuttonword6.move(250, 350)
        self.pushbuttonword6.resize(100, 50)
        self.pushbuttonword6.clicked.connect(self.pushbut6)
        self.pushbuttonword6.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

    def pushbut1(self):               #при нажатии на первую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl4[self.choice_word] == self.pushbuttonword1.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword1.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("4")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut2(self):               #при нажатии на вторую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl4[self.choice_word] == self.pushbuttonword2.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword2.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("4")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut3(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl4[self.choice_word] == self.pushbuttonword3.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword3.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("4")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut4(self):            #при нажатии на четвертую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl4[self.choice_word] == self.pushbuttonword4.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword4.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("4")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut5(self):               #при нажатии на пятую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl4[self.choice_word] == self.pushbuttonword5.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword5.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("4")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut6(self):               #при нажатии на шестую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl4[self.choice_word] == self.pushbuttonword6.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword6.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("4")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def back_to_start(self):               #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class Level5(QWidget):                     #создает пятый уровень
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.wordslvl5 = {'Mine': 'Мой', 'Yours': 'Твой', 'His': 'Его', 'Hers': 'Её', 'Its': 'Его, её', 'Ours': 'Наш'}
        self.wordvalue = [i for i in self.wordslvl5.values()]
        self.wordkey = [i for i in self.wordslvl5.keys()]
        self.pic_hp = ['Pictures/hp0.png', 'Pictures/hp1of6.png', 'Pictures/hp2of6.png', 'Pictures/hp3of6.png',
                       'Pictures/hp4of6.png', 'Pictures/hp5of6.png', 'Pictures/hp100.png']

        self.setGeometry(640, 270, 400, 450)
        self.setWindowTitle('LEVEL 5')

        self.place = QPixmap('Pictures/place.png')
        self.image_place = QLabel(self)
        self.image_place.resize(400, 250)
        self.image_place.setPixmap(self.place)

        self.placedown = QPixmap('Pictures/placedown.png')
        self.image_placedown = QLabel(self)
        self.image_placedown.resize(400, 250)
        self.image_placedown.move(0, 250)
        self.image_placedown.setPixmap(self.placedown)

        self.player = QPixmap('Pictures/player.png')
        self.image_player = QLabel(self)
        self.image_player.resize(400, 250)
        self.image_player.move(55, 61)
        self.image_player.setPixmap(self.player)

        self.boss = QPixmap('Pictures/boss.png')
        self.image_boss = QLabel(self)
        self.image_boss.resize(400, 250)
        self.image_boss.move(280, 66)
        self.image_boss.setPixmap(self.boss)

        self.count = 6
        self.hp = QPixmap(self.pic_hp[self.count])
        self.image_hp = QLabel(self)
        self.image_hp.resize(400, 50)
        self.image_hp.move(277, 15)
        self.image_hp.setPixmap(self.hp)

        self.choice_word = choice(self.wordkey)
        self.label_word = QLabel(self.choice_word, self)
        self.label_word.move(10, 215)
        self.label_word.resize(150, 20)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_word.setFont(font)
        self.label_word.setStyleSheet("color: rgb(128, 166, 255)")

        self.tipword = QLabel("Переведите местоименее выше", self)
        self.tipword.move(10, 250)
        self.tipword.resize(200, 15)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.tipword.setFont(font2)
        self.tipword.setStyleSheet("color: rgb(128, 166, 255)")

        self.count_los = 0
        self.label_los = QLabel(f'Ошибок: {self.count_los}', self)
        self.label_los.move(320, 420)
        self.label_los.resize(100, 15)
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(10)
        self.label_los.setFont(self.font1)
        self.label_los.setStyleSheet("color: rgb(90, 146, 100)")

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)
        self.back.setStyleSheet("color: rgb(255, 255, 255); background: rgb(68, 49, 32);")

        self.pushbuttonword1 = QPushButton(self.wordvalue[0], self)
        self.pushbuttonword1.move(50, 300)
        self.pushbuttonword1.resize(100, 50)
        self.pushbuttonword1.clicked.connect(self.pushbut1)
        self.pushbuttonword1.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword2 = QPushButton(self.wordvalue[1], self)
        self.pushbuttonword2.move(50, 350)
        self.pushbuttonword2.resize(100, 50)
        self.pushbuttonword2.clicked.connect(self.pushbut2)
        self.pushbuttonword2.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword3 = QPushButton(self.wordvalue[2], self)
        self.pushbuttonword3.move(150, 300)
        self.pushbuttonword3.resize(100, 50)
        self.pushbuttonword3.clicked.connect(self.pushbut3)
        self.pushbuttonword3.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword4 = QPushButton(self.wordvalue[3], self)
        self.pushbuttonword4.move(150, 350)
        self.pushbuttonword4.resize(100, 50)
        self.pushbuttonword4.clicked.connect(self.pushbut4)
        self.pushbuttonword4.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword5 = QPushButton(self.wordvalue[4], self)
        self.pushbuttonword5.move(250, 300)
        self.pushbuttonword5.resize(100, 50)
        self.pushbuttonword5.clicked.connect(self.pushbut5)
        self.pushbuttonword5.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword6 = QPushButton(self.wordvalue[5], self)
        self.pushbuttonword6.move(250, 350)
        self.pushbuttonword6.resize(100, 50)
        self.pushbuttonword6.clicked.connect(self.pushbut6)
        self.pushbuttonword6.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

    def pushbut1(self):               #при нажатии на первую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl5[self.choice_word] == self.pushbuttonword1.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword1.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("5")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut2(self):               #при нажатии на вторую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl5[self.choice_word] == self.pushbuttonword2.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword2.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("5")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut3(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl5[self.choice_word] == self.pushbuttonword3.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword3.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("5")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut4(self):            #при нажатии на четвертую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl5[self.choice_word] == self.pushbuttonword4.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword4.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("5")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut5(self):               #при нажатии на пятую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl5[self.choice_word] == self.pushbuttonword5.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword5.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("5")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut6(self):               #при нажатии на шестую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl5[self.choice_word] == self.pushbuttonword6.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword6.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("5")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def back_to_start(self):               #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class Level6(QWidget):                     #создает шестой уровень
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.wordslvl6 = {'Yours': 'Ваш', 'Theirs': 'Их', 'Myself': 'Я сам', 'Yourself': 'Ты сам', 'Himself': 'Он сам',
                     'Itself': 'Это само'}
        self.wordvalue = [i for i in self.wordslvl6.values()]
        self.wordkey = [i for i in self.wordslvl6.keys()]
        self.pic_hp = ['Pictures/hp0.png', 'Pictures/hp1of6.png', 'Pictures/hp2of6.png', 'Pictures/hp3of6.png',
                       'Pictures/hp4of6.png', 'Pictures/hp5of6.png', 'Pictures/hp100.png']

        self.setGeometry(640, 270, 400, 450)
        self.setWindowTitle('LEVEL 6')

        self.place = QPixmap('Pictures/place.png')
        self.image_place = QLabel(self)
        self.image_place.resize(400, 250)
        self.image_place.setPixmap(self.place)

        self.placedown = QPixmap('Pictures/placedown.png')
        self.image_placedown = QLabel(self)
        self.image_placedown.resize(400, 250)
        self.image_placedown.move(0, 250)
        self.image_placedown.setPixmap(self.placedown)

        self.player = QPixmap('Pictures/player.png')
        self.image_player = QLabel(self)
        self.image_player.resize(400, 250)
        self.image_player.move(55, 61)
        self.image_player.setPixmap(self.player)

        self.boss = QPixmap('Pictures/boss.png')
        self.image_boss = QLabel(self)
        self.image_boss.resize(400, 250)
        self.image_boss.move(280, 66)
        self.image_boss.setPixmap(self.boss)

        self.count = 6
        self.hp = QPixmap(self.pic_hp[self.count])
        self.image_hp = QLabel(self)
        self.image_hp.resize(400, 50)
        self.image_hp.move(277, 15)
        self.image_hp.setPixmap(self.hp)

        self.choice_word = choice(self.wordkey)
        self.label_word = QLabel(self.choice_word, self)
        self.label_word.move(10, 215)
        self.label_word.resize(150, 20)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_word.setFont(font)
        self.label_word.setStyleSheet("color: rgb(128, 166, 255)")

        self.tipword = QLabel("Переведите местоименее выше", self)
        self.tipword.move(10, 250)
        self.tipword.resize(200, 15)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.tipword.setFont(font2)
        self.tipword.setStyleSheet("color: rgb(128, 166, 255)")

        self.count_los = 0
        self.label_los = QLabel(f'Ошибок: {self.count_los}', self)
        self.label_los.move(320, 420)
        self.label_los.resize(100, 15)
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(10)
        self.label_los.setFont(self.font1)
        self.label_los.setStyleSheet("color: rgb(90, 146, 100)")

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)
        self.back.setStyleSheet("color: rgb(255, 255, 255); background: rgb(68, 49, 32);")

        self.pushbuttonword1 = QPushButton(self.wordvalue[0], self)
        self.pushbuttonword1.move(50, 300)
        self.pushbuttonword1.resize(100, 50)
        self.pushbuttonword1.clicked.connect(self.pushbut1)
        self.pushbuttonword1.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword2 = QPushButton(self.wordvalue[1], self)
        self.pushbuttonword2.move(50, 350)
        self.pushbuttonword2.resize(100, 50)
        self.pushbuttonword2.clicked.connect(self.pushbut2)
        self.pushbuttonword2.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword3 = QPushButton(self.wordvalue[2], self)
        self.pushbuttonword3.move(150, 300)
        self.pushbuttonword3.resize(100, 50)
        self.pushbuttonword3.clicked.connect(self.pushbut3)
        self.pushbuttonword3.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword4 = QPushButton(self.wordvalue[3], self)
        self.pushbuttonword4.move(150, 350)
        self.pushbuttonword4.resize(100, 50)
        self.pushbuttonword4.clicked.connect(self.pushbut4)
        self.pushbuttonword4.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword5 = QPushButton(self.wordvalue[4], self)
        self.pushbuttonword5.move(250, 300)
        self.pushbuttonword5.resize(100, 50)
        self.pushbuttonword5.clicked.connect(self.pushbut5)
        self.pushbuttonword5.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

        self.pushbuttonword6 = QPushButton(self.wordvalue[5], self)
        self.pushbuttonword6.move(250, 350)
        self.pushbuttonword6.resize(100, 50)
        self.pushbuttonword6.clicked.connect(self.pushbut6)
        self.pushbuttonword6.setStyleSheet("background: rgb(107, 107, 107); color: rgb(255, 255, 255);")

    def pushbut1(self):               #при нажатии на первую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl6[self.choice_word] == self.pushbuttonword1.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword1.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("6")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut2(self):               #при нажатии на вторую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl6[self.choice_word] == self.pushbuttonword2.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword2.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("6")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut3(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl6[self.choice_word] == self.pushbuttonword3.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword3.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("6")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut4(self):            #при нажатии на четвертую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl6[self.choice_word] == self.pushbuttonword4.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword4.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("6")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut5(self):               #при нажатии на пятую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl6[self.choice_word] == self.pushbuttonword5.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword5.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("6")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut6(self):               #при нажатии на шестую кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl6[self.choice_word] == self.pushbuttonword6.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword6.hide()
                self.hp = QPixmap(self.pic_hp[self.count])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("6")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def back_to_start(self):               #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class Level7(QWidget):                     #создает седьмой уровень
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.wordslvl7 = {'Ourselves': 'Мы сами', 'Yourselves': 'Вы сами', 'Themselves': 'Они сами'}
        self.wordvalue = [i for i in self.wordslvl7.values()]
        self.wordkey = [i for i in self.wordslvl7.keys()]
        self.pic_hp = ['Pictures/hp2of6.png', 'Pictures/hp4of6.png', 'Pictures/hp100.png']

        self.setGeometry(640, 270, 400, 450)
        self.setWindowTitle('LEVEL 7')

        self.setGeometry(640, 220, 400, 450)
        self.setWindowTitle('LEVEL 7')

        self.place = QPixmap('Pictures/place.png')
        self.image_place = QLabel(self)
        self.image_place.resize(400, 250)
        self.image_place.setPixmap(self.place)

        self.placedown = QPixmap('Pictures/placedown.png')
        self.image_placedown = QLabel(self)
        self.image_placedown.resize(400, 250)
        self.image_placedown.move(0, 250)
        self.image_placedown.setPixmap(self.placedown)

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)

        self.player = QPixmap('Pictures/player.png')
        self.image_player = QLabel(self)
        self.image_player.resize(400, 250)
        self.image_player.move(55, 61)
        self.image_player.setPixmap(self.player)

        self.boss = QPixmap('Pictures/boss.png')
        self.image_boss = QLabel(self)
        self.image_boss.resize(400, 250)
        self.image_boss.move(280, 66)
        self.image_boss.setPixmap(self.boss)

        self.tipword = QLabel("Переведите местоименее выше", self)
        self.tipword.move(10, 250)
        self.tipword.resize(200, 15)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.tipword.setFont(font2)
        self.tipword.setStyleSheet("color: rgb(128, 166, 255)")

        self.choice_word = choice(self.wordkey)

        self.label_word = QLabel(self.choice_word, self)
        self.label_word.move(10, 215)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_word.setFont(font)
        self.label_word.setStyleSheet("color: rgb(128, 166, 255)")

        self.count_los = 0
        self.label_los = QLabel(f'Ошибок: {self.count_los}', self)
        self.label_los.move(320, 420)
        self.label_los.resize(100, 15)
        self.font1 = QtGui.QFont()
        self.font1.setPointSize(10)
        self.label_los.setFont(self.font1)
        self.label_los.setStyleSheet("color: rgb(90, 146, 100)")

        self.count = 3
        self.hp = QPixmap(self.pic_hp[self.count - 1])
        self.image_hp = QLabel(self)
        self.image_hp.resize(400, 50)
        self.image_hp.move(277, 15)
        self.image_hp.setPixmap(self.hp)

        self.pushbuttonword1 = QPushButton(self.wordvalue[0], self)
        self.pushbuttonword1.move(50, 300)
        self.pushbuttonword1.resize(100, 50)
        self.pushbuttonword1.clicked.connect(self.pushbut1)

        self.pushbuttonword2 = QPushButton(self.wordvalue[1], self)
        self.pushbuttonword2.move(250, 300)
        self.pushbuttonword2.resize(100, 50)
        self.pushbuttonword2.clicked.connect(self.pushbut2)

        self.pushbuttonword3 = QPushButton(self.wordvalue[2], self)
        self.pushbuttonword3.move(150, 300)
        self.pushbuttonword3.resize(100, 50)
        self.pushbuttonword3.clicked.connect(self.pushbut3)

    def pushbut1(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl7[self.choice_word] == self.pushbuttonword1.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword1.hide()
                self.hp = QPixmap(self.pic_hp[self.count - 1])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("7")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut2(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl7[self.choice_word] == self.pushbuttonword2.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword2.hide()
                self.hp = QPixmap(self.pic_hp[self.count - 1])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("7")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

    def pushbut3(self):               #при нажатии на третью кнопку, убирает ее с экрана, при совпадении слов в словаре
        if self.wordslvl7[self.choice_word] == self.pushbuttonword3.text():
            self.count -= 1
            if len(self.wordkey) > 1:
                self.wordkey.remove(self.choice_word)
                self.choice_word = choice(self.wordkey)
                self.label_word.setText(self.choice_word)
                self.pushbuttonword3.hide()
                self.hp = QPixmap(self.pic_hp[self.count - 1])
                self.image_hp.setPixmap(self.hp)
            if self.count == 0:
                lstcomlvl.append("7")
                self.hide()
                self.w2 = EzWin()
                self.w2.show()
        else:
            self.count_los += 1
            self.label_los.setText(f'Ошибок: {self.count_los}')

        self.back = QPushButton('Вернуться', self)
        self.back.resize(100, 30)
        self.back.move(0, 420)
        self.back.clicked.connect(self.back_to_start)

    def back_to_start(self):               #возвращает на окно выбора уровня
        self.hide()
        self.w = ChooseED()
        self.w.show()


class EzWin(QWidget):                      #возвращает в главное меню
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        cursor.execute(f'''UPDATE Data SET LevelsComplite = "{''.join(lstcomlvl)}" WHERE Login = "{login}"''')
        connection.commit()

        self.setGeometry(730, 400, 220, 80)
        self.setWindowTitle('NICE!')

        self.labe = QLabel("Вы победили!!!", self)
        self.labe.move(70, 15)

        self.pushwin = QPushButton('К уровням!', self)
        self.pushwin.move(60, 35)
        self.pushwin.resize(100, 30)
        self.pushwin.clicked.connect(self.pushfin)

    def pushfin(self):
        self.hide()
        self.w = ChooseED()
        self.w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegLogED()
    ex.show()
    sys.exit(app.exec())
