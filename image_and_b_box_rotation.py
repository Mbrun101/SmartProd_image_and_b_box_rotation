# image_and_b_box_rotation.py
# Michael Brunner, 3.12.2019

# import the Python Image processing Library
# import the Python Math Libary
# import the Python os Libary

from PIL import Image
import math
import os

# get pathnames from the User where the files are stored an where they have to be stored after processing.
source_path = input("Absoluter Pfad des Ordners angeben in dem die gelabelten Fotos inkl. Text-Files liegen:")
target_path = input("Absoluter Pfad des Ordners angeben in welchem der Output gespeichert werden soll:" )
drehrwinkel = int(input("Drehwinkel in Grad angeben: "))

# set rotation for hardcoding angles.
#drehrwinkel = 45

# calculate the numbers of iteration it needs to complet the task. 
itterationen = int((360 / drehrwinkel)) #!!!Runden!!!
print(itterationen)
it_zaehler = 1

# ----Umschalten bei Pfadangabe-----
# switch to first option when the code gets executed in the same directory where the code is stored. If you want to open the open the files from a other directory switch to second option.
#all_txt_files = [x for x in os.listdir() if x.endswith(".txt")] #öffnet die Dateien die in im selben Ordner liegen wie der Code und dort aufgerufen wird.
all_txt_files = [x for x in os.listdir(source_path) if x.endswith(".txt")] #öffnen von Dateien in beim Aufruf angegebene Pfad

#print(all_txt_files)
list_length = (len(all_txt_files))
#print(list_length)

# initializing end Suffix 
end_letter = 'rot.txt'
  
# printing original list 
#print("The original list : " + str(all_txt_files)) 
  
# using list comprehension + endwith() 
# Segregating by Suffix 
with_end_letter = [x for x in all_txt_files if x.endswith(end_letter)] 
without_end_letter = [x for x in all_txt_files if x not in with_end_letter] 
  
# print results
#print("The list without suffix rot.txt : " + str(without_end_letter)) 
#print("The list with suffix rot.txt : " + str(with_end_letter)) 

with_list_lenth = (len(with_end_letter))
without_list_lenth = (len(without_end_letter))

#print("List lenth without Sufix: '%s': %s" % (end_letter, without_list_lenth))
#print("List lenth with Sufix: '%s': %s" % (end_letter, with_list_lenth))

