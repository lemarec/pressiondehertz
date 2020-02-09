import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
import os, sys
import re
import Errors
pression=0
# type de contact
ctype=0
# état des check-button
r1state = False
r2state = False
# Etat de combobox pour définir la pression
ecb0,ecb1,ecb2 = 0,0,0
# Données pour le combobox à redéfinir
combotype = ['Sur acier ou fonte sans matage', 'Sur acier ou fonte avec léger matage (ou sur béton)', 'Contact entre filets (ex: vis assemblage)']
# Valeur des pression pour les différents cas (3 premiers pour fixe, 3 autres pour mobile), et pour mini, maxi, moyen
pressm=[[80,200,15],[90,225,22.5], [100,250,30],[2,0.5,1,1,1.5,2.5,2,4],[4,4.25,13,1.25,2,3.25,2.5,6],[6,8,25,1.5,2.5,4,3,8]]

def test(valeur):
    err = False
    if not Errors.is_numeric(valeur):
        Errors.MessageErreur();
        err = True
    elif float(valeur) == 0:
        Errors.MessageErreurZero();
        err = True
    return err

# Calcul de la pression maxi en fonction de l'état des 3 combobox
def calcpression(ecb0,ecb1,ecb2):
    # ecb1 = 0 => cas 0,1,2 en fonction du combo 0 / ecb1 = 1 => cas 3,4,5 en fonction du combo 0
    cas=ecb1*3+ecb0
    # print("Etat des combos : ecb0:{0}-ecb1: {1}-ecb2: {2} (cas N°{3})".format(ecb0, ecb1, ecb2,cas))
    return pressm[cas][ecb2]

