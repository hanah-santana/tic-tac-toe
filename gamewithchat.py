from tkinter import *
from tkinter import messagebox
import tkinter as tk
from client import Client
from tkinter import scrolledtext, Entry, Button
import threading

def play_tic_tac_toe(master):
    frame = Frame(master)
    frame.pack()

    clicked = True
    count = 0
    winner = False

    buttons = []
    for i in range(9):
        button = Button(frame, text=" ", font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace",
                        command=lambda i=i: button_click(buttons[i]))
        buttons.append(button)
        row = i // 3
        col = i % 3
        button.grid(row=row, column=col)

    def disable_all_buttons():
        for button in buttons:
            button.config(state=DISABLED)

    def check_if_won():
        nonlocal winner
        winner_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]            # Diagonals
        ]

        for combo in winner_combinations:
            if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != " ":
                winner = True
                for index in combo:
                    buttons[index].config(bg="red")
                messagebox.showinfo("Tic Tac Toe", f"CONGRATULATIONS! {buttons[combo[0]]['text']} Wins!!")
                disable_all_buttons()
                return
        #TODO: create an if/else statement that checks winner combinations across the boards.

        if count == 9 and not winner:
            messagebox.showinfo("Tic Tac Toe", "Empate!\nIt's A Tie!\n👔")
            disable_all_buttons()

    def button_click(button):
        nonlocal clicked, count

        if button["text"] == " " and clicked:
            button["text"] = "X"
            clicked = False
            count += 1
            check_if_won()
        elif button["text"] == " " and not clicked:
            button["text"] = "O"
            clicked = True
            count += 1
            check_if_won()
        else:
            messagebox.showerror("Tic Tac Toe", "Hey! That box has already been selected 🖐🏻😌\nPick Another Box...")

    def reset_game():
        nonlocal clicked, count, winner
        for button in buttons:
            button.config(text=" ", bg="SystemButtonFace", state=NORMAL)
        clicked = True
        count = 0
        winner = False

# Create the main window
window = Tk()
window.title("PPD | Tic-Tac-Toe")
window.geometry('1000x800')
reset_functions = []


for _ in range(3):
    play_tic_tac_toe(window)
    Frame(window, height=20).pack()
    reset_functions.append(play_tic_tac_toe)

#Creation of chat

give_up_button = Button(window, text="🏳️ Give Up 🏳️", font=("Helvetica", 15), height=2, width=15, bg="SystemButtonFace",
                      command="").place(x= 700, y=40)

chat_frame = Frame(window)
chat_frame.place(x= 680, y=100)

chat_history = scrolledtext.ScrolledText(chat_frame, wrap=WORD, width=30, height=15)
chat_history.pack()

entry_field = Entry(chat_frame, width=25)
entry_field.pack()

host = '127.0.0.1'
port = 8080
client = Client(host, port)

def receive_messages():
        while True:
            try:
                message = client.client_socket.recv(1024).decode('utf-8')
                chat_history.insert(tk.END, 'Oponente: '+ message + '\n')
            except:
                break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def send_message():
    message = entry_field.get()
    if message:
        chat_history.insert(END, "You: " + message + "\n")
        client.client_socket.send(message.encode('utf-8'))
        entry_field.delete(0, END)

send_button = Button(chat_frame, text="Send", command=send_message)
send_button.pack()

def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_display.insert(tk.END, 'Oponente: '+ message + '\n')
            except:
                break

window.mainloop()