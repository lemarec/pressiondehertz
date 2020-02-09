import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import re


def is_numeric(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False

def MessageErreurEtatCheckbutton():
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Etat des check button")
    dialog.format_secondary_text("Ce sont des contacts ponctuels ou linéiques !")
    dialog.run()
    print("INFO dialog closed")
    dialog.destroy()

def MessageErreur():
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Entrer un nombre réél")
    dialog.format_secondary_text("Impossible de faire des calculs sur des valeurs non numériques.")
    dialog.run()
    print("INFO dialog closed")
    dialog.destroy()


def MessageErreurZero():
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Entrer un nombre non nul")
    dialog.format_secondary_text("Impossible de faire des divisions avec des valeurs nulles.")
    dialog.run()
    print("INFO dialog closed")
    dialog.destroy()

def MessageErreurEgaux():
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Entrer deux diamètres différents")
    dialog.format_secondary_text("Impossible de faire des divisions avec des valeurs nulles.")
    dialog.run()
    print("INFO dialog closed")
    dialog.destroy()