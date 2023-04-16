
from bs4 import BeautifulSoup
import requests


#cette fonction renvoie tout les liens dans le corps d'une page https://iceandfire.fandom.com"
def liste_liens(page):
    print("tentative de connexion à :")
    l=[]
    
    if('gameofthrones.fandom.com'in page):
        print(page)
        print("SIGNAL/")
        url= "https://iceandfire.fandom.com"+page.split("/wiki/")[-1]
        
    else :
        if('.com'in page):
             return  []  
    if('/wiki/' in page):
                url="https://iceandfire.fandom.com"+page
    else:
                 url="https://iceandfire.fandom.com/wiki/"+page
        
    print(url)

    p = requests.get(url)

    soup = BeautifulSoup(p.text, 'html.parser')

    corps =soup.find_all('div',class_="mw-parser-output")

    for corp in corps:
        for link in corp.find_all('a', href=True):
            if '/wiki/' in link['href']:
                page=link['href']
                if('.com' not in page):
                  l.append(page[6:])
                
                
               
    return l 

# test 1
#print (liste_liens("Petyr_Baelish")) 

#['Fingers', 'Harrenhal', 'Lord_Paramount', 'Riverlands', 'Eyrie', 'Vale_of_Arryn', 'Master_of_Coin', 'Robert_I_Baratheon', 'House_Baelish', 'House_Arryn', 'House_Baratheon_of_King%27s_Landing', 'Westeros', 'Andals', 'Essos', 'Braavos',
#  'Janos_Slynt', 'Edmure_Tully', 'Tyrion_Lannister', 'Lysa_Arryn', 'Harrenhal', 'Lord_Paramount', 'Riverlands', 'Eyrie', 'Vale_of_Arryn', 'Hoster_Tully', 'Catelyn_Stark', 'Lysa_Arryn', 'Edmure_Tully', 'Brandon_Stark', 'Master_of_Coin', 'Robert_Baratheon', 
# 'Iron_Throne', 'King%27s_Landing', 'Varys', 'Red_Keep',
#  'Valyrian_steel', 'Tyrion_Lannister', 'Eddard_Stark',
#  'Jon_Arryn', 'Tower_of_the_Hand', 'Hugh_of_the_Vale', 'Sansa_Stark', 'Daenerys_I_Targaryen', 'Barra', 'Jaime_Lannister', 'Joffrey_I_Baratheon', 'Tommen_I_Baratheon', 'Myrcella_Baratheon', 'Stannis_Baratheon']











#cette fonction sert à sauvegarder un dictionnaire dans un fichier txt
def svg_dico(dico, fichier):
    f= open(fichier, 'a')
    if(len(dico)==0):
        return f.close()
    
    titre = next(iter(dico))

    print(titre)

    f.write(titre)
    valeur=str(dico[titre])
    
    f.write(valeur)
    f.write('\n')
    
    f.close() 


#test 2

#mon_dictionnaire = {"titre_lien":["liste","des","liens"]}
#svg_dico(mon_dictionnaire, 'C:/Users/Lenovo/Desktop/test.txt')



##cette question sert à charger un dictionnaire depuis un fichier txt
def chg_dico(fichier):
    f=open(fichier, "r")
    dictionnaire={}
    for line in f:
         line = line.strip().replace("'", "").replace("[", ", ").replace("]", "").replace("%27", "'").replace("\n","")
         liste=line.split(", ")
         dictionnaire[liste[0]]=liste[1:]
        
        
    return dictionnaire     

#test 3
#print( chg_dico('C:/Users/Lenovo/Desktop/test.txt'))




 
    




#cette fonction fait un parcours en largeur du site https://iceandfire.fandom.com" et le sauvegarde dans un fichier txt
def bfs3(start_page):
 
    
    visited=set()
    queue=[start_page]
    while queue:
        dict={}
        page=queue.pop(0)
        liens=liste_liens(page)
        dict[page]=liens
        
        svg_dico(dict, 'C:/Users/Lenovo/Desktop/BFS.txt')

        for lien in liens:
            if lien not in visited:
                visited.add(lien)
                queue.append(lien)
    
    print("fin du bfs")

start_page = 'Petyr_Baelish'

#test 4 en partant de la page Petyr_Baelish
#bfs3(start_page)


#chargement du dictionnaire depuis le fichier txt du bfs ( le bfs peut prendre plusieurs minutes donct c'est preferable de le sauvegarder dans un fichier txt)
dict= chg_dico('C:/Users/Lenovo/Desktop/BFS.txt')




#cette fonction sert à trouver le plus court chemin d'une page A à une page B sur le wiki
def plus_court_chemin(start_page, end_page):
    visited = set()

    queue = [(start_page, [start_page])]

    while queue:
        page, path = queue.pop(0)

        if page == end_page:
            return path
        
        if page not in visited:
            visited.add(page)
            if page in dict:
                for lien in dict[page]:
                    if lien not in visited:
                        queue.append((lien, path + [lien]))
    return "Pas de chemin possible"


#test 5
#print(plus_court_chemin('Rhaego', 'Dorne'))



#on va ensuite essayer de trouver le plus court chemin en poids de caractere avec une voyelle =2 et consonne=1
#calculer nmbr des voyelles
def nombre_voyelle(cible):
     a=0
     for i in range(0,len(cible)):
          if cible[i] in "aeiouyAEIOUY":
               a+=2
     return a


#calculer nmbr des caractères
def nombre_caractères(cible):
     
     return int (len(cible)-( nombre_voyelle(cible)/2))


def nombre (cible):
     return nombre_caractères(cible)+nombre_voyelle(cible)
     

def somme_nombre(liste):
    somme = 0
    
    for element in liste:
            somme += nombre(element)
    return somme

#print(somme_nombre(['Harrenhal',  'Rhaego']))



#cette fonction permet de trouver le plus court chemin en poids de caracteres 
#- le poids d’un chemin étant défini comme la somme des poids des liens qui le composent 
def pcc_voyelles(start_page, end_page):
    visited = set()
    queue = [(start_page, [start_page], 0)]
    # chaque élément de la file d'attente est un triplet : 
    # (page courante, chemin parcouru jusqu'à cette page, poids total du chemin)

    while queue:
        queue.sort(key=lambda x: x[2])  # tri de la file d'attente par poids total croissant
        page, path, weight = queue.pop(0)
        if page == end_page:
            return path
        if page not in visited:
            visited.add(page)
            if page in dict:
                for lien in dict[page]:
                    if lien not in visited:
                        new_weight = weight + nombre(lien)
                        queue.append((lien, path + [lien], new_weight))
    return "Pas de chemin possible"

#test 6
#on a la deux different chemins entre le pcc et le pcc voyelle pour les memes page A et B 
print(plus_court_chemin("Jon_Arryn","Rhaego"))
print (pcc_voyelles('Jon_Arryn', 'Rhaego'))

    

  


    



# cette fonction renvoie tout les personnages de la saga Game of thrones
def Liste_personnages():
    liste=[]
    
    for key in dict:
        url = "https://iceandfire.fandom.com/wiki/"+key
        #print(url)
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        h2_list = soup.find_all('h2')
        for h2 in h2_list:
                if h2.text.lower() == 'family':
                    liste.append(key)
                    print('personnage !')
    return liste   

