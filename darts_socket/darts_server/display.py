# -*- coding: utf-8 -*-
import tkinter as tk
import sound
import socket
import threading

class ConnClient():
    '''
    ソケット通信によりラズベリーパイから画像情報を受け取る。
    '''

    def __init__(self,conn, addr):
        self.conn_socket = conn
        self.addr = addr
        self.recvdata = 0
        self.recvdata1 = 0
        self.recvdata2 = 0
        self.data_list=0

    def run(self):
        try:
            self.recvdata = self.conn_socket.recv(2359296)
            self.recvdata1 = self.recvdata.decode('utf-8')
            self.recvdata2 = self.recvdata1.split(",")
            self.data_list = [int(s) for s in self.recvdata2]
        except socket.error:
            print("connect error")

    def stop(self):
        self.conn_socket.close()


def main():
    global recvlist
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((HOSTNAME, PORT))
    s_socket.listen(CLIENTNUM)

    while (1):
        conn, addr = s_socket.accept()
        print("Conneted by" + str(addr))
        connClientThread = ConnClient(conn, addr)
        connClientThread.run()

        recvlist = connClientThread.data_list
        print(recvlist)

        bullsystem(recvlist[0])

def bullsystem(flag):
    global throw_number, score, round_total,recvlist
    photoorder = recvlist[1]
    throw_number += 1

    round_total = recvlist[2]
    first_throw = recvlist[3]
    second_throw = recvlist[4]
    third_throw = recvlist[5]


    canvas.itemconfig(on_canvas_text1, text=str(first_throw))
    canvas.itemconfig(on_canvas_text2, text=str(second_throw))
    canvas.itemconfig(on_canvas_text3, text=str(third_throw))


    if flag == 1:
        play_sounds.sound1()
        score += 50
        lb.insert(tk.END, str(throw_number)+ "BULL      " + str(score))
        canvas.itemconfig(
            on_canvas_text,
            text=str(score)
            )
    else:
        lb.insert(tk.END, str(throw_number)+"NO BULL"+ str(score))


    if photoorder == 3 and round_total > 0:
        changeimg()

def memo():
    value = entry.get()
    if not value:
        lb.insert(tk.END, "入力してね")

    else:
        lb.insert(tk.END, value)
        entry.delete(0, tk.END)


def changeimg():
    global canvas, on_canvas, score, round_total
    canvas.move(
        on_canvas_text,
        1000,
        1000
    )
    canvas.move(
        on_canvas_text1,
        1000,
        1000
    )
    canvas.move(
        on_canvas_text2,
        1000,
        1000
    )
    canvas.move(
        on_canvas_text3,
        1000,
        1000
    )



    if round_total == 50:
        canvas.itemconfig(
            on_canvas,
            image=images[1]
        )
    elif round_total == 100:
        canvas.itemconfig(
            on_canvas,
            image=images[2]
        )

    elif round_total == 150:
        canvas.itemconfig(
            on_canvas,
            image=images[3]

        )



    root.after(3900, play_sounds.sound2)
    root.after(7000, rechangeimg)

def rechangeimg():
    global root, canvas
    canvas.itemconfig(
        on_canvas,
        image=images[0]
    )
    canvas.move(
        on_canvas_text,
        -1000,
        -1000
    )
    canvas.move(
        on_canvas_text1,
        -1000,
        -1000
    )
    canvas.move(
        on_canvas_text2,
        -1000,
        -1000
    )
    canvas.move(
        on_canvas_text3,
        -1000,
        -1000
    )


def buffer():
    #ソケット通信を並列処理
    th_body = threading.Thread(target=main, name='main')
    th_body.setDaemon(True)
    th_body.start()

def rungui():
    global root, canvas, on_canvas, images, lb, entry, on_canvas_text, score
    global on_canvas_text1, on_canvas_text2, on_canvas_text3

    #メインウィンドウ
    root = tk.Tk()
    root.geometry("1140x675")
    root.title("DARTS BULL GAME")
    font = ("Helevetica", 14)
    font_log = ("Helevetica", 11)

    # menubar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # startmenu
    startmenu = tk.Menu(menubar)
    menubar.add_cascade(label="BULL GAME", menu=startmenu)
    startmenu.add_command(label="開始する", command=lambda: buffer())

    # canvas make
    canvas = tk.Canvas(
        root,
        width=960,
        height=600,
        relief=tk.RIDGE,
        bd=2
    )
    canvas.place(x=175, y=0)


    # image
    images.append(tk.PhotoImage(file="501.png"))
    images.append(tk.PhotoImage(file="onebull.png"))
    images.append(tk.PhotoImage(file="lowton.png"))
    images.append(tk.PhotoImage(file="hattrick.png"))


    on_canvas = canvas.create_image(
        0,
        0,
        image=images[0],
        anchor=tk.NW
    )
    on_canvas_text = canvas.create_text(
        480, 300, text=str(score), font=("Helvetica", 250, "bold")

    )
    on_canvas_text1 = canvas.create_text(
        850, 145, text=0, font=("Helvetica", 40, "bold"), fill='white')
    on_canvas_text2 = canvas.create_text(
        850, 195, text=0, font=("Helvetica", 40, "bold"), fill='white')
    on_canvas_text3 = canvas.create_text(
        850, 245, text=0, font=("Helvetica", 40, "bold"), fill='white')

     # response_area
    response_area = tk.Label(
        root,
        width=106,
        height=4,
        bg="gray",
        font=font,
        relief=tk.RIDGE,
        bd=2
    )
    response_area.place(x=176, y=600)


    # entrybox
    entry = tk.Entry(
        root,
        width=75,
        font=font
    )
    entry.place(x=230, y=630)
    entry.focus_set()

    # listbox
    lb = tk.Listbox(
        root,
        width=20,
        height=43,
        font=font_log
    )


    # scroolbar1
    sb1 = tk.Scrollbar(
        root,
        orient=tk.VERTICAL,
        command=lb.yview
    )

    # スクロールバーと連動
    lb.configure(yscrollcommand=sb1.set)
    lb.grid(row=0, column=0)
    sb1.grid(row=0, column=1, sticky=tk.NS)
    # button
    button = tk.Button(
        root,
        bg='black',
        command=lambda: buffer(),
        text="START",
        width=19,
    )
    button.place(x=0, y=655)
    # button2
    button2 = tk.Button(
        root,
        width=15,
        text="MEMO",
        command=lambda: memo())
    button2.place(x=950, y=630)
    # mainloop
    root.mainloop()


if __name__ == "__main__":
    lb = None
    on_canvas = None
    on_canvas_text = None
    on_canvas_text1 = None
    on_canvas_text2 = None
    on_canvas_text3 = None
    images = []
    entry = None
    response_area = None
    score = 0
    throw_number = 0

    play_sounds = sound.Sounds()

    HOSTNAME = "192.168.0.3"
    PORT = 12345
    CLIENTNUM = 1

    rungui()