# iterate over every Element which was never rotatet before.
for i in range(without_list_lenth):
    # set the variable "temp" which is needed to read the right .txt-file form the Array
    temp = without_end_letter[(without_list_lenth - i -1)]
    #print("i of without_list_lenth %s:" % i)
    #print("without_list_lenth - i: %s" % (without_list_lenth - i))
    #print("temp: %s" % temp)
    # strip the suffix ".txt" from the filename, is later used to create the new name of the rotatet file.
    temp_stript = temp.rstrip(".txt")
    #print("temp after rstrip: %s" % temp_stript)
    #!abfrageelement könnte ev. noch verbessert werden um Effizenz zu steigern!
    abfrage_element = "%s_%srot" % (temp_stript, drehrwinkel) #Format gedrehter Elente: (%s_%srot.txt" % (without_end_letter[i], rot), "x")
    #print("abfrage_element: %s" % abfrage_element)
    #print("abfrage_element not in List with_end_letter: %s" % abfrage_element not in with_end_letter)
    
    if abfrage_element not in with_end_letter:
        print("Fotobearbeitung durchführen")
        
        try:
            # .txt-File mit bounding Boxen auslesen und in String speichern, ausplitten und als Array speichern.
            # .txt-files with bounding boxes open, read, convert to string, split and safe as Arrays. If there is an error it will brake an print: "Fehler in 1.Try-Schlaufe"
            
            #----Umschalten bei Pfadangabe-----
            #switch to first option when the code gets executed in the same directory where the code is stored. If you want to open the open the files from a other directory switch to second option.
            #text_file = open("./%s.txt" % temp_stript)
            text_file = open("%s/%s.txt" % (source_path, temp_stript)) #öffnen von Dateien in beim Aufruf angegebene Pfad
            #print("text-file erfolgreich geöffnet")
            
            # länge des txt-files auslesen (anzahl Elemente -> num_of_list)
            num_of_lines = sum(1 for line in text_file)
            #print("Anzahl Zeilen im txt-file: %s" % num_of_lines)
            text_file.close()

            #text-file erneut öffnen, dammit der Coursor zum lesen wieder am Anfang der Elemente steht.
            #----Umschalten bei Pfadangabe-----
            #switch to first option when the code gets executed in the same directory where the code is stored. If you want to open the open the files from a other directory switch to second option.
            #text_file = open("./%s.txt" % temp_stript)
            text_file = open("%s/%s.txt" % (source_path, temp_stript)) #öffnen von Dateien in beim Aufruf angegebene Pfad

            #Variable zum while-schlaufen zählen auf 0 setzen, damit die das auslesen des txt-files am Anfang beginnt
            line_num = 0
            
            # while-loop is needed if there are more than one object lablet on the image (.txt-file contains per line one object)
            while line_num < num_of_lines:
                print("Einritt while-Schleife gelungen")
                text_original = text_file.readline().rstrip("\n")
                text = text_original.split(" ")
                #print("Inhalt Text-file ohne split: %s" % text_original)
                #text = text_original[line_num].split(" ")
                print("Line number %s: %s" % (line_num, text))
                #print("Inhalt Variable text:", text)
                

                # Die einzelen Arryteile den entsprechenden Variablen zuordnen
                # define the varables with, in the file given informations.
                obj_class = text[0]
                obj_center_rel_x = float(text[1])
                obj_center_rel_y = float(text[2])
                w_rel = float(text[3])
                h_rel = float(text[4])
                #print("obj_center_rel_x: %s, text[1]: %s" %(obj_center_rel_x, text[1]))
                #print("obj_center_rel_y: %s, text[2]: %s" %(obj_center_rel_y, text[2]))
                #print("w_rel: %s, text[3]: %s" %(w_rel, text[3]))
                #print("h_rel: %s, text[4]: %s" %(h_rel, text[4]))

                
                # Create an Image object, open the image with the same filname as the .txt-file
                #----Umschalten bei Pfadangabe-----
                #switch to first option when the code gets executed in the same directory where the code is stored. If you want to open the open the files from a other directory switch to second option.
                #colorImage  = Image.open("./%s.jpg" % temp_stript)
                colorImage  = Image.open("%s/%s.jpg" % (source_path, temp_stript)) #öffnen von Dateien in beim Aufruf angegebene Pfad
                
                #colorImage.show()
                

                # Befehl center=(x, y), x und y sind die Pilxel um weches gedreht
                # wird, gerechnten von oben links im Bild
                # get the dimensions of the image in pixels.
                width, height = colorImage.size

                print("Foto width:", width, "Pixels")
                print("Foto hight:", height, "Pixels")

                # calculate the centerpixel of the image where the rotation has to rotate on.
                obj_center_x_pixel = int(width * obj_center_rel_x)
                obj_center_y_pixel = int(height * obj_center_rel_y)
                
                print("Objekt Center Pixel x:", obj_center_x_pixel)
                print("Objekt Center Pixel y:", obj_center_y_pixel)
                
                # set iteration counter of the rotationsteps to 1 
                it_zaehler = 1
            
                while it_zaehler < (itterationen):

                    w_trans_rel = 0.0
                    h_trans_rel = 0.0

                    print("2. while schlaufe leuft")

                    rot = (drehrwinkel * it_zaehler)

                    print("rot = %s" % rot)
                    
                    # b-Box drehen und neue angepasste b-Box berechnen und in neues .txt File schreiben.
                    # rotate bounding box an calculate the new bounding box where the rotatet box fits in.

                    if rot == 90 or rot == 270:
                        w_trans_rel = (h_rel * height / width)
                        h_trans_rel = (w_rel * width / height)
                        
                    elif rot == 180:
                        w_trans_rel = w_rel
        
                        h_trans_rel = h_rel

                    else:
                        rad_rot = math.radians(rot)
                        #print("rad_rot = %s" % rad_rot)
                        w_trans_rel = ((abs(math.cos(rad_rot) * w_rel) * width) + (abs(math.sin(rad_rot) * h_rel) * height)) / width
                        h_trans_rel = ((abs(math.sin(rad_rot) * w_rel) * width) + (abs(math.cos(rad_rot) * h_rel) * height)) / height

                    w_trans_rel = round(w_trans_rel, 6)
                    h_trans_rel = round(h_trans_rel, 6)
                    
                    # try to safe the calculatet bounding box to a new .txt-file, if this file already exists, it occures an error and a messges withe the filename of .txt-file, witch faild to create gets print. 
                    try:
                        #----Umschalten bei Pfadangabe-----
                        #switch to first option when the code gets executed in the same directory where the code is stored. If you want to open the open the files from a other directory switch to second option.
                        #rot_text_file = open("./%s_%s_%s_%srot.txt" % (temp_stript, obj_class, line_num, rot), "x") #zu x wechseln nach dem Testn der Software, dammit keine bestehende b-Box-Files übeschriebn wenden sondern ein Fehler ausgegeben.
                        rot_text_file = open("%s/%s_%s_%s_%srot.txt" % (target_path, temp_stript, obj_class, line_num, rot), "x") #speicher von Dateien in beim Aufruf angegebene Pfad

                        # built the information string which sould get written to the new .txt-file, write it and safe it.
                        tmp = ' '
                        rot_text = tmp.join([text[0], text[1], text[2], str(w_trans_rel), str(h_trans_rel)])
                        rot_text_file.write(rot_text)
                        #print("Werte des rotierten txt-Files:", rot_text)
                        rot_text_file.close

                        # Bild im mittelpunk der b-Box rotieren und unter neum Namen abspeichern.
                        # rotate the image on the centerpixel for the given rotationangle.
                        rotated = colorImage.rotate(rot, center=(obj_center_x_pixel, obj_center_y_pixel))
                        

                        # Safe rotated Image

                        #----Umschalten bei Pfadangabe-----
                        #switch to first option when the code gets executed in the same directory where the code is stored. If you want to open the open the files from a other directory switch to second option.
                        #rotated.save('./%s_%s_%s_%srot.jpg' % (temp_stript, obj_class ,line_num, rot), quality=95) #muss gleiches format haben wie das zufor generierte Text-file
                        rotated.save('%s/%s_%s_%s_%srot.jpg' % (target_path, temp_stript, obj_class ,line_num, rot), quality=95) #speicher von Dateien in beim Aufruf angegebene Pfad

                        #rotated.show()
                    except: 
                        print("Text-file %s_%s_%s_%srot.txt bereits vorhanden, weiterfahren mit nächster Rotation." % (temp_stript, obj_class, line_num, rot))
                
                    it_zaehler += 1
                    continue
                
                line_num += 1
                print("while line_num < num_of_lines: -> %s mal Durchlaufen" % line_num)
                continue
            text_file.close()

        except:
            print("Fehler in 1.Try-Schlaufe")
print("Task erledigt :-)")
            