#test 7
#l=Liste_personnages()  
#print(l)
#print("-----------")
##affichage :<
l=['Petyr_Baelish', 'Robert_I_Baratheon', 'Janos_Slynt', 'Edmure_Tully', 'Tyrion_Lannister', 'Lysa_Arryn', 'Hoster_Tully', 'Catelyn_Stark', 'Brandon_Stark', 'Robert_Baratheon', 'Eddard_Stark', 'Jon_Arryn', 
'Sansa_Stark', 'Daenerys_I_Targaryen', 'Barra', 'Jaime_Lannister', 'Joffrey_I_Baratheon', 'Tommen_I_Baratheon', 'Myrcella_Baratheon', 'Stannis_Baratheon', 'Shella_Whent', 'Harren_Hoare', 'Aegon_the_Conqueror', 'Daemon_Targaryen', 'Aegon_IV', 'Daemon_Blackfyre', 'Maekar_I', 'Minisa_Tully', 'Tywin_Lannister', 'Arya_Stark', 'Gregor_Clegane', 'Cersei_Lannister', 'Aegon_I_Targaryen', 'Orys_Baratheon', 'Argella_Baratheon', 'Mern_IX_Gardener', 'Renly_Baratheon', 'Mace_Tyrell', 'Harwyn_Hoare', 'Lyanna_Stark', 'Rhaegar_Targaryen', 'Rickard_Stark', 'Aerys_II_Targaryen', 'Robb_Stark', 'Lysa_Tully', 'Robert_Arryn', 'Vardis_Egen', 'Bronn', 'Gyles_Rosby', 'Harys_Swyft', 'Steffon_Baratheon', 'Tommen_Baratheon', 'Edric_Storm', 'Mya_Stone', 'Gendry', 'Aerys_II', 'Rhaelle_Targaryen', 'Aegon_V', 'Joffrey_Baratheon', 'Balon_Greyjoy', 'Theon_Greyjoy', 'Jon_Snow', 'Daenerys_Targaryen', 'Barristan_Selmy', 'Sandor_Clegane', 'Drogo', 'Harrold_Hardyng', 'Jaehaerys_I', 'Aemma_Arryn', 'Viserys_I_Targaryen', 'Rhaenyra_Targaryen', 'Daeron_II', 'Nymeria', 'Aegon_VI_Targaryen', 'Khal_Drogo', 'Aegor_Rivers', 'Maelys_Blackfyre', 'Viserys_Targaryen', 'Illyrio_Mopatis', 'Morros_Slynt', 'Danos_Slynt', 'Samwell_Tarly', 'Emmon_Frey', 'Roslin_Frey', 'Marq_Piper', 'Clement_Piper', 'Kevan_Lannister', 'Tytos_Blackwood', 'Roose_Bolton', 'Helman_Tallhart', 'Walder_Frey', 'Brynden_Tully', 'Ryman_Frey', 'Jeyne_Westerling', 'Joanna_Lannister', 'Benjen_Stark', 'Joffrey', 'Olenna_Tyrell', 'Cersei', 'Marillion', 'Arianne_Martell', 'Doran_Martell', 'Viserys_III_Targaryen', 'Jon_Connington', 'Utherydes_Wayn', 'Desmond_Grell', 'Jonos_Bracken', 'Karyl_Vance', 'Jason_Mallister', 'Lothar_Frey', 'Bran_Stark', 'Rickon_Stark', 'Loras_Tyrell', 'Lyarra_Stark', 'Barbrey_Dustin', 'Aenys_I_Targaryen', 'Maegor_I_Targaryen', 'Jaehaerys_I_Targaryen', 'Aegon_II_Targaryen', 'Aegon_III_Targaryen', 'Daeron_I_Targaryen', 'Baelor_I_Targaryen', 'Viserys_II_Targaryen', 'Aegon_IV_Targaryen', 'Daeron_II_Targaryen', 'Aerys_I_Targaryen', 'Maekar_I_Targaryen', 'Aegon_V_Targaryen', 'Jaehaerys_II_Targaryen', 'Haegon_Blackfyre', 'Renly_I_Baratheon', 'Stannis_I_Baratheon', 'Maegor_the_Cruel', 'Baelor_the_Blessed', 'Aegon_Targaryen', 'Jorah_Mormont', 'Visenya_Targaryen', 'Brynden_Rivers', 
'Randyll_Tarly', 'Lyn_Corbray', 'Jeor_Mormont', 'Harras_Harlaw', 'Brienne_of_Tarth', 'Dunstan_Drumm', 
'Ashara_Dayne', 'Jory_Cassel', 'Raymun_Darry', 'Jeyne_Poole', 'Beth_Cassel', 'Robar_Royce', 'Hizdahr_zo_Loraq', 'Rhaella_Targaryen', 'Rhaego', 'Paxter_Redwyne', 'Ilyrio_Mopatis', 'File:Fire_and_blood_by_michael_c_hayes-d74jlwu.jpg', 'Rhaego_Targaryen', 'File:Daenerys_targareyen_by_teiiku.jpeg', 'Drogon', 
'File:Daenerys_by_aida20-d51j6ck.png', 'File:Daenerys_targaryen_by_vvveverka.jpeg', 'File:Daenerys_by_samtronika.png', 'File:Daenerys_by_mischievous_martian.jpeg', 'File:Daenerys_by_willpheonix-d5347cr.jpeg', 'File:Daenerys_the_queen_in_meereen_by_monkey19934-d56vyle.jpeg', 'File:Daenerys_khal_drogo_my_sun_and_stars_by_gali_miau-d4e06rl.jpeg', 'File:Daenerys_targaryen_study_with_videos_by_zombiesandwich-d6oms6m.jpg', 'File:Daenerys-mother-of-dragons-by-krewi.jpg', 'File:Targaryen_by_aprilis420-d5mnto7.jpg', 'File:Audience_Hall_by_Marc_Simonetti.jpg', 'Brienne_Tarth', 'Oberyn_Martell', 'Arthur_Dayne', 'Oswell_Whent', 'Roland_Crakehall', 'Bryce_Caron', 'Andar_Royce', 'Eddard_Karstark', 'Torrhen_Karstark', 'Margaery_Tyrell', 'Catelyn_Tully', 'Trystane_Martell', 'Selyse_Florent', 'Shireen_Baratheon', 'Victarion_Greyjoy', 'Davos_Seaworth', 'Garlan_Tyrell', 'Alester_Florent', 'Axell_Florent', 'Aemon_Targaryen', 'Ramsay_Bolton', 'Asha_Greyjoy', 'Alys_Karstark', 'Arrec_Durrandon', 'Harrag_Hoare', 'Ravos_Hoare', 'Harmund_II_Hoare', 'Harmund_III_Hoare', 'Hagon_Hoare', 'Qhorwyn_Hoare', 'Harlan_Hoare', 'Halleck_Hoare', 'Osmund_Strong', 'Lucamore_Strong', 'Lyonel_Strong', 'Harwin_Strong', 'Larys_Strong', 'Simon_Strong', 'Kermit_Tully', 'Cregan_Stark', 'Walter_Whent', 'Willis_Wode', 'Aenys_I', 'Aenar_Targaryen', 'Argilac_the_Arrogant', 'Rhaena_Targaryen', 'Elaena_Targaryen', 'Baelor_Targaryen', 'Myriah_Martell', 'Shiera_Seastar', 'Aegon_Blackfyre', 'Aemon_Blackfyre', 'Daenerys_Martell', 'Artos_Stark', 'Damon_Lannister_(lord)', 'Aerion_Targaryen', 'Aemon_Targaryen_(Maester)', 'Rhaenys_Targaryen', 'Dalton_Greyjoy', 'Quentyn_Ball', 'Tybolt_Lannister', 'Roger_Reyne', 'Ellyn_Reyne', 'Tytos_Lannister', 'Cerenna_Lannister', 'Damion_Lannister', 'Daven_Lannister', 'Janei_Lannister', 'Lucion_Lannister', 'Martyn_Lannister', 'Myrielle_Lannister', 'Stafford_Lannister', 'Rickard_Karstark', 'Tyrek_Lannister', 'Tygett_Lannister', 'Joy_Hill', 'Loren_Lannister', 'Gerold_Lannister', 'Aerion_Targaryen_(son_of_Daemion)', 'Valaena_Velaryon', 'File:Aegon,_visenya,_rhaenys.png', 'File:350px-Aegon_the_Conqueror.webp', 'Benjicot_Blackwood', 'Alicent_Hightower', 'Aemond_Targaryen', 'Aegon_II', 'Alyssa_Targaryen', 'Rhea_Royce', 'Laena_Velaryon', 
'Visenya_Targaryen_(daughter_of_Rhaenyra)', 'Rhaena_Targaryen_(daughter_of_Laena_Velaryon)', 'Baela_Targaryen', 'Aegon_III', 'Larra_Rogare', 'Naerys_Targaryen', 'Alysanne_(daughter_of_Aegon_IV)', 'Lily', 
'Willow_(daughter_of_Aegon_IV)', 'Rosey_(daughter_of_Aegon_IV)', 'Bellanora_Otherys', 'Narha_Otherys', 'Balerion_Otherys', 'Mya_Rivers', 'Gwenys_Rivers', 'Daeron_I', 'Baelor_I', 'Falena_Stokeworth', 'Bellegere_Otherys', 'Calla_Blackfyre', 'Baelor_Breakspear', 'Rhaegel_Targaryen', 'Baelor_Targaryen_(son_of_Daeron_II)', 'Dyanna_Dayne', 'Daella_Targaryen_(daughter_of_Maekar_I)', 'Rhae_Targaryen', 'Imry_Florent', 'Euron_Greyjoy', 'Jeyne_Marbrand', 'Genna_Lannister', 'Genna_Lannister_Frey', 'Cleos_Frey', 'Illyrio', 'Denyo_Terys', 'Ternesio_Terys', 'Yorko_Terys', 'Kindly_Man', 'Waif', 'Clegane_(Father_of_Gregor_and_Sandor)', 'Balon_Swann', 'File:Gregor.jpeg', 'File:Gregor_middle.jpg', 'File:Gregor_clegane_baby_smash.jpeg', 'Aurane_Waters', 'Gilly', 'Dareon', 'Podrick_Payne', 'Maegor_I', 'Aeron_Greyjoy', 'Quentyn_Martell', 'Durran', 'Elinor_Tyrell', 'Garth_Tyrell', 'Janna_Tyrell', 'Medwick_Tyrell', 'Megga_Tyrell', 'Mina_Tyrell', 'Olene_Tyrell', 'Olymer_Tyrell', 'Raymund_Tyrell', 'Rickard_Tyrell', 'Theodore_Tyrell', 'Victaria_Tyrell', 'Willas_Tyrell', 'Luthor_Tyrell', 'Quentin_Tyrell', 'Victor_Tyrell', 'Tommen_Tully', 'Agnes_Blackwood', 'Grover_Tully', 'Elmo_Tully', 'Lyonel_Baratheon', 'Argella_Durrandon', 'Ormund_Baratheon', 'Argilac_Durrandon', 'Ronnel_Arryn_(king)', 'Daenys_Targaryen', 'Aegon_I', 'Edwell_Celtigar', 'Viserys_I', 'Viserys_II', 'Valarr_Targaryen', 'Aerys_I', 'Jaehaerys_II', 'Danaerys_Targaryen', 
'Wyl_of_Wyl', 'Walter_Wyl', 'Rogar_Baratheon', 'Brella', 'Alerie_Hightower', 'Benedict_I_Justman', 'Benedict_II_Justman', 'Bernarr_II_Justman', 'Roderick_Blackwood', 'Garth_Greenhand', 'Yohn_Royce', 'Harrion_Karstark', 'Quincy_Cox', 'Lyle_Crakehall', 'Hoster_Blackwood', 'Lucas_Blackwood', 'Walder_Frey_(Black)', 'Harry_Rivers', 'Rolph_Spicer', 'Sybell_Spicer', 'Dacey_Mormont', 'Raynald_Westerling', 'Jon_Umber_(Greatjon)', 'Patrek_Mallister', 'Danwell_Frey', 'Hosteen_Frey', 'Leslyn_Haigh', 'Whalen_Frey', 'Raymund_Frey', 'Walder_Rivers', 'Garse_Goodbrook', 'Benfrey_Frey', 'Ellaria_Sand', 'Qarlton_II_Durrandon', 'Benedict_Rivers', 'Shiera_Blackwood', 'Laenor_Velaryon', 'Alysanne_Blackwood', 'Melissa_Blackwood', 'Robert_Blackwood', 'Brynden_Blackwood', 'Edmund_Blackwood', 'Alyn_Blackwood', 'Bethany_Blackwood', 'Melantha_Blackwood', 'Edwyle_Stark', 'Jocelyn_Stark', 'Elys_Waynwood', 'Barbara_Bracken', 'Jayne_Bracken', 'Catelyn_Bracken', 'Bess_Bracken', 'Alysanne_Bracken', 'Balon_IX_Greyjoy', 'Harren_the_Black', 
'Jaehaerys_the_Conciliator', 'Addam_Velaryon', 'Shaena_Targaryen', 'Daeron_Targaryen_(son_of_Aerys_II)', 'Aegon_Targaryen_(son_of_Aerys_II)', 'Aegon_Targaryen_(son_of_Rhaegar)', 'Daenerys', 'File:Rhaegar_Targaryen.jpg', 'File:350px-Rhaegar_Targaryen_Elia_Martell_marriage.jpg', 'File:766ae003452aa7d5ec4faa5cd99d8dfe.jpg', 'File:DMlVd5LWAAAbQDS.jpg', 'File:250px-Denkata5698_Rhaegar_Elia_goodbye.webp', 'Marna_Locke', 'Arya_Flint', 'Jaehaerys_Targaryen_(son_of_Aerys_II)', 'Denys_Darklyn', 'Ser_Barristan_Selmy', 'Meera_Reed', 'Ygritte', 'Alayne_Stone', 'Maron_Greyjoy', 'Maege_Mormont', 'Stevron_Frey', 'Gawen_Westerling', 'Tytos_Brax', 'Willem_Lannister', 'Tion_Frey', 'Mathis_Rowan', 'Edwyn_Frey', 'Aemon_II_Targaryen', 'Osmund_Kettleblack', 'Tanda_Stokeworth', 'Tyrion_Tanner', 'Falyse_Stokeworth', 'Balman_Byrch', 'Dorna_Swyft', 'Steffon_Swyft', 'Shierle_Swyft', 'Aemon_(son_of_Maekar_I)', 'Daemon_I_Blackfyre', 'John_the_Oak', 'Maegor_Targaryen', 'Glendon_Flowers', 'Creighton_Longbough', 'Delena_Florent', 'Mychel_Redfort', 'Gregor_Goode', 'Griffith_Goode', 'Robin_Darklyn', 'Humfrey', 'Erryk_Cargyll', 'Arryk_Cargyll', 'Rickard_Thorne', 'Mervyn_Flowers', 'Alyn_Connington', 'Tom_Costayne', 'Harwin', 'Daeron_Targaryen_(son_of_Aegon_V)', 'Olenna_Redwyne', 'Jorah_Mormont#Jorah_Mormont', 'Matarys_Targaryen', 'Maegon_Targaryen', 'Gaemon_Targaryen_(son_of_Aenar)', 'Aegon_Targaryen_(son_of_Gaemon)', 'Elaena_Targaryen_(daughter_of_Gaemon)', 'Aelyx_Targaryen', 'Baelon_Targaryen_(son_of_Aerys)', 'Daemion_Targaryen', 'Ceryse_Hightower', 'Jeyne_Westerling_(wife_of_Maegor_I)', 'Aegon_Targaryen_(son_of_Jaehaerys_I)', 'Valerion_Targaryen', 'Vaegon_Targaryen', 'Maegelle_Targaryen', 'Viserra_Targaryen', 'Gael_Targaryen', 'Daella_Targaryen_(daughter_of_Jaehaerys_I)', 'Baelon_Targaryen_(son_of_Viserys_I)', 'Daenaera_Velaryon', 'Jon_Waters', 'Jeyne_Waters', 'Daenora_Targaryen', 'Maegor_Targaryen_(son_of_Aerion)', 'Quellon_Greyjoy', 'Urrigon_Greyjoy', 'Lyman_Darry', 'Amerei_Frey', 'Mariya_Darry', 'Lyonel_Selmy', 'Bharbo', 'Arwood_Frey', 'Donnel_Haigh', 'Harys_Haigh', 'Tywin_Frey', 'Jeyne_Darry', 'Willem_Frey', 'Lyonel_Frey', 'Melesa_Crakehall', 'Walder_Frey_(son_of_Emmon)', 'Joyeuse_Erenford', 'Kyra_Frey', 'Walder_Goodbrook', 'Jeyne_Goodbrook', 'Dickon_Tarly', 'Lewys_Piper', 'Aegon_Targaryen_(Son_of_Aenys_I)', 'Lythene_Frey', 'Jonos_Arryn', 'Roland_I_Arryn', 'Anya_Waynwood', 'Humfrey_Beesbury', 'Deana_Hardyng', 'Walton_Frey', 'Steffon_Frey', 'Walda_Frey_(daughter_of_Walton)', 'Bryan_Frey', 'Horton_Redfort', 'Jon_Redfort', 'Ysilla_Royce', 'Perra_Royce', 'Jennis_Templeton', 'Geremy_Frey', 'Gaemon_Targaryen_(son_of_Jaehaerys_I)', 'Annara_Farring', 'Rennifer_Longwaters', 'Josua_Massey', 'Alarra_Massey', 'Aethan_Velaryon', 'Samantha_Stokeworth', 'Androw_Farman', 'Bronn_of_the_Blackwater', 'Jon_Cafferen', 'Alys_Oakheart', 'Allyria_Dayne', 'Rhaenys_Targaryen_(daughter_of_Aerion)', 'Beron_Stark', 'Veron_Greyjoy', 'Bittersteel', 'Harlon_Greyjoy', 'Quenton_Greyjoy', 'Donel_Greyjoy', 'Robin_Greyjoy', 'Tommen_Costayne', 'File:Visereys_by_amoka.jpg', 'File:AegonI-Targaryen.jpg', 'File:Maegor_I.jpg', 'File:Jaehaerys_I_Targaryen.jpg', 'File:File-Rhaenys.jpeg', 'File:Visenya-Targaryen.jpg', 'File:Aenys_I_Targaryen.jpg', 'File:Viserys_I_Targaryen.jpg', 
'File:Aegon_II_Targaryen.jpg', 'File:Aegon_III_Targaryen.jpg', 'File:Daeron_I_Targaryen.jpg', 'File:Baelor_I_Targaryen.jpg', 'File:Viserys_II_Targaryen.jpg', 'File:Aegon_IV_Targaryen.jpg', 'File:DaemonI-Blackfyre.jpg', 'File:Daeron_II_Targaryen.jpg', 'File:Aerys_I_Targaryen.jpg', 'File:MaekarI-Targaryen.jpg', 'File:Aegon_V_Targaryen.jpg', 'File:Aemon_by_amoka.jpg', 'File:Jaehaerys_II_Targeryen.jpg', 'File:Lord_Commander_Rivers.png', 'File:25_middle.jpg', 'Sawane_Botley', 'Germund_Botley', 'Sigorn', 'Eddison_Tollett', 'Garth_the_Gardener', 'Mellario_of_Norvos', 'Nymeria_Sand', 'Davos_Dayne', 'Bloodraven', 
'Lyanna_Mormont', 'Ramsay_Snow', 'Jon_Stark', 'Rickard_Stark_(king)', 'File:Bonnie_prince_charlie.jpg', 'Addam_Marbrand', 'Melessa_Florent', 'Talla_Tarly', 'Hobber_Redwyne', 'Horas_Redwyne', 'Aemon_Targaryen_(Son_of_Maekar_I)', 'Jack_Bulwer', 'Aenys_Frey', 'Jared_Frey', 'Luceon_Frey', 'Symond_Frey', 'Jammos_Frey', 'Morya_Frey', 'Tyta_Frey', 'Perwyn_Frey', 'Willamen_Frey', 'Olyvar_Frey', 'Arwyn_Frey', 'Wendel_Frey', 'Colmar_Frey', 'Waltyr_Frey', 'Waltyr_Frey', 'Elmar_Frey', 'Shirei_Frey', 'Bethany_Rosby', 
'Lady_Stoneheart', 'Benfred_Tallhart', 'Eddara_Tallhart', 'Galbart_Glover', 'Robett_Glover', 'Leobald_Tallhart', 'Cyrenna_Swann', 'Amarei_Crakehall', 'Alyssa_Blackwood', 'Sarya_Whent', 'Perriane_Frey', 'Donnel_Waynwood', 'Aegon_Frey', 'Petyr_Frey', 'Eleyna_Westerling', 'Rollam_Westerling', 'Jason_Lannister_(son_of_Gerold)', 'Marla_Prester', 'Damon_Lannister_(son_of_Jason)', 'Lynora_Hill', 'Gendry_Waters', 'Tyrion', 'Erryk', 'Arryk', 'Gilbert_of_the_Vines', 'File:Jon_connington_by_an_jing.png', 'File:Jon_connington_2_by_an_jing.png', 'File:Jon_the_griff_connington_by_acazigot.jpeg', 'File:Rhaegar_and_jon_connington_by_icklenickel.png', 'File:Jon_connington.png', 'Robin_Ryger', 'Three-Eyed_Crow', 'File:Bran_stark_by_teiiku.jpeg', 'File:Bran_stark_by_blue_zombie.jpeg', 'File:Brandon_stark_by_sykaaa-d4ptssv.jpeg', 'Varamyr_Sixskins', 'Jon_Heddle', 'Branda_Stark', 'Donella_Hornwood', 'Naerys_I_Targaryen', 'Herndon_of_the_Horn', 'Harlon_the_Hunter', 'Lyonel_Corbray', 'Lucas_Corbray', 'Rodrik_Harlaw', 'Erich_V_Harlaw', 'Harron_Harlaw', 'Gorold_Goodbrother', 'Gwynesse_Harlaw', 'Illifer', 'Rufus_Leek', 'Denys_Drumm', 'Donnel_Drumm', 'Maester_Aemon_Targaryen', 'Martyn_Cassel', 'Hallyne', 'Vayon_Poole', 'Martyn_Rivers', 'Desmera_Redwyne', 'Walda_Frey_(daughter_of_Merrett)', 'Walder_Frey_(son_of_Merrett)', 'Burton_Crakehall', 'Tybolt_Crakehall', 'Merlon_Crakehall', 'Bryen_Caron', 'Hullen', 'Old_Nan', 'Ryam_Florent', 
'Erren_Florent', 'File:Victorion.jpeg', 'Steffarion_Sparr', 'Wex_Pyke', 'Alekyne_Florent', 'Leonette_Fossoway', 'Colin_Florent', 'Rylene_Florent', 'Melara_Crane', 'Rhea_Florent', 'Clydas', 'Mully', 'Cregan_Karstark', 'Euron_III_Greyjoy', 'Rohanne_Webber', 'Wylis_Manderly', 'Halys_Hornwood', 'Walder_Frey_(Little)', 'Dormund', 'Walda_Frey_(Fat_Walda_Frey)', 'Reek', 'Daryn_Hornwood', 'Beren_Tallhart', 'Larence_Snow', 'Berena_Hornwood', 'Medger_Cerwyn', 'Robard_Cerwyn', 'Aregelle_Stark', 'Brandon_Tallhart', 'Lelia_Lannister', 'Urras_Greyiron', 'Erich_I_Greyiron', 'Urragon_III_Greyiron', 'Torgon_Greyiron', 'Urragon_IV_Greyiron', 'Tristifer_Botley', 'Sargon_Botley', 'Harren_Botley', 'Symond_Botley', 'Harlon_Botley', 'Vickon_Botley', 'Bennarion_Botley', 'Balon_Botley', 'Quellon_Botley', 'Lucimore_Botley', 'The_Sparr', 'Alys_Rivers', 'Aemon_Targaryen_(Son_of_Jaehaerys_I)', 'Oscar_Tully', 'Sabitha_Frey', 'Rickon_Stark_(Son_of_Benjen)', 'Gilliane_Glover', 'Sara_Snow', 'Arra_Norrey', 'Lynara_Stark', 'Rickon_Stark_(Son_of_Cregan)', 'Sarra_Stark', 'Alys_Stark', 'Raya_Stark', 'Mariah_Stark', 'Jonnel_Stark', 'Edric_Stark_(Son_of_Cregan)', 'Lyanna_Stark_(Daughter_of_Cregan)', 'Barthogan_Stark', 'Brandon_Stark_(Son_of_Cregan)', 'Bennard_Stark', 'Jeyne_Manderly', 'Serena_Stark', 'Sansa', 'Alleras', 'Baelor_II_Targaryen', 'Gerrick_Kingsblood', 'Lorra_Royce', 'Donnor_Stark', 'Cerissa_Brax', 'Manfred_Dondarrion', 'Jason_Lannister', 'Ellyn_Tarbeck', 'Walderan_Tarbeck', 'Ella_Lannister', 'Cerelle_Lannister', 'Cerissa_Lannister', 'Teora_Kyndall', 'Androw_Ashford', 'Robert_Reyne', 'Reynard_Reyne', 'Tion_Lannister', 'Rohanne_Tarbeck', 'Cyrelle_Tarbeck', 'Tion_Tarbeck', 'Tywald_Lannister', 'Last_Lord_Tarbeck', 'Andros_Brax', 'Flement_Brax', 'Rupert_Brax', 'Robert_Brax', 'Robert_Brax_(son_of_Flement)', 'Walder_Brax', 'Jon_Brax', 'Shiera_Crakehall', 'Sebaston_Farman', 'Marq_Farman', 'Franklyn_Farman', 'Lysa_Farman', 'Jeyne_Farman', 'Gareth_Clifton', 'Alysanne_Farman', 'Antario_Jast', 'Lanna_Lannister', 'Leonella_Lefford', 'Myranda_Lefford', 'Damon_Marbrand', 'Melwyn_Sarsfield', 'Selmond_Stackspear', 'Alys_Stackspear', 'Alyn_Stackspear', 'Joanna_Swyft', 'Alyn_Tarbeck', 'Johanna_Westerling', 'Titus_Peake', 'Florys_the_Fox', 'Margot_Lannister', 'Moro', 'Haggo', 'Qotho', 'Rhogoro', 'Tomard', 'Lorent_Caswell', 'Orbert_Caswell', 'Armond_Caswell', 'Taena_Merryweather', 'Rowan_Gold-Tree', 'Hosman_Norcross', 'Alester_Norcross', 'Renly_Norcross', 'Norbert_Vance', 'Tyana_Wylde', 'Morgan_Wylde', 'Coryanne_Wylde', 'Howard_Bullock', 'Samwell_Blackwood', 'Loren_I_Lannister', 'Aegon_Targaryen_(Son_of_Jaehaerys_I)', 'Daenerys_Targaryen_(Daughter_of_Jaehaerys_I)', 'Daella_Targaryen_(Daughter_of_Jaehaerys_I)', 'Gaemon_Targaryen_(Son_of_Jaehaerys_I)', 'Aegon_Targaryen_(Son_of_Baelon)', 'Donnel_Hightower', 'Cletus_Yronwood', 'Margaret_Karstark', 'Brandon_Stark_(son_of_Cregan)', 'Alyn_Marbrand', 'Walder_Frey_(son_of_Emmon_Frey)', 'Leo_Tyrell_(Lazy)', 'Gylbert_Farwynd', 'Hibald', 'Naggle', 'Hal_(Hairy)', 'Kedge', 'Lew', "High_Septon_(Tyrion's)", 'Lambert_Turnberry', 'Alyce_Graceford', 'Duskendale_Captain', "Captain's_Sister", 'Durran_II_Durrandon', 'Durran_Durrandon_(the_Devout)', 'Omer_Florent', 'Merrell_Florent', 'Rycherd_Crane', 'Lysa_Meadows', 'Rose_of_Red_Lake', 'Alysanne_Bulwer', 'Bors_the_Breaker', 'Osbert_Serry', 'Talbert_Serry', 'Lia_Serry', 'Owen_Oakenshield', 'Luthor_Tyrell_(son_of_Moryn)', 'Elyn_Norridge', 'Leo_Blackbar', 'Luthor_Tyrell_(son_of_Theodore)', 'Leo_Tyrell_(son_of_Victor)', 'Jon_Bulwer', 'Robert_Ashford', 'Prunella_Celtigar', 'Prudence_Celtigar', 'Cayn', 'Gage', 'Albar_Royce', 'Iron_Emmett', 'Maris_the_Maid', 'Foss_the_Archer', 'Ellyn_Ever_Sweet', 'Brandon_of_the_Bloody_Blade', 'Uthor_of_the_High_Tower', 'Prentys_Tully', 'Rhaegar_Frey', 'Hoarfrost_Umber', 'Ronel_Rivers', 'Wynafrei_Whent', 'Bellena_Hawick', 'Ryella_Frey', 'Androw_Frey', 'Alyn_Frey', 'Hostella_Frey', 'Little_Walder_Frey', 'Alyn_Haigh', 'Sylwa_Paege', 'Hoster_Frey', 'Merianne_Frey', 'Roslin_Tully', 'Harmen_Uller', 'Amos_Bracken', 'Rickon_Stark_(son_of_Cregan)', 'Jasper_Waynwood', 'Renfred_Rykker', 'Gawen_Glover', 'Erena_Glover', 'Torghen_Flint', 'Donnel_Flint', 'Artos_Flint', 'Marsella_Waynwood', 'Black_Walder_Frey', 'Bran', 'Penny_Jenny', 'Walton_Stark_(Son_of_Brandon)', 'Griff', 'Aerys_Targaryen_(son_of_Aegon)', 'Daenerys_Targaryen_(daughter_of_Jaehaerys_I)', 'Elys_Arryn', 'Fat_Walda_Frey', 'Ryella_Royce', 'Viserys_Targaryen_(Son_of_Aenys_I)', 'Lyman_Lannister', 'Kedge_Whiteye', 'Guncer_Sunglass', 'Alayne_Royce', 'Jocasta_Lannister', 'Tyler_Hill', 'Merrell_Bullock', 
'Cassella_Staunton', 'Jonah_Mooton', 'Braxton_Beesbury', 'Perianne_Moore', 'Dunstan_Pryor', 'Alys_Karstark_(Wife_of_Brandon)', 'Lonnel_Snow', 'Rodwell_Stark', 'Arsa_Stark', 'Ygon_Farwynd', 'Harmund_Sharp', 'Deziel_Dalt', 'Emmett', 'Dolorous_Edd', 'Andrey_Dalt', 'Aegon_Frey_(son_of_Aenys)', 'Wynafryd_Manderly', 'Wylla_Manderly', 'Sallei_Paege', 'Walder_Frey_(son_of_Jammos)', 'Dickon_Frey', 'Mathis_Frey', 'Hubard_Rambton', 'Walder_Frey_(Big)', 'Jeyne_Beesbury', 'Robert_Frey_(son_of_Rhaegar)', 'Walda_Frey_(daughter_of_Rhaegar)', 'Jonos_Frey', 'Walder_Haigh', 'Tysane_Frey', 'Walda_Frey_(daughter_of_Lothar)', 
'Emberlei_Frey', 'Meha', 'Bump', 'Harrold_Rogers', 'Big_Walder_Frey', 'Leona_Woolfield', 'Torwynd', 'Munda', 'Dryn', 'Wylla_Fenn', 'Cregard_Stark', 'Torrhen_Stark_(Son_of_Edric)', 'Arrana_Stark', 'Varamyr', 'Benjen_Stark_(Lord)', 'Lysa_Locke', 'Sansa_Stark_(Daughter_of_Rickon)', 'Robyn_Ryswell', 'Benjen_Stark_(Son_of_Bennard)', 'Brandon_Stark_(Son_of_Bennard)', 'Elric_Stark', 'Jon_Umber_(Husband_of_Serena)', "Gerrick_Kingsblood's_Youngest_Daughter", 'Leana_Frey', 'Steffon_Stackspear', 'Surly_lad', 'Borys_Baratheon', 'Alyn_Bullock', 'Raylon_Rivers', 'Orryn_Baratheon', 'Norman_Hightower', 'Black_Jack_Bulwer', 'Leo_Tyrell_(son_of_Moryn)', 'Alys_Beesbury', 'Uther_Peake', 'Black_Maris', 'Peremore_Hightower', 'Lucinda_Tully', 'Ella_Broome', 'Humfrey_Bracken', 'Brandon_Stark_(Father_of_Walton)', 'Alaric_Stark', 
'Lord_Tarbeck_(Son_of_Alyn)', 'Lord_Sunglass', 'Melony_Piper', 'Lord_Staunton_(Father_of_Cassella)', 'Myriame_Manderly', 'Missandei', 'Longspear_Ryk', 'Ryk', 'Osric_Umber', 'Ronnal_Baratheon', "Archon's_Daughter_(Jaehaerys_I)", 'Alarra_Stark', 'Jeyne_Westerling_(Wife_of_Maegor_I)', 'Jon_Piper']
"""
['Petyr_Baelish', 'Robert_I_Baratheon', 'Janos_Slynt', 'Edmure_Tully', 'Tyrion_Lannister', 'Lysa_Arryn', 'Hoster_Tully', 'Catelyn_Stark', 'Brandon_Stark', 'Robert_Baratheon', 'Eddard_Stark', 'Jon_Arryn', 
'Sansa_Stark', 'Daenerys_I_Targaryen', 'Barra', 'Jaime_Lannister', 'Joffrey_I_Baratheon', 'Tommen_I_Baratheon', 'Myrcella_Baratheon', 'Stannis_Baratheon', 'Shella_Whent', 'Harren_Hoare', 'Aegon_the_Conqueror', 'Daemon_Targaryen', 'Aegon_IV', 'Daemon_Blackfyre', 'Maekar_I', 'Minisa_Tully', 'Tywin_Lannister', 'Arya_Stark', 'Gregor_Clegane', 'Cersei_Lannister', 'Aegon_I_Targaryen', 'Orys_Baratheon', 'Argella_Baratheon', 'Mern_IX_Gardener', 'Renly_Baratheon', 'Mace_Tyrell', 'Harwyn_Hoare', 'Lyanna_Stark', 'Rhaegar_Targaryen', 'Rickard_Stark', 'Aerys_II_Targaryen', 'Robb_Stark', 'Lysa_Tully', 'Robert_Arryn', 'Vardis_Egen', 'Bronn', 'Gyles_Rosby', 'Harys_Swyft', 'Steffon_Baratheon', 'Tommen_Baratheon', 'Edric_Storm', 'Mya_Stone', 'Gendry', 'Aerys_II', 'Rhaelle_Targaryen', 'Aegon_V', 'Joffrey_Baratheon', 'Balon_Greyjoy', 'Theon_Greyjoy', 'Jon_Snow', 'Daenerys_Targaryen', 'Barristan_Selmy', 'Sandor_Clegane', 'Drogo', 'Harrold_Hardyng', 'Jaehaerys_I', 'Aemma_Arryn', 'Viserys_I_Targaryen', 'Rhaenyra_Targaryen', 'Daeron_II', 'Nymeria', 'Aegon_VI_Targaryen', 'Khal_Drogo', 'Aegor_Rivers', 'Maelys_Blackfyre', 'Viserys_Targaryen', 'Illyrio_Mopatis', 'Morros_Slynt', 'Danos_Slynt', 'Samwell_Tarly', 'Emmon_Frey', 'Roslin_Frey', 'Marq_Piper', 'Clement_Piper', 'Kevan_Lannister', 'Tytos_Blackwood', 'Roose_Bolton', 'Helman_Tallhart', 'Walder_Frey', 'Brynden_Tully', 'Ryman_Frey', 'Jeyne_Westerling', 'Joanna_Lannister', 'Benjen_Stark', 'Joffrey', 'Olenna_Tyrell', 'Cersei', 'Marillion', 'Arianne_Martell', 'Doran_Martell', 'Viserys_III_Targaryen', 'Jon_Connington', 'Utherydes_Wayn', 'Desmond_Grell', 'Jonos_Bracken', 'Karyl_Vance', 'Jason_Mallister', 'Lothar_Frey', 'Bran_Stark', 'Rickon_Stark', 'Loras_Tyrell', 'Lyarra_Stark', 'Barbrey_Dustin', 'Aenys_I_Targaryen', 'Maegor_I_Targaryen', 'Jaehaerys_I_Targaryen', 'Aegon_II_Targaryen', 'Aegon_III_Targaryen', 'Daeron_I_Targaryen', 'Baelor_I_Targaryen', 'Viserys_II_Targaryen', 'Aegon_IV_Targaryen', 'Daeron_II_Targaryen', 'Aerys_I_Targaryen', 'Maekar_I_Targaryen', 'Aegon_V_Targaryen', 'Jaehaerys_II_Targaryen', 'Haegon_Blackfyre', 'Renly_I_Baratheon', 'Stannis_I_Baratheon', 'Maegor_the_Cruel', 'Baelor_the_Blessed', 'Aegon_Targaryen', 'Jorah_Mormont', 'Visenya_Targaryen', 'Brynden_Rivers', 
'Randyll_Tarly', 'Lyn_Corbray', 'Jeor_Mormont', 'Harras_Harlaw', 'Brienne_of_Tarth', 'Dunstan_Drumm', 
'Ashara_Dayne', 'Jory_Cassel', 'Raymun_Darry', 'Jeyne_Poole', 'Beth_Cassel', 'Robar_Royce', 'Hizdahr_zo_Loraq', 'Rhaella_Targaryen', 'Rhaego', 'Paxter_Redwyne', 'Ilyrio_Mopatis', 'File:Fire_and_blood_by_michael_c_hayes-d74jlwu.jpg', 'Rhaego_Targaryen', 'File:Daenerys_targareyen_by_teiiku.jpeg', 'Drogon', 
'File:Daenerys_by_aida20-d51j6ck.png', 'File:Daenerys_targaryen_by_vvveverka.jpeg', 'File:Daenerys_by_samtronika.png', 'File:Daenerys_by_mischievous_martian.jpeg', 'File:Daenerys_by_willpheonix-d5347cr.jpeg', 'File:Daenerys_the_queen_in_meereen_by_monkey19934-d56vyle.jpeg', 'File:Daenerys_khal_drogo_my_sun_and_stars_by_gali_miau-d4e06rl.jpeg', 'File:Daenerys_targaryen_study_with_videos_by_zombiesandwich-d6oms6m.jpg', 'File:Daenerys-mother-of-dragons-by-krewi.jpg', 'File:Targaryen_by_aprilis420-d5mnto7.jpg', 'File:Audience_Hall_by_Marc_Simonetti.jpg', 'Brienne_Tarth', 'Oberyn_Martell', 'Arthur_Dayne', 'Oswell_Whent', 'Roland_Crakehall', 'Bryce_Caron', 'Andar_Royce', 'Eddard_Karstark', 'Torrhen_Karstark', 'Margaery_Tyrell', 'Catelyn_Tully', 'Trystane_Martell', 'Selyse_Florent', 'Shireen_Baratheon', 'Victarion_Greyjoy', 'Davos_Seaworth', 'Garlan_Tyrell', 'Alester_Florent', 'Axell_Florent', 'Aemon_Targaryen', 'Ramsay_Bolton', 'Asha_Greyjoy', 'Alys_Karstark', 'Arrec_Durrandon', 'Harrag_Hoare', 'Ravos_Hoare', 'Harmund_II_Hoare', 'Harmund_III_Hoare', 'Hagon_Hoare', 'Qhorwyn_Hoare', 'Harlan_Hoare', 'Halleck_Hoare', 'Osmund_Strong', 'Lucamore_Strong', 'Lyonel_Strong', 'Harwin_Strong', 'Larys_Strong', 'Simon_Strong', 'Kermit_Tully', 'Cregan_Stark', 'Walter_Whent', 'Willis_Wode', 'Aenys_I', 'Aenar_Targaryen', 'Argilac_the_Arrogant', 'Rhaena_Targaryen', 'Elaena_Targaryen', 'Baelor_Targaryen', 'Myriah_Martell', 'Shiera_Seastar', 'Aegon_Blackfyre', 'Aemon_Blackfyre', 'Daenerys_Martell', 'Artos_Stark', 'Damon_Lannister_(lord)', 'Aerion_Targaryen', 'Aemon_Targaryen_(Maester)', 'Rhaenys_Targaryen', 'Dalton_Greyjoy', 'Quentyn_Ball', 'Tybolt_Lannister', 'Roger_Reyne', 'Ellyn_Reyne', 'Tytos_Lannister', 'Cerenna_Lannister', 'Damion_Lannister', 'Daven_Lannister', 'Janei_Lannister', 'Lucion_Lannister', 'Martyn_Lannister', 'Myrielle_Lannister', 'Stafford_Lannister', 'Rickard_Karstark', 'Tyrek_Lannister', 'Tygett_Lannister', 'Joy_Hill', 'Loren_Lannister', 'Gerold_Lannister', 'Aerion_Targaryen_(son_of_Daemion)', 'Valaena_Velaryon', 'File:Aegon,_visenya,_rhaenys.png', 'File:350px-Aegon_the_Conqueror.webp', 'Benjicot_Blackwood', 'Alicent_Hightower', 'Aemond_Targaryen', 'Aegon_II', 'Alyssa_Targaryen', 'Rhea_Royce', 'Laena_Velaryon', 
'Visenya_Targaryen_(daughter_of_Rhaenyra)', 'Rhaena_Targaryen_(daughter_of_Laena_Velaryon)', 'Baela_Targaryen', 'Aegon_III', 'Larra_Rogare', 'Naerys_Targaryen', 'Alysanne_(daughter_of_Aegon_IV)', 'Lily', 
'Willow_(daughter_of_Aegon_IV)', 'Rosey_(daughter_of_Aegon_IV)', 'Bellanora_Otherys', 'Narha_Otherys', 'Balerion_Otherys', 'Mya_Rivers', 'Gwenys_Rivers', 'Daeron_I', 'Baelor_I', 'Falena_Stokeworth', 'Bellegere_Otherys', 'Calla_Blackfyre', 'Baelor_Breakspear', 'Rhaegel_Targaryen', 'Baelor_Targaryen_(son_of_Daeron_II)', 'Dyanna_Dayne', 'Daella_Targaryen_(daughter_of_Maekar_I)', 'Rhae_Targaryen', 'Imry_Florent', 'Euron_Greyjoy', 'Jeyne_Marbrand', 'Genna_Lannister', 'Genna_Lannister_Frey', 'Cleos_Frey', 'Illyrio', 'Denyo_Terys', 'Ternesio_Terys', 'Yorko_Terys', 'Kindly_Man', 'Waif', 'Clegane_(Father_of_Gregor_and_Sandor)', 'Balon_Swann', 'File:Gregor.jpeg', 'File:Gregor_middle.jpg', 'File:Gregor_clegane_baby_smash.jpeg', 'Aurane_Waters', 'Gilly', 'Dareon', 'Podrick_Payne', 'Maegor_I', 'Aeron_Greyjoy', 'Quentyn_Martell', 'Durran', 'Elinor_Tyrell', 'Garth_Tyrell', 'Janna_Tyrell', 'Medwick_Tyrell', 'Megga_Tyrell', 'Mina_Tyrell', 'Olene_Tyrell', 'Olymer_Tyrell', 'Raymund_Tyrell', 'Rickard_Tyrell', 'Theodore_Tyrell', 'Victaria_Tyrell', 'Willas_Tyrell', 'Luthor_Tyrell', 'Quentin_Tyrell', 'Victor_Tyrell', 'Tommen_Tully', 'Agnes_Blackwood', 'Grover_Tully', 'Elmo_Tully', 'Lyonel_Baratheon', 'Argella_Durrandon', 'Ormund_Baratheon', 'Argilac_Durrandon', 'Ronnel_Arryn_(king)', 'Daenys_Targaryen', 'Aegon_I', 'Edwell_Celtigar', 'Viserys_I', 'Viserys_II', 'Valarr_Targaryen', 'Aerys_I', 'Jaehaerys_II', 'Danaerys_Targaryen', 
'Wyl_of_Wyl', 'Walter_Wyl', 'Rogar_Baratheon', 'Brella', 'Alerie_Hightower', 'Benedict_I_Justman', 'Benedict_II_Justman', 'Bernarr_II_Justman', 'Roderick_Blackwood', 'Garth_Greenhand', 'Yohn_Royce', 'Harrion_Karstark', 'Quincy_Cox', 'Lyle_Crakehall', 'Hoster_Blackwood', 'Lucas_Blackwood', 'Walder_Frey_(Black)', 'Harry_Rivers', 'Rolph_Spicer', 'Sybell_Spicer', 'Dacey_Mormont', 'Raynald_Westerling', 'Jon_Umber_(Greatjon)', 'Patrek_Mallister', 'Danwell_Frey', 'Hosteen_Frey', 'Leslyn_Haigh', 'Whalen_Frey', 'Raymund_Frey', 'Walder_Rivers', 'Garse_Goodbrook', 'Benfrey_Frey', 'Ellaria_Sand', 'Qarlton_II_Durrandon', 'Benedict_Rivers', 'Shiera_Blackwood', 'Laenor_Velaryon', 'Alysanne_Blackwood', 'Melissa_Blackwood', 'Robert_Blackwood', 'Brynden_Blackwood', 'Edmund_Blackwood', 'Alyn_Blackwood', 'Bethany_Blackwood', 'Melantha_Blackwood', 'Edwyle_Stark', 'Jocelyn_Stark', 'Elys_Waynwood', 'Barbara_Bracken', 'Jayne_Bracken', 'Catelyn_Bracken', 'Bess_Bracken', 'Alysanne_Bracken', 'Balon_IX_Greyjoy', 'Harren_the_Black', 
'Jaehaerys_the_Conciliator', 'Addam_Velaryon', 'Shaena_Targaryen', 'Daeron_Targaryen_(son_of_Aerys_II)', 'Aegon_Targaryen_(son_of_Aerys_II)', 'Aegon_Targaryen_(son_of_Rhaegar)', 'Daenerys', 'File:Rhaegar_Targaryen.jpg', 'File:350px-Rhaegar_Targaryen_Elia_Martell_marriage.jpg', 'File:766ae003452aa7d5ec4faa5cd99d8dfe.jpg', 'File:DMlVd5LWAAAbQDS.jpg', 'File:250px-Denkata5698_Rhaegar_Elia_goodbye.webp', 'Marna_Locke', 'Arya_Flint', 'Jaehaerys_Targaryen_(son_of_Aerys_II)', 'Denys_Darklyn', 'Ser_Barristan_Selmy', 'Meera_Reed', 'Ygritte', 'Alayne_Stone', 'Maron_Greyjoy', 'Maege_Mormont', 'Stevron_Frey', 'Gawen_Westerling', 'Tytos_Brax', 'Willem_Lannister', 'Tion_Frey', 'Mathis_Rowan', 'Edwyn_Frey', 'Aemon_II_Targaryen', 'Osmund_Kettleblack', 'Tanda_Stokeworth', 'Tyrion_Tanner', 'Falyse_Stokeworth', 'Balman_Byrch', 'Dorna_Swyft', 'Steffon_Swyft', 'Shierle_Swyft', 'Aemon_(son_of_Maekar_I)', 'Daemon_I_Blackfyre', 'John_the_Oak', 'Maegor_Targaryen', 'Glendon_Flowers', 'Creighton_Longbough', 'Delena_Florent', 'Mychel_Redfort', 'Gregor_Goode', 'Griffith_Goode', 'Robin_Darklyn', 'Humfrey', 'Erryk_Cargyll', 'Arryk_Cargyll', 'Rickard_Thorne', 'Mervyn_Flowers', 'Alyn_Connington', 'Tom_Costayne', 'Harwin', 'Daeron_Targaryen_(son_of_Aegon_V)', 'Olenna_Redwyne', 'Jorah_Mormont#Jorah_Mormont', 'Matarys_Targaryen', 'Maegon_Targaryen', 'Gaemon_Targaryen_(son_of_Aenar)', 'Aegon_Targaryen_(son_of_Gaemon)', 'Elaena_Targaryen_(daughter_of_Gaemon)', 'Aelyx_Targaryen', 'Baelon_Targaryen_(son_of_Aerys)', 'Daemion_Targaryen', 'Ceryse_Hightower', 'Jeyne_Westerling_(wife_of_Maegor_I)', 'Aegon_Targaryen_(son_of_Jaehaerys_I)', 'Valerion_Targaryen', 'Vaegon_Targaryen', 'Maegelle_Targaryen', 'Viserra_Targaryen', 'Gael_Targaryen', 'Daella_Targaryen_(daughter_of_Jaehaerys_I)', 'Baelon_Targaryen_(son_of_Viserys_I)', 'Daenaera_Velaryon', 'Jon_Waters', 'Jeyne_Waters', 'Daenora_Targaryen', 'Maegor_Targaryen_(son_of_Aerion)', 'Quellon_Greyjoy', 'Urrigon_Greyjoy', 'Lyman_Darry', 'Amerei_Frey', 'Mariya_Darry', 'Lyonel_Selmy', 'Bharbo', 'Arwood_Frey', 'Donnel_Haigh', 'Harys_Haigh', 'Tywin_Frey', 'Jeyne_Darry', 'Willem_Frey', 'Lyonel_Frey', 'Melesa_Crakehall', 'Walder_Frey_(son_of_Emmon)', 'Joyeuse_Erenford', 'Kyra_Frey', 'Walder_Goodbrook', 'Jeyne_Goodbrook', 'Dickon_Tarly', 'Lewys_Piper', 'Aegon_Targaryen_(Son_of_Aenys_I)', 'Lythene_Frey', 'Jonos_Arryn', 'Roland_I_Arryn', 'Anya_Waynwood', 'Humfrey_Beesbury', 'Deana_Hardyng', 'Walton_Frey', 'Steffon_Frey', 'Walda_Frey_(daughter_of_Walton)', 'Bryan_Frey', 'Horton_Redfort', 'Jon_Redfort', 'Ysilla_Royce', 'Perra_Royce', 'Jennis_Templeton', 'Geremy_Frey', 'Gaemon_Targaryen_(son_of_Jaehaerys_I)', 'Annara_Farring', 'Rennifer_Longwaters', 'Josua_Massey', 'Alarra_Massey', 'Aethan_Velaryon', 'Samantha_Stokeworth', 'Androw_Farman', 'Bronn_of_the_Blackwater', 'Jon_Cafferen', 'Alys_Oakheart', 'Allyria_Dayne', 'Rhaenys_Targaryen_(daughter_of_Aerion)', 'Beron_Stark', 'Veron_Greyjoy', 'Bittersteel', 'Harlon_Greyjoy', 'Quenton_Greyjoy', 'Donel_Greyjoy', 'Robin_Greyjoy', 'Tommen_Costayne', 'File:Visereys_by_amoka.jpg', 'File:AegonI-Targaryen.jpg', 'File:Maegor_I.jpg', 'File:Jaehaerys_I_Targaryen.jpg', 'File:File-Rhaenys.jpeg', 'File:Visenya-Targaryen.jpg', 'File:Aenys_I_Targaryen.jpg', 'File:Viserys_I_Targaryen.jpg', 
'File:Aegon_II_Targaryen.jpg', 'File:Aegon_III_Targaryen.jpg', 'File:Daeron_I_Targaryen.jpg', 'File:Baelor_I_Targaryen.jpg', 'File:Viserys_II_Targaryen.jpg', 'File:Aegon_IV_Targaryen.jpg', 'File:DaemonI-Blackfyre.jpg', 'File:Daeron_II_Targaryen.jpg', 'File:Aerys_I_Targaryen.jpg', 'File:MaekarI-Targaryen.jpg', 'File:Aegon_V_Targaryen.jpg', 'File:Aemon_by_amoka.jpg', 'File:Jaehaerys_II_Targeryen.jpg', 'File:Lord_Commander_Rivers.png', 'File:25_middle.jpg', 'Sawane_Botley', 'Germund_Botley', 'Sigorn', 'Eddison_Tollett', 'Garth_the_Gardener', 'Mellario_of_Norvos', 'Nymeria_Sand', 'Davos_Dayne', 'Bloodraven', 
'Lyanna_Mormont', 'Ramsay_Snow', 'Jon_Stark', 'Rickard_Stark_(king)', 'File:Bonnie_prince_charlie.jpg', 'Addam_Marbrand', 'Melessa_Florent', 'Talla_Tarly', 'Hobber_Redwyne', 'Horas_Redwyne', 'Aemon_Targaryen_(Son_of_Maekar_I)', 'Jack_Bulwer', 'Aenys_Frey', 'Jared_Frey', 'Luceon_Frey', 'Symond_Frey', 'Jammos_Frey', 'Morya_Frey', 'Tyta_Frey', 'Perwyn_Frey', 'Willamen_Frey', 'Olyvar_Frey', 'Arwyn_Frey', 'Wendel_Frey', 'Colmar_Frey', 'Waltyr_Frey', 'Waltyr_Frey', 'Elmar_Frey', 'Shirei_Frey', 'Bethany_Rosby', 
'Lady_Stoneheart', 'Benfred_Tallhart', 'Eddara_Tallhart', 'Galbart_Glover', 'Robett_Glover', 'Leobald_Tallhart', 'Cyrenna_Swann', 'Amarei_Crakehall', 'Alyssa_Blackwood', 'Sarya_Whent', 'Perriane_Frey', 'Donnel_Waynwood', 'Aegon_Frey', 'Petyr_Frey', 'Eleyna_Westerling', 'Rollam_Westerling', 'Jason_Lannister_(son_of_Gerold)', 'Marla_Prester', 'Damon_Lannister_(son_of_Jason)', 'Lynora_Hill', 'Gendry_Waters', 'Tyrion', 'Erryk', 'Arryk', 'Gilbert_of_the_Vines', 'File:Jon_connington_by_an_jing.png', 'File:Jon_connington_2_by_an_jing.png', 'File:Jon_the_griff_connington_by_acazigot.jpeg', 'File:Rhaegar_and_jon_connington_by_icklenickel.png', 'File:Jon_connington.png', 'Robin_Ryger', 'Three-Eyed_Crow', 'File:Bran_stark_by_teiiku.jpeg', 'File:Bran_stark_by_blue_zombie.jpeg', 'File:Brandon_stark_by_sykaaa-d4ptssv.jpeg', 'Varamyr_Sixskins', 'Jon_Heddle', 'Branda_Stark', 'Donella_Hornwood', 'Naerys_I_Targaryen', 'Herndon_of_the_Horn', 'Harlon_the_Hunter', 'Lyonel_Corbray', 'Lucas_Corbray', 'Rodrik_Harlaw', 'Erich_V_Harlaw', 'Harron_Harlaw', 'Gorold_Goodbrother', 'Gwynesse_Harlaw', 'Illifer', 'Rufus_Leek', 'Denys_Drumm', 'Donnel_Drumm', 'Maester_Aemon_Targaryen', 'Martyn_Cassel', 'Hallyne', 'Vayon_Poole', 'Martyn_Rivers', 'Desmera_Redwyne', 'Walda_Frey_(daughter_of_Merrett)', 'Walder_Frey_(son_of_Merrett)', 'Burton_Crakehall', 'Tybolt_Crakehall', 'Merlon_Crakehall', 'Bryen_Caron', 'Hullen', 'Old_Nan', 'Ryam_Florent', 
'Erren_Florent', 'File:Victorion.jpeg', 'Steffarion_Sparr', 'Wex_Pyke', 'Alekyne_Florent', 'Leonette_Fossoway', 'Colin_Florent', 'Rylene_Florent', 'Melara_Crane', 'Rhea_Florent', 'Clydas', 'Mully', 'Cregan_Karstark', 'Euron_III_Greyjoy', 'Rohanne_Webber', 'Wylis_Manderly', 'Halys_Hornwood', 'Walder_Frey_(Little)', 'Dormund', 'Walda_Frey_(Fat_Walda_Frey)', 'Reek', 'Daryn_Hornwood', 'Beren_Tallhart', 'Larence_Snow', 'Berena_Hornwood', 'Medger_Cerwyn', 'Robard_Cerwyn', 'Aregelle_Stark', 'Brandon_Tallhart', 'Lelia_Lannister', 'Urras_Greyiron', 'Erich_I_Greyiron', 'Urragon_III_Greyiron', 'Torgon_Greyiron', 'Urragon_IV_Greyiron', 'Tristifer_Botley', 'Sargon_Botley', 'Harren_Botley', 'Symond_Botley', 'Harlon_Botley', 'Vickon_Botley', 'Bennarion_Botley', 'Balon_Botley', 'Quellon_Botley', 'Lucimore_Botley', 'The_Sparr', 'Alys_Rivers', 'Aemon_Targaryen_(Son_of_Jaehaerys_I)', 'Oscar_Tully', 'Sabitha_Frey', 'Rickon_Stark_(Son_of_Benjen)', 'Gilliane_Glover', 'Sara_Snow', 'Arra_Norrey', 'Lynara_Stark', 'Rickon_Stark_(Son_of_Cregan)', 'Sarra_Stark', 'Alys_Stark', 'Raya_Stark', 'Mariah_Stark', 'Jonnel_Stark', 'Edric_Stark_(Son_of_Cregan)', 'Lyanna_Stark_(Daughter_of_Cregan)', 'Barthogan_Stark', 'Brandon_Stark_(Son_of_Cregan)', 'Bennard_Stark', 'Jeyne_Manderly', 'Serena_Stark', 'Sansa', 'Alleras', 'Baelor_II_Targaryen', 'Gerrick_Kingsblood', 'Lorra_Royce', 'Donnor_Stark', 'Cerissa_Brax', 'Manfred_Dondarrion', 'Jason_Lannister', 'Ellyn_Tarbeck', 'Walderan_Tarbeck', 'Ella_Lannister', 'Cerelle_Lannister', 'Cerissa_Lannister', 'Teora_Kyndall', 'Androw_Ashford', 'Robert_Reyne', 'Reynard_Reyne', 'Tion_Lannister', 'Rohanne_Tarbeck', 'Cyrelle_Tarbeck', 'Tion_Tarbeck', 'Tywald_Lannister', 'Last_Lord_Tarbeck', 'Andros_Brax', 'Flement_Brax', 'Rupert_Brax', 'Robert_Brax', 'Robert_Brax_(son_of_Flement)', 'Walder_Brax', 'Jon_Brax', 'Shiera_Crakehall', 'Sebaston_Farman', 'Marq_Farman', 'Franklyn_Farman', 'Lysa_Farman', 'Jeyne_Farman', 'Gareth_Clifton', 'Alysanne_Farman', 'Antario_Jast', 'Lanna_Lannister', 'Leonella_Lefford', 'Myranda_Lefford', 'Damon_Marbrand', 'Melwyn_Sarsfield', 'Selmond_Stackspear', 'Alys_Stackspear', 'Alyn_Stackspear', 'Joanna_Swyft', 'Alyn_Tarbeck', 'Johanna_Westerling', 'Titus_Peake', 'Florys_the_Fox', 'Margot_Lannister', 'Moro', 'Haggo', 'Qotho', 'Rhogoro', 'Tomard', 'Lorent_Caswell', 'Orbert_Caswell', 'Armond_Caswell', 'Taena_Merryweather', 'Rowan_Gold-Tree', 'Hosman_Norcross', 'Alester_Norcross', 'Renly_Norcross', 'Norbert_Vance', 'Tyana_Wylde', 'Morgan_Wylde', 'Coryanne_Wylde', 'Howard_Bullock', 'Samwell_Blackwood', 'Loren_I_Lannister', 'Aegon_Targaryen_(Son_of_Jaehaerys_I)', 'Daenerys_Targaryen_(Daughter_of_Jaehaerys_I)', 'Daella_Targaryen_(Daughter_of_Jaehaerys_I)', 'Gaemon_Targaryen_(Son_of_Jaehaerys_I)', 'Aegon_Targaryen_(Son_of_Baelon)', 'Donnel_Hightower', 'Cletus_Yronwood', 'Margaret_Karstark', 'Brandon_Stark_(son_of_Cregan)', 'Alyn_Marbrand', 'Walder_Frey_(son_of_Emmon_Frey)', 'Leo_Tyrell_(Lazy)', 'Gylbert_Farwynd', 'Hibald', 'Naggle', 'Hal_(Hairy)', 'Kedge', 'Lew', "High_Septon_(Tyrion's)", 'Lambert_Turnberry', 'Alyce_Graceford', 'Duskendale_Captain', "Captain's_Sister", 'Durran_II_Durrandon', 'Durran_Durrandon_(the_Devout)', 'Omer_Florent', 'Merrell_Florent', 'Rycherd_Crane', 'Lysa_Meadows', 'Rose_of_Red_Lake', 'Alysanne_Bulwer', 'Bors_the_Breaker', 'Osbert_Serry', 'Talbert_Serry', 'Lia_Serry', 'Owen_Oakenshield', 'Luthor_Tyrell_(son_of_Moryn)', 'Elyn_Norridge', 'Leo_Blackbar', 'Luthor_Tyrell_(son_of_Theodore)', 'Leo_Tyrell_(son_of_Victor)', 'Jon_Bulwer', 'Robert_Ashford', 'Prunella_Celtigar', 'Prudence_Celtigar', 'Cayn', 'Gage', 'Albar_Royce', 'Iron_Emmett', 'Maris_the_Maid', 'Foss_the_Archer', 'Ellyn_Ever_Sweet', 'Brandon_of_the_Bloody_Blade', 'Uthor_of_the_High_Tower', 'Prentys_Tully', 'Rhaegar_Frey', 'Hoarfrost_Umber', 'Ronel_Rivers', 'Wynafrei_Whent', 'Bellena_Hawick', 'Ryella_Frey', 'Androw_Frey', 'Alyn_Frey', 'Hostella_Frey', 'Little_Walder_Frey', 'Alyn_Haigh', 'Sylwa_Paege', 'Hoster_Frey', 'Merianne_Frey', 'Roslin_Tully', 'Harmen_Uller', 'Amos_Bracken', 'Rickon_Stark_(son_of_Cregan)', 'Jasper_Waynwood', 'Renfred_Rykker', 'Gawen_Glover', 'Erena_Glover', 'Torghen_Flint', 'Donnel_Flint', 'Artos_Flint', 'Marsella_Waynwood', 'Black_Walder_Frey', 'Bran', 'Penny_Jenny', 'Walton_Stark_(Son_of_Brandon)', 'Griff', 'Aerys_Targaryen_(son_of_Aegon)', 'Daenerys_Targaryen_(daughter_of_Jaehaerys_I)', 'Elys_Arryn', 'Fat_Walda_Frey', 'Ryella_Royce', 'Viserys_Targaryen_(Son_of_Aenys_I)', 'Lyman_Lannister', 'Kedge_Whiteye', 'Guncer_Sunglass', 'Alayne_Royce', 'Jocasta_Lannister', 'Tyler_Hill', 'Merrell_Bullock', 
'Cassella_Staunton', 'Jonah_Mooton', 'Braxton_Beesbury', 'Perianne_Moore', 'Dunstan_Pryor', 'Alys_Karstark_(Wife_of_Brandon)', 'Lonnel_Snow', 'Rodwell_Stark', 'Arsa_Stark', 'Ygon_Farwynd', 'Harmund_Sharp', 'Deziel_Dalt', 'Emmett', 'Dolorous_Edd', 'Andrey_Dalt', 'Aegon_Frey_(son_of_Aenys)', 'Wynafryd_Manderly', 'Wylla_Manderly', 'Sallei_Paege', 'Walder_Frey_(son_of_Jammos)', 'Dickon_Frey', 'Mathis_Frey', 'Hubard_Rambton', 'Walder_Frey_(Big)', 'Jeyne_Beesbury', 'Robert_Frey_(son_of_Rhaegar)', 'Walda_Frey_(daughter_of_Rhaegar)', 'Jonos_Frey', 'Walder_Haigh', 'Tysane_Frey', 'Walda_Frey_(daughter_of_Lothar)', 
'Emberlei_Frey', 'Meha', 'Bump', 'Harrold_Rogers', 'Big_Walder_Frey', 'Leona_Woolfield', 'Torwynd', 'Munda', 'Dryn', 'Wylla_Fenn', 'Cregard_Stark', 'Torrhen_Stark_(Son_of_Edric)', 'Arrana_Stark', 'Varamyr', 'Benjen_Stark_(Lord)', 'Lysa_Locke', 'Sansa_Stark_(Daughter_of_Rickon)', 'Robyn_Ryswell', 'Benjen_Stark_(Son_of_Bennard)', 'Brandon_Stark_(Son_of_Bennard)', 'Elric_Stark', 'Jon_Umber_(Husband_of_Serena)', "Gerrick_Kingsblood's_Youngest_Daughter", 'Leana_Frey', 'Steffon_Stackspear', 'Surly_lad', 'Borys_Baratheon', 'Alyn_Bullock', 'Raylon_Rivers', 'Orryn_Baratheon', 'Norman_Hightower', 'Black_Jack_Bulwer', 'Leo_Tyrell_(son_of_Moryn)', 'Alys_Beesbury', 'Uther_Peake', 'Black_Maris', 'Peremore_Hightower', 'Lucinda_Tully', 'Ella_Broome', 'Humfrey_Bracken', 'Brandon_Stark_(Father_of_Walton)', 'Alaric_Stark', 
'Lord_Tarbeck_(Son_of_Alyn)', 'Lord_Sunglass', 'Melony_Piper', 'Lord_Staunton_(Father_of_Cassella)', 'Myriame_Manderly', 'Missandei', 'Longspear_Ryk', 'Ryk', 'Osric_Umber', 'Ronnal_Baratheon', "Archon's_Daughter_(Jaehaerys_I)", 'Alarra_Stark', 'Jeyne_Westerling_(Wife_of_Maegor_I)', 'Jon_Piper']
"""

