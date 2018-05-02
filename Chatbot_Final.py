#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *  # Initialize the tkinter methods
from tkinter import ttk, font

from chatterbot.trainers import ListTrainer  # method to train the chatbot
from chatterbot import ChatBot  # import the chatterbot constructor
import os  # for the reading list

bot = ChatBot('Chatter Tinker',  # Create the chatbot
              logic_adapters=['chatterbot.logic.BestMatch',
                              {
                                  'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                                  'threshold': 0.55,
                                  'default_response': 'Lo siento, no entendi lo que dijiste...'
                              },
                              'chatterbot.logic.MathematicalEvaluation',
                              ],
              filters=["chatterbot.filters.RepetitiveResponseFilter"]
              )

bot.set_trainer(ListTrainer)  # set the trainer

for _file in os.listdir('Contexts'):
    chats = open('Contexts/' + _file, 'r').readlines()  # Funcion para leer los documentos de texto

    # bot.train(chats)  # Funcion que llama a chats y entrena al bot


# Gestor de geometría (grid). Ventana dimensionable
class Aplicacion:
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("Mi chatbot")
        fuente = font.Font(weight='bold')

        self.marco = ttk.Frame(self.raiz, borderwidth=2,
                               padding=(10, 10))
        self.scrollbar = ttk.Scrollbar(self.marco)
        self.msg_list = Listbox(self.marco, height=15)

        self.etiq1 = ttk.Label(self.marco, text="User:",
                               font=fuente, padding=(5, 5))
        self.etiq2 = ttk.Label(self.marco, text="Mensaje:",
                               font=fuente, padding=(5, 5))
        self.etiq3 = ttk.Label(self.marco, text="Bienvenidos a la sala de chat, soy {}".format(bot.name),
                               font=fuente, padding=(5, 5))

        self.usuario = StringVar()
        self.mensaje = StringVar()

        self.ctext1 = ttk.Entry(self.marco, textvariable=self.usuario,
                                width=30)
        self.ctext2 = ttk.Entry(self.marco, textvariable=self.mensaje,
                                width=30)

        self.separ1 = ttk.Separator(self.marco, orient=HORIZONTAL)
        self.boton1 = ttk.Button(self.marco, text="Enviar",
                                 padding=(5, 5), command=self.enviar)
        self.boton2 = ttk.Button(self.marco, text="Salir",
                                 padding=(5, 5), command=quit)
        self.boton3 = ttk.Button(self.marco, text="Ayuda",
                                 padding=(5, 5), command=self.ayuda)
        self.boton4 = ttk.Button(self.marco, text="Limpiar mensajes",
                                 padding=(5, 5), command=self.limpiar)

        # Ahora se colocan las posiciones dentro del marco
        self.marco.grid(column=0, row=0, padx=5, pady=5,
                        sticky=(N, S, E, W))
        self.scrollbar.grid(column=7, row=1,
                            sticky=(N, S, E, W))
        self.msg_list.grid(column=1, row=1, columnspan=6, padx=1,
                           sticky=(N, S, E, W))

        self.etiq1.grid(column=0, row=6,
                        sticky=(N, S, E, W))
        self.ctext1.grid(column=1, row=6, columnspan=2,
                         sticky=(E, W))
        self.etiq2.grid(column=3, row=6,
                        sticky=(N, S, E, W))
        self.ctext2.grid(column=4, row=6, columnspan=2,
                         sticky=(E, W))
        self.separ1.grid(column=0, row=5, columnspan=7, pady=5,
                         sticky=(N, S, E, W))
        self.boton1.grid(column=6, row=6, padx=5,
                         sticky=E)
        self.boton2.grid(column=3, row=7, padx=5,
                         sticky=W)
        self.etiq3.grid(column=1, row=0, columnspan=5,
                        sticky=(N, S, E, W))
        self.boton3.grid(column=6, row=0, padx=5,
                         sticky=W)
        self.boton4.grid(column=1, row=2, padx=5,
                         sticky=W)

        # A continuación, se activa la propiedad de expandirse
        # o contraerse definida antes con la opción
        # 'sticky' del método grid().
        self.raiz.columnconfigure(0, weight=1)
        self.raiz.rowconfigure(0, weight=1)
        self.marco.columnconfigure(0, weight=1)
        self.marco.columnconfigure(1, weight=1)
        self.marco.columnconfigure(2, weight=1)
        self.marco.columnconfigure(3, weight=1)
        self.marco.columnconfigure(4, weight=1)
        self.marco.columnconfigure(5, weight=1)
        self.marco.rowconfigure(0, weight=1)
        self.marco.rowconfigure(1, weight=1)
        self.marco.rowconfigure(2, weight=1)
        self.marco.rowconfigure(3, weight=1)
        self.marco.rowconfigure(4, weight=1)
        self.marco.rowconfigure(5, weight=1)
        self.marco.rowconfigure(6, weight=1)

        # Establece el foco en la caja de mensaje
        self.ctext2.focus_set()
        self.raiz.mainloop()

    # Fin de la clase aplicacion

    # Se define la funcion que va a realizar el boton enviar
    def enviar(self):
        while True:
            request = (self.ctext2.get())
            f_request = self.ctext1.get() + ": " + str(request)
            response = bot.get_response(request)
            f_response = str(bot.name) + ": " + str(response)
            self.msg_list.insert(END, f_request)
            self.msg_list.insert(END, f_response)
            self.mensaje.set("")
            self.ctext2.focus_set()
            break

    def limpiar(self):
        self.msg_list.delete(0, END)
        self.mensaje.set("")
        self.ctext2.focus_set()

    def ayuda(self):
        self.msg_list.insert(END, "Si necesitas ayuda puedes hablarme de los siguientes temas:")
        self.msg_list.insert(END, 'Venezuela, "No se te ha ido la luz?"')
        self.msg_list.insert(END, 'Deportes, "A que equipo le vas?"')
        self.msg_list.insert(END, 'Musica, "Cual es tu musica favorita?"')
        self.msg_list.insert(END, 'Peliculas, "Cual es tu pelicula favorita?"')
        self.msg_list.insert(END, 'Series, "Te gustan las series?"')
        self.msg_list.insert(END, 'Memes, "Tienes memes?"')
    # Fin de la clase Aplicacion


def main():
    Aplicacion()
    return 0


if __name__ == '__main__':
    main()
# Fin del programa
