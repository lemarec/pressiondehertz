# PressionDeHertz

Permet de calculer la pression dans des contacts linéiques ou ponctuels.

Ce programme est réalisé en Python et utilise une interface graphique construite avec Glade.

## Modules python nécessaires

PyGObject (binding for GObject)

## Installation de PyGObject sur windows

La méthode conseillés officiellement et qui permet une installation rapide et fiable passe par l'installation de **Msys2** [https://www.msys2.org](https://www.msys2.org "Site internet de MSYS2")

### Installation et mise à jour de MSYS2

	1. – Installer MSYS2
	2. – Lancer Msys2 par le menu démarrer (MSYS2 MinGW 64 bits (x86_64 et pas i686))
	3. – Mis a jour des packages : `pacman -Syu` (il est possible d'utiliser une proxy)
	4. – Fermer le shell AVEC LA CROIX EN HAUT A DROITE DU SHELL.
	5. – Relancer et finir les mises à jour : relancer par le menu démarrer puis `pacman -Su` (2 fois)
	6. – Doc complète ici : https://github.com/msys2/msys2/wiki/MSYS2-installation

### Installer Python et PyGobject

	1. – Lancer MYS2 puis `pacman -Suy` (Commande à faire de temps en temps)
	2. – `pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject` 
	3. – `Pacman -S mingw-w64-x86_64-gcc make` (le compilateur GCC au cas ou, n'est pas installé de base!)
	4. – Dupliquer puis renommer mingw32-make en make par copier/coller  !!!!!! (dans le rep. mingw64/bin)
	5. – Dans le répertoire de Msys2/home/'Votre Login', éditer le fichier .bashrc et en fin de fichier ajouter la ligne : 	export PATH=$PATH :.:/c/msys64/mingw64/bin ( à modifier en fonction de votre chemin d'installation)
	6. – Vérification : lancer gtk3-demo
	7. – Lancer hello.py par python3 hello.py

Scrypt de hello.py :
```python
    import gi  
    gi.require_version("Gtk", "3.0")  
    from gi.repository import Gtk  

    window = Gtk.Window(title="Hello World")  
    window.show()  
    window.connect("destroy", Gtk.main_quit)  
    Gtk.main()
```

### Glade

Vous pouvez téléchager Glade [ici](https://glade.gnome.org "Site Internet de Glade") <br>
(seulement pour réaliser des modifications sur l'interface)