# cette fonction pour supprimer les doublons des personnage [Aegon_the_Conqueror', Aegon_I_Targaryen'] = >[ 'Aegon_I_Targaryen']
       
def doublons():
 filtered_urls =[]
 for key in l:
         url = "https://iceandfire.fandom.com/wiki/"+key
         # Récupération de l'en-tête de la réponse HTTP
         response = requests.head(url, allow_redirects=True)

        # Comparaison de l'URL de la réponse avec l'URL d'origine
         if response.url == url:
             filtered_urls.append(key)
 return filtered_urls            
#l1final=doublons()
#print(l1final)



 ## Affichage apres la fonction doublon:
ll=['Petyr_Baelish', 'Robert_I_Baratheon', 'Janos_Slynt', 'Edmure_Tully', 'Tyrion_Lannister', 'Lysa_Arryn', 'Hoster_Tully', 'Catelyn_Stark', 'Brandon_Stark', 'Eddard_Stark', 'Jon_Arryn', 'Sansa_Stark', 'Daenerys_I_Targaryen', 'Barra', 'Jaime_Lannister', 'Joffrey_I_Baratheon', 'Tommen_I_Baratheon', 'Myrcella_Baratheon', 'Stannis_Baratheon', 'Shella_Whent', 'Harren_Hoare', 'Daemon_Targaryen', 'Daemon_Blackfyre', 'Minisa_Tully', 'Tywin_Lannister', 'Arya_Stark', 'Gregor_Clegane', 'Cersei_Lannister', 'Aegon_I_Targaryen', 'Orys_Baratheon', 'Mern_IX_Gardener', 'Renly_Baratheon', 'Mace_Tyrell', 'Harwyn_Hoare', 'Lyanna_Stark', 'Rhaegar_Targaryen', 'Rickard_Stark', 'Aerys_II_Targaryen', 'Robb_Stark', 'Robert_Arryn', 'Vardis_Egen', 'Bronn', 'Gyles_Rosby', 'Harys_Swyft', 'Steffon_Baratheon', 'Edric_Storm', 'Mya_Stone', 'Gendry', 'Rhaelle_Targaryen', 'Theon_Greyjoy', 'Jon_Snow', 'Barristan_Selmy', 'Sandor_Clegane', 'Drogo', 'Harrold_Hardyng', 'Aemma_Arryn', 'Viserys_I_Targaryen', 'Rhaenyra_Targaryen', 'Nymeria', 'Aegor_Rivers', 'Maelys_Blackfyre', 'Illyrio_Mopatis', 'Morros_Slynt', 'Danos_Slynt', 'Samwell_Tarly', 'Emmon_Frey', 'Marq_Piper', 'Clement_Piper', 'Kevan_Lannister', 'Tytos_Blackwood', 'Roose_Bolton', 'Helman_Tallhart', 'Walder_Frey', 'Brynden_Tully', 'Ryman_Frey', 'Jeyne_Westerling', 'Joanna_Lannister', 'Benjen_Stark', 'Olenna_Tyrell', 'Marillion', 'Arianne_Martell', 'Doran_Martell', 'Viserys_III_Targaryen', 'Jon_Connington', 'Utherydes_Wayn', 'Desmond_Grell', 'Jonos_Bracken', 'Karyl_Vance', 'Jason_Mallister', 'Lothar_Frey', 'Bran_Stark', 'Rickon_Stark', 'Loras_Tyrell', 'Lyarra_Stark', 'Barbrey_Dustin', 'Aenys_I_Targaryen', 'Maegor_I_Targaryen', 'Jaehaerys_I_Targaryen', 'Aegon_II_Targaryen', 'Aegon_III_Targaryen', 'Daeron_I_Targaryen', 'Baelor_I_Targaryen', 'Viserys_II_Targaryen', 'Aegon_IV_Targaryen', 'Daeron_II_Targaryen', 'Aerys_I_Targaryen', 'Maekar_I_Targaryen', 'Aegon_V_Targaryen', 'Jaehaerys_II_Targaryen', 'Haegon_Blackfyre', 'Jorah_Mormont', 'Visenya_Targaryen', 'Brynden_Rivers', 'Randyll_Tarly', 'Lyn_Corbray', 'Jeor_Mormont', 'Harras_Harlaw', 'Dunstan_Drumm', 'Ashara_Dayne', 'Jory_Cassel', 'Raymun_Darry', 'Jeyne_Poole', 'Beth_Cassel', 'Robar_Royce', 'Hizdahr_zo_Loraq', 'Rhaella_Targaryen', 'Rhaego', 'Paxter_Redwyne', 'Drogon', 'Brienne_Tarth', 'Oberyn_Martell', 'Arthur_Dayne', 'Oswell_Whent', 'Roland_Crakehall', 'Bryce_Caron', 'Andar_Royce', 'Eddard_Karstark', 'Torrhen_Karstark', 'Margaery_Tyrell', 'Trystane_Martell', 'Selyse_Florent', 'Shireen_Baratheon', 'Victarion_Greyjoy', 'Davos_Seaworth', 'Garlan_Tyrell', 'Alester_Florent', 'Axell_Florent', 'Ramsay_Bolton', 'Asha_Greyjoy', 'Alys_Karstark', 'Arrec_Durrandon', 'Harrag_Hoare', 'Ravos_Hoare', 'Harmund_II_Hoare', 'Harmund_III_Hoare', 'Hagon_Hoare', 'Qhorwyn_Hoare', 'Harlan_Hoare', 'Halleck_Hoare', 'Osmund_Strong', 'Lucamore_Strong', 'Lyonel_Strong', 'Harwin_Strong', 'Larys_Strong', 'Simon_Strong', 'Kermit_Tully', 'Cregan_Stark', 'Walter_Whent', 'Willis_Wode', 'Aenar_Targaryen', 'Rhaena_Targaryen', 'Elaena_Targaryen', 'Myriah_Martell', 'Shiera_Seastar', 'Aegon_Blackfyre', 'Aemon_Blackfyre', 'Daenerys_Martell', 'Artos_Stark', 'Damon_Lannister_(lord)', 'Aerion_Targaryen', 'Dalton_Greyjoy', 'Quentyn_Ball', 'Tybolt_Lannister', 'Roger_Reyne', 'Ellyn_Reyne', 'Tytos_Lannister', 'Cerenna_Lannister', 'Damion_Lannister', 'Daven_Lannister', 'Janei_Lannister', 'Lucion_Lannister', 'Martyn_Lannister', 'Myrielle_Lannister', 'Stafford_Lannister', 'Rickard_Karstark', 'Tyrek_Lannister', 'Tygett_Lannister', 'Joy_Hill', 'Gerold_Lannister', 'Aerion_Targaryen_(son_of_Daemion)', 'Valaena_Velaryon',
 'Benjicot_Blackwood', 'Alicent_Hightower', 'Aemond_Targaryen', 'Alyssa_Targaryen', 'Rhea_Royce', 'Laena_Velaryon', 'Visenya_Targaryen_(daughter_of_Rhaenyra)', 'Rhaena_Targaryen_(daughter_of_Laena_Velaryon)', 'Baela_Targaryen', 'Larra_Rogare', 'Naerys_Targaryen', 'Alysanne_(daughter_of_Aegon_IV)', 'Lily', 'Willow_(daughter_of_Aegon_IV)', 'Rosey_(daughter_of_Aegon_IV)', 'Bellanora_Otherys', 'Narha_Otherys', 'Balerion_Otherys', 'Mya_Rivers', 'Gwenys_Rivers', 'Falena_Stokeworth', 'Bellegere_Otherys', 'Calla_Blackfyre', 'Rhaegel_Targaryen', 'Baelor_Targaryen_(son_of_Daeron_II)', 'Dyanna_Dayne', 'Daella_Targaryen_(daughter_of_Maekar_I)', 'Rhae_Targaryen', 'Imry_Florent', 'Jeyne_Marbrand', 'Genna_Lannister', 'Cleos_Frey', 'Denyo_Terys', 'Ternesio_Terys', 'Yorko_Terys', 'Kindly_Man', 'Waif', 'Clegane_(Father_of_Gregor_and_Sandor)', 'Balon_Swann', 'Aurane_Waters', 'Gilly', 'Dareon', 'Podrick_Payne', 'Aeron_Greyjoy', 'Quentyn_Martell', 'Durran', 'Elinor_Tyrell', 'Garth_Tyrell', 'Janna_Tyrell', 'Medwick_Tyrell', 'Megga_Tyrell', 'Mina_Tyrell', 'Olene_Tyrell', 'Olymer_Tyrell', 'Raymund_Tyrell', 'Rickard_Tyrell', 'Theodore_Tyrell', 'Victaria_Tyrell', 'Willas_Tyrell', 'Luthor_Tyrell', 'Quentin_Tyrell', 'Victor_Tyrell', 'Tommen_Tully', 'Agnes_Blackwood', 'Grover_Tully', 'Elmo_Tully', 'Lyonel_Baratheon', 'Argella_Durrandon', 'Ormund_Baratheon', 'Argilac_Durrandon', 'Ronnel_Arryn_(king)', 'Daenys_Targaryen', 'Edwell_Celtigar', 'Valarr_Targaryen', 'Wyl_of_Wyl', 'Walter_Wyl', 'Rogar_Baratheon', 'Brella', 'Alerie_Hightower', 'Benedict_I_Justman', 'Benedict_II_Justman', 'Bernarr_II_Justman', 'Roderick_Blackwood', 'Garth_Greenhand', 'Yohn_Royce', 'Harrion_Karstark', 'Quincy_Cox', 'Lyle_Crakehall', 'Hoster_Blackwood', 'Lucas_Blackwood', 'Walder_Frey_(Black)', 'Harry_Rivers', 'Rolph_Spicer', 'Sybell_Spicer', 'Dacey_Mormont', 'Raynald_Westerling', 'Jon_Umber_(Greatjon)', 'Patrek_Mallister', 'Danwell_Frey', 'Hosteen_Frey', 'Leslyn_Haigh', 'Whalen_Frey', 'Raymund_Frey', 'Walder_Rivers', 'Garse_Goodbrook', 'Benfrey_Frey', 'Ellaria_Sand', 'Qarlton_II_Durrandon', 'Shiera_Blackwood', 'Laenor_Velaryon', 'Alysanne_Blackwood', 'Melissa_Blackwood', 'Robert_Blackwood', 'Brynden_Blackwood', 'Edmund_Blackwood', 'Alyn_Blackwood', 'Bethany_Blackwood', 'Melantha_Blackwood', 'Edwyle_Stark', 'Jocelyn_Stark', 'Elys_Waynwood', 'Barbara_Bracken', 'Jayne_Bracken', 'Catelyn_Bracken', 'Bess_Bracken', 'Alysanne_Bracken', 'Balon_IX_Greyjoy', 'Addam_Velaryon', 'Shaena_Targaryen', 'Daeron_Targaryen_(son_of_Aerys_II)', 'Aegon_Targaryen_(son_of_Aerys_II)', 'Aegon_Targaryen_(son_of_Rhaegar)', 'Marna_Locke', 'Arya_Flint', 'Jaehaerys_Targaryen_(son_of_Aerys_II)', 'Denys_Darklyn', 'Meera_Reed', 'Ygritte', 'Maron_Greyjoy', 'Maege_Mormont', 'Stevron_Frey', 'Gawen_Westerling', 'Tytos_Brax', 'Willem_Lannister', 'Tion_Frey', 'Mathis_Rowan', 'Edwyn_Frey', 'Osmund_Kettleblack', 'Tanda_Stokeworth', 'Tyrion_Tanner', 'Falyse_Stokeworth', 'Balman_Byrch', 'Dorna_Swyft', 'Steffon_Swyft', 'Shierle_Swyft', 'John_the_Oak', 'Glendon_Flowers', 'Creighton_Longbough', 'Delena_Florent', 'Mychel_Redfort', 'Gregor_Goode', 'Griffith_Goode', 'Robin_Darklyn', 'Humfrey', 'Erryk_Cargyll', 'Arryk_Cargyll', 'Rickard_Thorne', 'Mervyn_Flowers', 'Alyn_Connington', 'Tom_Costayne', 'Harwin', 'Daeron_Targaryen_(son_of_Aegon_V)', 'Jorah_Mormont#Jorah_Mormont', 'Matarys_Targaryen', 'Maegon_Targaryen', 'Gaemon_Targaryen_(son_of_Aenar)', 'Aegon_Targaryen_(son_of_Gaemon)', 'Elaena_Targaryen_(daughter_of_Gaemon)', 'Aelyx_Targaryen', 'Baelon_Targaryen_(son_of_Aerys)', 'Daemion_Targaryen', 'Ceryse_Hightower', 'Aegon_Targaryen_(son_of_Jaehaerys_I)',
 'Valerion_Targaryen', 'Vaegon_Targaryen', 'Maegelle_Targaryen', 'Viserra_Targaryen', 'Gael_Targaryen', 'Daella_Targaryen_(daughter_of_Jaehaerys_I)', 'Baelon_Targaryen_(son_of_Viserys_I)', 'Daenaera_Velaryon', 'Jon_Waters', 'Jeyne_Waters', 'Daenora_Targaryen', 'Maegor_Targaryen_(son_of_Aerion)', 'Quellon_Greyjoy', 'Urrigon_Greyjoy', 'Lyman_Darry', 'Amerei_Frey', 'Mariya_Darry', 'Lyonel_Selmy', 'Bharbo', 'Arwood_Frey', 'Donnel_Haigh', 'Harys_Haigh', 'Tywin_Frey', 'Jeyne_Darry', 'Willem_Frey', 'Lyonel_Frey', 'Melesa_Crakehall', 'Walder_Frey_(son_of_Emmon)', 'Joyeuse_Erenford', 'Kyra_Frey', 'Walder_Goodbrook', 'Jeyne_Goodbrook', 'Dickon_Tarly', 'Lewys_Piper', 'Aegon_Targaryen_(Son_of_Aenys_I)', 'Lythene_Frey', 'Jonos_Arryn', 'Roland_I_Arryn', 'Anya_Waynwood', 'Humfrey_Beesbury', 'Deana_Hardyng', 'Walton_Frey', 'Steffon_Frey', 'Walda_Frey_(daughter_of_Walton)', 'Bryan_Frey', 'Horton_Redfort', 'Jon_Redfort', 'Ysilla_Royce', 'Perra_Royce', 'Jennis_Templeton', 'Geremy_Frey', 'Gaemon_Targaryen_(son_of_Jaehaerys_I)', 'Annara_Farring', 'Rennifer_Longwaters', 'Josua_Massey', 'Alarra_Massey', 'Aethan_Velaryon', 'Samantha_Stokeworth', 'Androw_Farman', 'Jon_Cafferen', 'Alys_Oakheart', 'Allyria_Dayne', 'Rhaenys_Targaryen_(daughter_of_Aerion)', 'Beron_Stark', 'Veron_Greyjoy', 'Harlon_Greyjoy', 'Quenton_Greyjoy', 'Donel_Greyjoy', 'Robin_Greyjoy', 'Tommen_Costayne', 'Sawane_Botley', 'Germund_Botley', 'Sigorn', 'Eddison_Tollett', 'Garth_the_Gardener', 'Mellario_of_Norvos', 'Nymeria_Sand', 'Davos_Dayne', 'Lyanna_Mormont', 'Jon_Stark', 'Rickard_Stark_(king)', 'Addam_Marbrand', 'Melessa_Florent', 'Talla_Tarly', 'Hobber_Redwyne', 'Horas_Redwyne', 'Aemon_Targaryen_(Son_of_Maekar_I)', 'Jack_Bulwer', 'Aenys_Frey', 'Jared_Frey', 'Luceon_Frey', 'Symond_Frey', 'Jammos_Frey', 'Morya_Frey', 'Tyta_Frey', 'Perwyn_Frey', 'Willamen_Frey', 'Olyvar_Frey', 'Arwyn_Frey', 'Wendel_Frey', 'Colmar_Frey', 'Waltyr_Frey', 'Waltyr_Frey', 'Elmar_Frey', 'Shirei_Frey', 'Bethany_Rosby', 'Benfred_Tallhart', 'Eddara_Tallhart', 'Galbart_Glover', 'Robett_Glover', 'Leobald_Tallhart', 'Cyrenna_Swann', 'Amarei_Crakehall', 'Alyssa_Blackwood', 'Sarya_Whent', 'Perriane_Frey', 'Donnel_Waynwood', 'Aegon_Frey', 'Petyr_Frey', 'Eleyna_Westerling', 'Rollam_Westerling', 'Jason_Lannister_(son_of_Gerold)', 'Marla_Prester', 'Damon_Lannister_(son_of_Jason)', 'Lynora_Hill', 'Erryk', 'Arryk', 'Gilbert_of_the_Vines', 'Robin_Ryger', 'Three-Eyed_Crow', 'Jon_Heddle', 'Branda_Stark', 'Donella_Hornwood', 'Herndon_of_the_Horn', 'Harlon_the_Hunter', 'Lyonel_Corbray', 'Lucas_Corbray', 'Rodrik_Harlaw', 'Erich_V_Harlaw', 'Harron_Harlaw', 'Gorold_Goodbrother', 'Gwynesse_Harlaw', 'Illifer', 'Rufus_Leek', 'Denys_Drumm', 'Donnel_Drumm', 'Martyn_Cassel', 'Hallyne', 'Vayon_Poole', 'Martyn_Rivers', 'Desmera_Redwyne', 'Walda_Frey_(daughter_of_Merrett)', 'Walder_Frey_(son_of_Merrett)', 'Burton_Crakehall', 'Tybolt_Crakehall', 'Merlon_Crakehall', 'Bryen_Caron', 'Hullen', 'Old_Nan', 'Ryam_Florent', 'Erren_Florent', 'Steffarion_Sparr', 'Wex_Pyke', 'Alekyne_Florent', 'Leonette_Fossoway', 'Colin_Florent', 'Rylene_Florent', 'Melara_Crane', 'Rhea_Florent', 'Clydas', 'Mully', 'Cregan_Karstark', 'Euron_III_Greyjoy', 'Rohanne_Webber', 'Wylis_Manderly', 'Halys_Hornwood', 'Dormund', 'Daryn_Hornwood', 'Beren_Tallhart', 'Larence_Snow', 'Berena_Hornwood', 'Medger_Cerwyn', 'Robard_Cerwyn', 'Aregelle_Stark', 'Brandon_Tallhart', 'Lelia_Lannister', 'Urras_Greyiron', 'Erich_I_Greyiron', 'Urragon_III_Greyiron', 'Torgon_Greyiron', 'Urragon_IV_Greyiron', 'Tristifer_Botley', 'Sargon_Botley', 'Harren_Botley', 'Symond_Botley', 'Harlon_Botley', 'Vickon_Botley', 'Bennarion_Botley', 
 'Balon_Botley', 'Quellon_Botley', 'Lucimore_Botley', 'The_Sparr', 'Alys_Rivers', 'Aemon_Targaryen_(Son_of_Jaehaerys_I)', 'Oscar_Tully', 'Sabitha_Frey', 'Rickon_Stark_(Son_of_Benjen)', 'Gilliane_Glover', 'Sara_Snow', 'Arra_Norrey', 'Lynara_Stark', 'Rickon_Stark_(Son_of_Cregan)', 'Sarra_Stark', 'Alys_Stark', 'Raya_Stark', 'Mariah_Stark', 'Jonnel_Stark', 'Edric_Stark_(Son_of_Cregan)', 'Lyanna_Stark_(Daughter_of_Cregan)', 'Barthogan_Stark', 'Brandon_Stark_(Son_of_Cregan)', 'Bennard_Stark', 'Jeyne_Manderly', 'Serena_Stark', 'Alleras', 'Gerrick_Kingsblood', 'Lorra_Royce', 'Donnor_Stark', 'Manfred_Dondarrion', 'Jason_Lannister', 'Walderan_Tarbeck', 'Ella_Lannister', 'Cerelle_Lannister', 'Cerissa_Lannister', 'Teora_Kyndall', 'Androw_Ashford', 'Robert_Reyne', 'Reynard_Reyne', 'Tion_Lannister', 'Rohanne_Tarbeck', 'Cyrelle_Tarbeck', 'Tion_Tarbeck', 'Tywald_Lannister', 'Last_Lord_Tarbeck', 'Andros_Brax', 'Flement_Brax', 'Rupert_Brax', 'Robert_Brax', 'Robert_Brax_(son_of_Flement)', 'Walder_Brax', 'Jon_Brax', 'Shiera_Crakehall', 'Sebaston_Farman', 'Marq_Farman', 'Franklyn_Farman', 'Lysa_Farman', 'Jeyne_Farman', 'Gareth_Clifton', 'Alysanne_Farman', 'Antario_Jast', 'Lanna_Lannister', 'Leonella_Lefford', 'Myranda_Lefford', 'Damon_Marbrand', 'Melwyn_Sarsfield', 'Selmond_Stackspear', 'Alys_Stackspear', 'Alyn_Stackspear', 'Joanna_Swyft', 'Alyn_Tarbeck', 'Johanna_Westerling', 'Titus_Peake', 'Florys_the_Fox', 'Margot_Lannister', 'Moro', 'Haggo', 'Qotho', 'Rhogoro', 'Tomard', 'Lorent_Caswell', 'Orbert_Caswell', 'Armond_Caswell', 'Taena_Merryweather', 'Rowan_Gold-Tree', 'Hosman_Norcross', 'Alester_Norcross', 'Renly_Norcross', 'Norbert_Vance', 'Tyana_Wylde', 'Morgan_Wylde', 'Coryanne_Wylde', 'Howard_Bullock', 'Samwell_Blackwood', 'Loren_I_Lannister', 'Aegon_Targaryen_(Son_of_Baelon)', 'Donnel_Hightower', 'Cletus_Yronwood', 'Margaret_Karstark', 'Alyn_Marbrand', 'Gylbert_Farwynd', 'Hibald', 'Naggle', 'Hal_(Hairy)', 'Kedge', 'Lew', "High_Septon_(Tyrion's)", 'Lambert_Turnberry', 'Alyce_Graceford', 'Duskendale_Captain', "Captain's_Sister", 'Durran_II_Durrandon', 'Omer_Florent', 'Merrell_Florent', 'Rycherd_Crane', 'Lysa_Meadows', 'Rose_of_Red_Lake', 'Alysanne_Bulwer', 'Bors_the_Breaker', 'Osbert_Serry', 'Talbert_Serry', 'Lia_Serry', 'Owen_Oakenshield', 'Luthor_Tyrell_(son_of_Moryn)', 'Elyn_Norridge', 'Leo_Blackbar', 'Luthor_Tyrell_(son_of_Theodore)', 'Leo_Tyrell_(son_of_Victor)', 'Jon_Bulwer', 'Robert_Ashford', 'Prunella_Celtigar', 'Prudence_Celtigar', 'Cayn', 'Gage', 'Albar_Royce', 'Maris_the_Maid', 'Foss_the_Archer', 'Ellyn_Ever_Sweet', 'Brandon_of_the_Bloody_Blade', 'Uthor_of_the_High_Tower', 'Prentys_Tully', 'Rhaegar_Frey', 'Hoarfrost_Umber', 'Ronel_Rivers', 'Wynafrei_Whent', 'Bellena_Hawick', 'Ryella_Frey', 'Androw_Frey', 'Alyn_Frey', 'Hostella_Frey', 'Alyn_Haigh', 'Sylwa_Paege', 'Hoster_Frey', 'Merianne_Frey', 'Roslin_Tully', 'Harmen_Uller', 'Amos_Bracken', 'Jasper_Waynwood', 'Renfred_Rykker', 'Gawen_Glover', 'Erena_Glover', 'Torghen_Flint', 'Donnel_Flint', 'Artos_Flint', 'Marsella_Waynwood', 'Penny_Jenny', 'Walton_Stark_(Son_of_Brandon)', 'Aerys_Targaryen_(son_of_Aegon)', 'Daenerys_Targaryen_(daughter_of_Jaehaerys_I)', 'Elys_Arryn', 'Ryella_Royce', 'Viserys_Targaryen_(Son_of_Aenys_I)', 'Lyman_Lannister', 'Guncer_Sunglass', 'Alayne_Royce', 'Jocasta_Lannister', 'Tyler_Hill', 'Merrell_Bullock', 'Cassella_Staunton', 'Jonah_Mooton', 'Braxton_Beesbury', 'Perianne_Moore', 'Dunstan_Pryor', 'Alys_Karstark_(Wife_of_Brandon)', 'Lonnel_Snow', 'Rodwell_Stark', 'Arsa_Stark', 'Ygon_Farwynd', 'Harmund_Sharp', 'Deziel_Dalt', 'Emmett', 'Andrey_Dalt', 'Aegon_Frey_(son_of_Aenys)', 'Wynafryd_Manderly', 
 'Wylla_Manderly', 'Sallei_Paege', 'Walder_Frey_(son_of_Jammos)', 'Dickon_Frey', 'Mathis_Frey', 'Hubard_Rambton', 'Jeyne_Beesbury', 'Robert_Frey_(son_of_Rhaegar)', 'Walda_Frey_(daughter_of_Rhaegar)', 'Jonos_Frey', 'Walder_Haigh', 'Tysane_Frey', 'Walda_Frey_(daughter_of_Lothar)', 'Emberlei_Frey', 'Meha', 'Bump', 'Harrold_Rogers', 'Leona_Woolfield', 'Torwynd', 'Munda', 'Dryn', 'Wylla_Fenn', 'Cregard_Stark', 'Torrhen_Stark_(Son_of_Edric)', 'Arrana_Stark', 'Varamyr', 'Benjen_Stark_(Lord)', 'Lysa_Locke', 'Sansa_Stark_(Daughter_of_Rickon)', 'Robyn_Ryswell', 'Benjen_Stark_(Son_of_Bennard)', 'Brandon_Stark_(Son_of_Bennard)', 'Elric_Stark', 'Jon_Umber_(Husband_of_Serena)', "Gerrick_Kingsblood's_Youngest_Daughter", 'Leana_Frey', 'Steffon_Stackspear', 'Surly_lad', 'Borys_Baratheon', 'Alyn_Bullock', 'Raylon_Rivers', 'Orryn_Baratheon', 'Norman_Hightower', 'Leo_Tyrell_(son_of_Moryn)', 'Alys_Beesbury', 'Uther_Peake', 'Black_Maris', 'Peremore_Hightower', 'Lucinda_Tully', 'Ella_Broome', 'Humfrey_Bracken', 'Brandon_Stark_(Father_of_Walton)', 'Alaric_Stark', 'Lord_Tarbeck_(Son_of_Alyn)', 'Lord_Sunglass', 'Melony_Piper', 'Lord_Staunton_(Father_of_Cassella)', 'Myriame_Manderly', 'Missandei', 'Ryk', 'Osric_Umber', 'Ronnal_Baratheon', "Archon's_Daughter_(Jaehaerys_I)", 'Alarra_Stark', 'Jeyne_Westerling_(Wife_of_Maegor_I)', 'Jon_Piper']



