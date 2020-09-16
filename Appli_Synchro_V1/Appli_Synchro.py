import tkinter

# Pour ouvrir la boite de dialogue
from tkinter import filedialog

## Pour les fichiers doc et chemin de OS (systeme)
import os.path 

# Pour la copie des fichiers et repertoire
import shutil

## Pour la date des fichiers
import stat
from stat import ST_MTIME

# Pour afficher la date et l'heure en entete du fichier de rapport de synchro
import datetime


class AppliSynchro :
    def __init__(self, MainWindows) :
    #def __init__(self) :
        # Attribu Fenetre principale
        self.MainWindows = MainWindows
        self.MainWindows.title("Application de synchronisation")
        self.MainWindows.config(relief=tkinter.RAISED, bd=3)
        # Celle de gadjets 
        self.makeWidgets()


    def makeWidgets(self) :
        # frame (conteneur Listes) en premier
        frameListes = tkinter.Frame(self.MainWindows)
        frameListes.pack()
        #----------------------------
        # frame (conteneur des Informations) 
        frameInfos = tkinter.Frame(self.MainWindows)
        frameInfos.pack()
        #----------------------------
        # frame (conteneur de la barre de progression) 
        frameProgressBarre = tkinter.Frame(self.MainWindows)
        frameProgressBarre.pack()
        #----------------------------
        # frame (conteneur des Bouttons Radio)
        frameBouttonsR = tkinter.Frame(self.MainWindows)
        frameBouttonsR.pack()
        #----------------------------
        # frame (conteneur des Bouttons Poussoir) 
        frameBouttonsP = tkinter.Frame(self.MainWindows)
        frameBouttonsP.pack()
        #----------------------------
    
        # Liste Box du dossier SOURCE :
        # on crée une étiquette texte dans ce conteneur
        self.Label_Source = tkinter.Label(frameListes, text="Liste repertoires/fichiers de la Source").grid(row=0, column=0, sticky=tkinter.EW)
        # on crée la liste des fichiers
        self.cvar_fichiers_source = tkinter.StringVar() 
        self.liste_fichiers_source = tkinter.Listbox(frameListes, listvariable=self.cvar_fichiers_source)
        self.liste_fichiers_source.grid(row=1, column=0, sticky=tkinter.NS+tkinter.EW)
        # avec sa scrollbar
        self.vbar_fichiers_source = tkinter.Scrollbar(frameListes, orient=tkinter.VERTICAL)
        self.vbar_fichiers_source.grid(row=1, column=1, sticky=tkinter.NS+tkinter.W)
        # on connecte la scrollbar à la liste des fichiers
        self.liste_fichiers_source.configure(yscrollcommand=self.vbar_fichiers_source.set)
        self.vbar_fichiers_source.configure(command=self.liste_fichiers_source.yview)


        # Liste Box du dossier DESTINATION :
        self.Label_Destination = tkinter.Label(frameListes, text="Liste repertoires/fichiers de la Destination").grid(row=0, column=2, sticky=tkinter.EW)
        # on crée la liste des fichiers
        self.cvar_fichiers_destination = tkinter.StringVar()
        self.liste_fichiers_destination = tkinter.Listbox(frameListes, listvariable=self.cvar_fichiers_destination)
        self.liste_fichiers_destination.grid(row=1, column=2, sticky=tkinter.NS+tkinter.EW)
        # avec sa scrollbar
        self.vbar_fichiers_destination = tkinter.Scrollbar(frameListes, orient=tkinter.VERTICAL)
        self.vbar_fichiers_destination.grid(row=1, column=3, sticky=tkinter.NS+tkinter.W)
        # on connecte la scrollbar à la liste des fichiers
        self.liste_fichiers_destination.configure(yscrollcommand=self.vbar_fichiers_destination.set)
        self.vbar_fichiers_destination.configure(command=self.liste_fichiers_destination.yview)
        #---------------------------------------------------------------------------------------------------------------------
        # La zone d'affichage des textes :
        self.Infos = tkinter.Label(frameInfos, text = " Reglage par défaut : Simulation de synchronisation")
        self.Infos.grid(row=1, column=1, sticky=tkinter.NS+tkinter.EW)
        self.Infos.config(bg='gray', fg='yellow')
        self.Infos.config(height=4, width=65)
        self.Infos.pack(expand=tkinter.YES, fill=tkinter.BOTH)

        #----------------------------------------------------------------------------------------------------------------------------------------
        # Widgets uniquement pour la barre de progression #######################################################################################
        self.f1=tkinter.Frame(frameProgressBarre, height=32, width=420, highlightbackground="#e5c95b", bg="#4c4c4c",bd=2, relief=tkinter.GROOVE)
        #self.f1.place(x=2, y=6) 
        self.f1.grid(row=1, column=1, sticky=tkinter.NS+tkinter.EW)
        #global c
        self.c=tkinter.Canvas(self.f1, height=20, width=410, bg="#e5c95b")
        self.c.place(x=1, y=1)
        #global f2
        self.f2=tkinter.Frame(frameProgressBarre, height=20, width=40, highlightbackground="#e5c95b", bg="#4c4c4c", relief=tkinter.GROOVE)
        self.f2.grid(row=1, column=2, sticky=tkinter.NS+tkinter.EW)
        #global lab1
        self.lab1=tkinter.Label(self.f2, bg="#4c4c4c", fg="#e5c95b") 
        self.lab1.place(x=0, y=4)
        # ######################################################################################################################################
        #---------------------------------------------------------------------------------------------------------------------------------------
        # Les boutons radios pour le choix de synchro
        self.varRadio = tkinter.IntVar()
        self.RB1 = tkinter.Radiobutton(frameBouttonsR, text="Simulation de la synchronisation (affichage simple)",
            variable=self.varRadio, value=0, command=self.commande_bRadio)
        self.RB1.pack(anchor=tkinter.W)

        self.RB2 = tkinter.Radiobutton(frameBouttonsR, text="Execution de la synchronisation (vrai synchro)", 
            variable=self.varRadio, value=1, command=self.commande_bRadio)
        self.RB2.pack(anchor=tkinter.W)
        #---------------------------------------------------------------------------------------------------------------------
        # Les Boutton Source, Destination, Synchro, Exit :
        bSource = tkinter.Button(frameBouttonsP, text="Choisir dossier source", command=self.commande_bSource)
        bDestination = tkinter.Button(frameBouttonsP, text="Choisir dossier destination", command=self.commande_bDestination)
        bSynchro = tkinter.Button(frameBouttonsP, text="Lancer la synchronisation", command=self.commande_bSynchro)
        bExit = tkinter.Button(frameBouttonsP, text="Quitter", command=self.MainWindows.destroy)
        bSource.pack(side=tkinter.LEFT, pady=2)
        bDestination.pack(side=tkinter.LEFT, pady=2)
        bSynchro.pack(side=tkinter.LEFT, pady=2)
        bExit.pack(side=tkinter.LEFT, pady=2)
        #-----------------------------------------------------------------------------------------------------------------------
    

    def commande_bSource(self) :
        # Choix du dossier source :

        "ouvre un dialogue de sélection de répertoire"
        # voir http://tkinter.unpythonic.net/wiki/tkFileDialog
        self.dossier_S = tkinter.filedialog.askdirectory(title="Sélectionnez le dossier source", mustexist=True, parent=self.MainWindows)
        # un dossier a vraiment été sélectionné ?
        if self.dossier_S :
            # on remplit la liste de fichiers
            liste_fichiers_S = os.listdir(self.dossier_S)
            #print(liste_fichiers_S)
            for i in liste_fichiers_S: self.liste_fichiers_source.insert(tkinter.END,i)
            #self.cvar_fichiers_source.set(" ".join(map(os.path.basename, liste_fichiers_S)))
 
    def commande_bDestination(self) :
        # Choix du dossier destination :

        "ouvre un dialogue de sélection de répertoire"
        # voir http://tkinter.unpythonic.net/wiki/tkFileDialog
        self.dossier_D = tkinter.filedialog.askdirectory(title="Sélectionnez le dossier destination", mustexist=True, parent=self.MainWindows)
        # un dossier a vraiment été sélectionné ?
        if self.dossier_D :
            # on remplit la liste de fichiers
            liste_fichiers_D = os.listdir(self.dossier_D)
            #print(liste_fichiers_D)
            for i in liste_fichiers_D: self.liste_fichiers_destination.insert(tkinter.END,i)
            #self.cvar_fichiers_destination.set(" ".join(map(os.path.basename, liste_fichiers_D)))


    def commande_bRadio(self) :
        # Choix de l'option : Simulation de Synchro ou vrai Synchro
        #print(str(self.varRadio.get()))
        if self.varRadio.get() == 1:
            self.Infos.configure(text = " Attention !!! Vous venez d'activer la vrai synchronisation ")
        else :
            self.Infos.configure(text = " Reglage par défaut : Simulation de synchronisation")


    def commande_bSynchro(self) :
        try:
            if self.varRadio.get() == 0:
                self.Infos.configure(text = "Simulation de synchronisation en cours")
                self.synchro(self.dossier_S, self.dossier_D)
                # Appelle de la barre de progression
                self.calculerBARRE()
            else :
                self.Infos.configure(text = "Synchronisation en cours")
                # Execution de la vrai synchronisation
                self.Vrai_synchro(self.dossier_S, self.dossier_D)
                # Appelle de la barre de progression
                self.calculerBARRE()
        # Au cas où self.dossier_S ou self.dossier_D n'existent pas ie (dossier source/destination non choisit)
        except AttributeError :
            self.Infos.configure(text = "VEUILLEZ CHOISIR D'ABORD LES DOSSIERS SOURCE ET DESTINATION") 


    # def commande_bExit(self) :
    #     # on quitte l'application
    #     self.lab.grid_forget()


    def calculerBARRE(self) :
      
      #listeESSAI=[0]*223719
      listeESSAI = self.listeSRC
      
      # Compteur pour la barre de progression . 
      cptBARRE=0 

      for itter in range(len(listeESSAI)) :
        
        # Calcul du pourcentage
        calcPourcentage=((itter+1)*100)/len(listeESSAI)
        # Mise a jour de la barre de progression 
        # (par le Canvas c).
        self.c.update()

        # Creation des rectangles pour la barre de progression .
        while cptBARRE<=calcPourcentage*4 :

          self.c.create_rectangle((cptBARRE, 1, 4+cptBARRE, 21), outline="#e5c95b", fill="red", width=0)
          cptBARRE=cptBARRE+4
          
          # Pourcentage pour affichage a cote de la barre .
          pourcChiffre=" %d %s" % ((cptBARRE/4)-1, "%") 
          # Affichage du pourcentage en calcul dans le 
          # Label (se trouvant dans la Frame f2) .
          self.f2.update()
          self.lab1.config(text=pourcChiffre)
          
        # Des que la barre de progression arrive a 100 %, la barre de
        # progression disparait pour laisser la place au Canvas jaune . 
        if cptBARRE>100*4 :
          self.c.create_rectangle((0, 1, 403, 21), outline="#e5c95b", fill="#e5c95b", width=1) 
        
        #Affichage de l'action réalisée dans le boite d'information
        if self.varRadio.get() == 0:
            self.Infos.configure(text = "Simulation de synchronisation terminer") 
        else :  
            self.Infos.configure(text = "Synchronisation terminer") 
      


    # Les fonction de SYNCHRO ET VRAI SYNCHRO --------------------------------------------------------------------------------------
    ####def synchro(src, dest) :
    def synchro(self, SOURCE, DESTINATION) :
        """ Cette fonction permet de faire la simulation de la synchronisation (src vers dest) en effectuant des affichages """

        # Ouverture/Création du fichier de rapport de synchonisation
        Fichier_Rapport = open("Rapport_Simu_Synchro.txt", "a") # "w" pour tout écrasé !
        date = datetime.datetime.now()
        print("")
        print("=================================== Rapport de la simulation de synchronisation du " + str(date) + " ===================================" + "\n")
        Fichier_Rapport.write("=================================== Rapport de la simulation de synchronisation du " + str(date) + " ===================================" + "\n")
        Fichier_Rapport.write("Copie simulée de : \n")
        ###listeSRC = os.listdir(src)
        ###listeDEST = os.listdir(dest)
        self.listeSRC = os.listdir(SOURCE)
        self.listeDEST = os.listdir(DESTINATION)

        print("Les Fichiers et repertoires de la Source sont :")
        print(self.listeSRC)
        print("")
        print("Les Fichiers et repertoires de la Destination sont :")
        print(self.listeDEST)
        print("")
        print("Copie simulée de : ")
  
        # Pour tout [fichierS] dans source
        for fichierS in self.listeSRC :

                # Pour tout [fichierD] dans destination
                #for fichierD in listeDEST :
                 
                #CheminS='src/'+fichierS
                #CheminCOPIE_S='dest/'+fichierS
                CheminS=os.path.join(SOURCE, fichierS)
                CheminCOPIE_S=os.path.join(DESTINATION, fichierS)
                ####self.listeDEST = os.listdir(DESTINATION)
                
                if ( os.path.isfile(CheminS) ) and ( not (fichierS in self.listeDEST) ) :
                     # Copie du fichierS de source dans dest
                     #shutil.copy( os.path.join(src, fichierS), os.path.join(dest,fichierS) )
                     #shutil.copy(CheminS, CheminCOPIE_S)
                     print(CheminS, "=========>", CheminCOPIE_S) 
                     Fichier_Rapport.write(CheminS + " =========> " + CheminCOPIE_S + "\n")
                
                elif ( os.path.isdir(CheminS) ) and ( not (fichierS in self.listeDEST) ) and (not os.path.exists(CheminCOPIE_S)) :
                     # Copie du fichierS de source dans dest
                     #shutil.copytree(CheminS, CheminCOPIE_S) 
                     print(CheminS, "=========>", CheminCOPIE_S) 
                     Fichier_Rapport.write(CheminS + " =========> " + CheminCOPIE_S + "\n") 
                    
                elif ( os.path.isfile(CheminS) ) and ( fichierS in self.listeDEST ):
                     #Comparaison des dates
                     #pathSRC =  'src/'+fichierS
                     #pathDES =  'dest/'+fichierS
                    
                     pathSRC = os.path.join(SOURCE, fichierS)
                     pathDES = os.path.join(DESTINATION, fichierS)
                    
                     DT1 = os.stat( pathSRC )[ST_MTIME]
                     DT2 = os.stat( pathDES )[ST_MTIME]
                     #if (DT1 >= DT2) :
                     if (DT1 > DT2) :
                         #shutil.copy(CheminS, CheminCOPIE_S)
                         print(CheminS, "=========>", CheminCOPIE_S) 
                         Fichier_Rapport.write(CheminS + " =========> " + CheminCOPIE_S + "\n") 
                                    
                # Si fichierS est un repertoire donc
                elif ( os.path.isdir(CheminS) ) and  (fichierS in self.listeDEST)  :
                     CheminS = fichierS
                     NV_pathSRC = os.path.join(SOURCE, fichierS)
                     NV_pathDES = os.path.join(DESTINATION, fichierS)
                     self.synchro(NV_pathSRC, NV_pathDES)
                    
        print("")
        print("")
        Fichier_Rapport.write("\n")
        Fichier_Rapport.write("\n")
        Fichier_Rapport.close()
                
    

    def Vrai_synchro(self, SOURCE, DESTINATION) :
        """ Cette fonction permet de faire la vrai synchronisation en effectuant des vrai copies """ 

        # Ouverture/Création du fichier de rapport de synchonisation
        Fichier_Rapport = open("Rapport_Synchro.txt", "a")  #"w" pour tout écrasé !
        date = datetime.datetime.now()
        print("")
        print("=================================== Rapport de la simulation de synchronisation du " + str(date) + " ===================================" + "\n")
        Fichier_Rapport.write("=================================== Rapport de la synchronisation du " + str(date) + " ===================================" + "\n")
        Fichier_Rapport.write("Copie de : \n")

        self.listeSRC = os.listdir(SOURCE)
        self.listeDEST = os.listdir(DESTINATION)

        print("Les Fichiers et repertoires de la Source sont :")
        print(self.listeSRC)
        print("")
        print("Les Fichiers et repertoires de la Destination sont :")
        print(self.listeDEST)
        print("")
        print("Copie de : ")

        # Pour tout [fichierS] dans source
        for fichierS in self.listeSRC :
                CheminS=os.path.join(SOURCE, fichierS)
                CheminCOPIE_S=os.path.join(DESTINATION, fichierS)
                
                if ( os.path.isfile(CheminS) ) and ( not (fichierS in self.listeDEST) ) :
                    #Copie du fichierS de source dans dest
                    print(CheminS, "=========>", CheminCOPIE_S) 
                    
                    shutil.copy(CheminS, CheminCOPIE_S)
                    Fichier_Rapport.write(CheminS + " =========> " + CheminCOPIE_S + "\n")
                
                elif ( os.path.isdir(CheminS) ) and ( not (fichierS in self.listeDEST) ) and (not os.path.exists(CheminCOPIE_S)) :
                    #Copie du fichierS de source dans dest
                    print(CheminS, "=========>", CheminCOPIE_S)
                     
                    shutil.copytree(CheminS, CheminCOPIE_S) 
                    Fichier_Rapport.write(CheminS + " =========> " + CheminCOPIE_S + "\n")                  
                    
                elif ( os.path.isfile(CheminS) ) and ( fichierS in self.listeDEST ):
                    #Comparaison des dates
                    
                    pathSRC = os.path.join(SOURCE, fichierS)
                    pathDES = os.path.join(DESTINATION, fichierS)
                    
                    
                    DT1 = os.stat( pathSRC )[ST_MTIME]
                    DT2 = os.stat( pathDES )[ST_MTIME]
                    #if (DT1 >= DT2) :
                    if (DT1 > DT2) :
                        print(CheminS, "=========>", CheminCOPIE_S) 
                        #print(DT1)
                        #print(DT2)
                        shutil.copy(CheminS, CheminCOPIE_S)
                        Fichier_Rapport.write(CheminS + " =========> " + CheminCOPIE_S + "\n")                                         
                                    
                # Si fichierS est un repertoire donc
                elif ( os.path.isdir(CheminS) ) and  (fichierS in self.listeDEST)  :
                    CheminS = fichierS
                    NV_pathSRC = os.path.join(SOURCE, fichierS)
                    NV_pathDES = os.path.join(DESTINATION, fichierS)
                    #print("")
                    #print("Synchro de Source vers Destination par la recursivite")
                    self.Vrai_synchro(NV_pathSRC, NV_pathDES)
        
        print("")
        print("")
        Fichier_Rapport.write("\n")
        Fichier_Rapport.write("\n")
        Fichier_Rapport.close()
    # FIN Fonctions SYNCHRO ET VRAI SYNCHRO ----------------------------------------------------


if __name__ == "__main__" :
    root = tkinter.Tk()
    app = AppliSynchro(root)
    # Taille de la fenetre principale
    ###root.geometry("500x370+10+10")
    # Empecher le fenetre principale de se mettre en full screen
    root.resizable(width=False, height=False)
    root.mainloop()