class PressionHertz:
    __gtype_name__ = "Pressions de Hertz"
    def __init__(self):
        # en cas d'usage de PyInstaller pour créer un exe unique, il faut adapter le chemin du fichier glade
        if getattr(sys, 'frozen', False):
           print("bundle")
           wd = sys._MEIPASS
        else:
           print("live")
           wd = os.getcwd()
        file_path = os.path.join(wd,'Interface_PressionDeHertz.glade')
        interface = Gtk.Builder()
        interface.add_from_file(file_path)
        interface.connect_signals(self)
        window = interface.get_object("window")
        # Variables pour label et textEntry 'longueur' / permet aussi de rendre visible/invisible
        self.longueur = interface.get_object("Entry_longueur")
        self.llongueur = interface.get_object("label_longueur")
        # Variable en TextEntry rayon des pièce 1 et 2
        self.lr1 = interface.get_object('label_r1')
        self.lr2 = interface.get_object('label_r2')
        self.er1 = interface.get_object('entry_r1')
        self.er2 = interface.get_object('entry_r2')
        # combo type de contact
        self.combo2=interface.get_object('comboboxtext2')
        self.pressionmax=interface.get_object('labelpressionmax')
        # Construire le combo 2
        for i in (0,1,2):
            self.combo2.append_text(combotype[i])
        self.combo2.set_active(0)
        # autre objets
        self.E1 = interface.get_object('entry_E1')
        self.E2 = interface.get_object('entry_E2')
        self.effort = interface.get_object('entry_effort')
        self.ldim = interface.get_object('label_dim')
        self.lpmax = interface.get_object('label_pmax')
        self.warnings = interface.get_object('label_warnings')

        window.show_all()

    def on_button_calculer_clicked(self,widget):
        # Récupération des données et vérification de la validité des données
        erreur = False
        self.warnings.set_text('')
        # Effort, E1, E2
        effort = self.effort.get_text()
        E1 = self.E1.get_text()
        E2 = self.E2.get_text()
        for i in (E1,E2,effort):
            erreur = test(i)
        # Evaluation de r
        if r1state==True:
            r=self.er2.get_text()
            erreur = test(r)
        elif r2state==True:
            r=self.er1.get_text()
            erreur = test(r)
        else:
            r1 = self.er1.get_text()
            r2 = self.er2.get_text()
            for i in (r1, r2):
               erreur=test(i)
            if not erreur:
                r=1/(1/float(r1)+1/float(r2))
                print("r=",r)
        if ctype==0:
            # liaison cylindre/Cylindre
            longueur=self.longueur.get_text()
            erreur = test(longueur)
            if not erreur:
                print(longueur)
                E = 1 / (1 / float(E1) + 1 / float(E2))
                b=1.52*(float(effort)*abs(float(r))/(float(E)*float(longueur)))**0.5
                pmax=0.418*(float(effort)*float(E)/(abs(float(r))*float(longueur)))**0.5
                print("E={0} - r={1} - b={2} - pmax={3}".format(E,r,b,pmax))
                self.ldim.set_text(str(round(b,4)))
                self.lpmax.set_text(str(round(pmax,1)))

        else:
            # Liaison sphere/Sphere
            print("sph/sph")
            if not erreur:
                E = 1 / (1 / float(E1) + 1 / float(E2))
                b=1.11*(float(effort)*abs(float(r))/float(E))**(1/3)
                pmax=0.388*(float(effort)*(float(E)/abs(float(r)))**2)**(1/3)
                self.ldim.set_text(str(round(b, 4)))
                self.lpmax.set_text(str(round(pmax, 1)))
        print("pression = ",pression)
        if not erreur and pmax > float(pression):
            self.warnings.set_text('ATTENTION PRESSION ADMISSIBLE DEPASSEE')

    # Lien avec glade : windows / signaux / GtkWidget / widget / destroy -> destroy
    def on_destroy(self, widget):
        print("Au Revoir !")
        Gtk.main_quit()

    # togglebutton de la pièce 1 (rayon 1)
    def r1_toggled(self,checked):
        global r1state
        if checked.get_active():
            r1state = True
            self.lr1.set_visible(False)
            self.er1.set_visible(False)
            # on ne peut activer les 2 combos
            if r2state == True:
                Errors.MessageErreurEtatCheckbutton()
                checked.set_active(False)
        else:
            r1state = False
            self.lr1.set_visible(True)
            self.er1.set_visible(True)
        print ("check_button - etat :",r1state)

    # togglebutton de la pièce 2 (rayon 2)
    def r2_toggled(self,checked):
        global r2state
        if checked.get_active():
            r2state = True
            self.lr2.set_visible(False)
            self.er2.set_visible(False)
            if r1state == True:
                Errors.MessageErreurEtatCheckbutton()
                checked.set_active(False)
        else:
            r2state = False
            self.lr2.set_visible(True)
            self.er2.set_visible(True)
        print ("check_button - etat :",r2state)

    def combotype_changed(self,widget,data=None):
        global ctype
        model = widget.get_model()
        active = widget.get_active()
        if active >=0:
            print("code : ", model[active][0], "active=", active)
            if active==1:
                ctype=1
                self.longueur.set_visible(False)
                self.llongueur.set_visible(False)
            else:
                ctype=0
                self.longueur.set_visible(True)
                self.llongueur.set_visible(True)
        else:
            print("erreur combo - active =", active)

    def combo0changed(self,widget,data=None):
        global ecb0
        global pression
        model=widget.get_model()
        active=widget.get_active()
        if active >= 0:
            ecb0=active
            pression = calcpression(ecb0,ecb1,ecb2)
            self.pressionmax.set_text("Pression maximale (MPa) : " + str(pression))
            print("Etat des combos : ecb0: {0} - ecb1: {1} - ecb2: {2} - pression = {3}".format(ecb0, ecb1, ecb2,pression))
        else:
            print("erreur combo min/moy/max")


    def combo1changed(self,widget,data=None):
        global ecb1
        global ecb2
        global pression
        model=widget.get_model()
        active=widget.get_active()
        if active >=0:
            ecb1 = active
            ecb2 = 0
            pression = calcpression(ecb0, ecb1, ecb2)
            self.pressionmax.set_text("Pression maximale (MPa) : " + str(pression))
            print("Etat des combos : ecb0: {0} - ecb1: {1} - ecb2: {2} - pression = {3}".format(ecb0, ecb1, ecb2,pression))
            #print("code : ", model[active][0], "active=", active)
            secu= model[active][0]

            if active==0:
                self.combo2.remove_all()
                for i in (0, 1, 2):
                    self.combo2.append_text(combotype[i])
                self.combo2.set_active(0)
            if active==1:
                self.combo2.remove_all()
                self.combo2.append_text('Contact entre filets (mobile en fonctionnement)')
                self.combo2.append_text('Articulations en porte à faux')
                self.combo2.append_text('Articulations en chape (ou fourchette)')
                self.combo2.append_text('Paliers rigide avec flèxion de l`arbre : acier/fonte')
                self.combo2.append_text('Paliers à rotule, acier sur bronze à graissage intermittent')
                self.combo2.append_text('Paliers acier trempé/bronze. Lubrification sur film d`huile')
                self.combo2.append_text('Galet sur rail Acier/fonte grise')
                self.combo2.append_text('Galet sur rail Acier/Acier')
                self.combo2.set_active(0)
        else:
            print("erreur combo type contact")

    def combo2changed(self,widget,data=None):
        global ecb2
        global pression
        model=widget.get_model()
        active=widget.get_active()
        if active >=0:
            ecb2=active
            pression = calcpression(ecb0, ecb1, ecb2)
            self.pressionmax.set_text("Pression maximale (MPa) : " + str(pression))
            print("Etat des combos : ecb0: {0} - ecb1: {1} - ecb2: {2} - pression = {3}".format(ecb0, ecb1, ecb2,pression))
            #print("code : ", model[active][0], "active=", active)
        else:
            print("erreur combo - préciser contact")

if __name__ == "__main__":
    app = PressionHertz()
    Gtk.main()