#on met au point un dictionnaire pour sauvegarder les relations entre les personnages de la saga
dictRelation={} #personnage-->(fraterie[],parent[],enfant[],Amour[])

#cette fonction parcours la liste des personnages et sauvegarde dans le dictionnaire des relation le type de relation entre
#les personnages

def Relation():
   with open('C:/Users/Lenovo/Desktop/relationp.txt', 'w') as f:
        for p in ll:
            personnages_siblings=[]
            personnages_father=[]
            personnages_spouse=[]
            personnages_children=[]
            url="https://iceandfire.fandom.com/wiki/"+p
            
            response=requests.get(url)
            soup=BeautifulSoup(response.text,"html.parser")
            ##recuperation des liens de la classe father
            try:
                 div_father = soup.find('div', {'data-source': 'father'})
                 links = div_father.find_all('a')

                 for link in links:
                    personnages_father.append(link.get('href')[6:])
            except AttributeError: 
                pass
            
            ##recuperation des liens de la classe mother
            try:
                 div_father = soup.find('div', {'data-source': 'mother'})
                 links = div_father.find_all('a')

                 for link in links:
                    personnages_father.append(link.get('href')[6:])
            except AttributeError: 
                pass


            ##recuperation des liens de la classe siblings    
            try:
                div_siblings = soup.find('div', {'data-source': 'siblings'})
                links = div_siblings.find_all('a')

                for link in links:
                    personnages_siblings.append(link.get('href')[6:])
            except AttributeError: 
                pass        

            ##recuperation des liens de la classe spouse    
            try:
                div_spouse = soup.find('div', {'data-source': 'spouse'})
                links = div_spouse.find_all('a')

                for link in links:
                    personnages_spouse.append(link.get('href')[6:])
            except AttributeError:
               pass 

             ##recuperation des liens de la classe children    
            try:
                div_children = soup.find('div', {'data-source': 'children'})
                links = div_children.find_all('a')

                for link in links:
                    personnages_children.append(link.get('href')[6:]) 
            except AttributeError:
                pass          

            dictRelation[p]=[personnages_siblings,personnages_father,personnages_children,personnages_spouse]

            # écrire dans le fichier
            f.write(str(dictRelation[p])+'\n')

            ##print(dictRelation[p])

        return dictRelation
#test 8
#Relation()
 
 #Cette fonction parcours le dictionnaire des relations pour trouver les noms communs entre famille et amour et 
 # renvoie les couples incestieux de la saga
 

def check_common_names(d):
    # parcourir chaque entrée du dictionnaire
    for name, lists in d.items():
        # créer une liste vide pour stocker les noms communs
        common_names = []
        # parcourir les trois premières listes
        for l in lists[:-1]:
            # ajouter chaque nom présent dans la liste courante
            # s'il n'est pas déjà dans la liste des noms communs
            for n in l:
                if n not in common_names:
                    common_names.append(n)
        # parcourir la dernière liste
        for n in lists[-1]:
            # si le nom courant est dans la liste des noms communs,
            # afficher un message indiquant qu'il y a un nom en commun
            if n in common_names:
                print(f"{name} est dans un couple incestueux avec : {n}")



 
#heck_common_names(dictRelation)  
#liste des couples incestueux de la saga Game of thrones

#Aegon_I_Targaryen est dans un couple incestueux avec : Visenya_Targaryen
#Aegon_I_Targaryen est dans un couple incestueux avec : Rhaenys_Targaryen
#Aerys_II_Targaryen est dans un couple incestueux avec : Rhaella_Targaryen
#Jaehaerys_I_Targaryen est dans un couple incestueux avec : Alysanne_Targaryen
#Aegon_II_Targaryen est dans un couple incestueux avec : Helaena_Targaryen
#Baelor_I_Targaryen est dans un couple incestueux avec : Daena_Targaryen
#Aegon_IV_Targaryen est dans un couple incestueux avec : Naerys_Targaryen
#Visenya_Targaryen est dans un couple incestueux avec : Aegon_I_Targaryen
#Rhaella_Targaryen est dans un couple incestueux avec : Aerys_II_Targaryen
#Naerys_Targaryen est dans un couple incestueux avec : Aegon_IV_Targaryen



#svg_dico(mon_dictionnaire, 'C:/Users/Lenovo/Desktop/couples.txt');
 
     
 

    

    