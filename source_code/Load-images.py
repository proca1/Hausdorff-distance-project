#!/usr/bin/env python

from gimpfu import *
import os

def load_images(path):
    
    
    #VENGONO SALVATE SU UN ARRAY SONO I FILE CHE SONO IMMAGINI png OPPURE jpg
    
    try:
        png_jpg_images = [filename for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename)) and (filename.lower().split(".")[-1] in ("png", "jpg"))];
    except Exception, error:
        pdb.gimp_message("ERRORE: caricamento immagini fallito\n");
    
    
    
    #VIENE CONTROLLATO SE IL NUMERO DELLE IMMAGINI E' PARI
    
    png_jpg_images_len = len(png_jpg_images);
    
    if png_jpg_images_len % 2 == 1: 
        pdb.gimp_message("IMMAGINI DISPARI: inserire o eliminare una immagine\n");
        return
    else:#se sono pari si esegue 
    
    
    
    
        open(path+"distanze_hausdorff.csv", "w").close();#pulizia file
        index = 0;
        while index != png_jpg_images_len:
            
            
            #VENGONO CARICATE LE IMMAGINI

            filename = png_jpg_images[index];
            if index % 2 == 0:

                #CARICAMENTO DELL'IMMAGINE IN MEMORIA
                img = pdb.gimp_file_load(os.path.join(path, filename),filename)
                img.layers[0].name = filename;

            else:

                #VIENE CARICATO IL SECONDO LAYER ALL'IMMAGINE PRECEDENTEMENTE INSERITA
                new_layer = pdb.gimp_file_load_layer(img,os.path.join(path, filename));
                new_layer.name = filename;
                pdb.gimp_image_insert_layer(img,new_layer,None,0);




            index = index + 1;


            if index % 2 == 0:#solo dopo aver caricato 2 layer si calcola la distanza


                #VIENE CALCOLATA E SALVATA LA DISTANZA DI HAUSDORFF

                hd = pdb.python_fu_Hausdorff_distance();



                #VENGONO SALVATE LE IMMAGINI E LE DISTANZE SU UN FILE 

                layer1 = img.layers[0];
                layer2 = img.layers[1];

                out_file = open(path+"distanze_hausdorff.csv","a");
                out_file.write("La distanza di Hausdorff tra le immagini:   "+layer1.name+" e "+layer2.name+" e' "+str(hd)+"\n\n");
                out_file.close();

                new_path = path+"result_images/";
                prev_index = index-1;
                merged_layer = pdb.gimp_image_merge_visible_layers(img, 1);
                #pdb.gimp_file_save(img,merged_layer,os.path.join(new_path,filename),'');#salvataggio immagine
                pdb.gimp_file_save(img,merged_layer,'%s/image%d_%d.png' % (new_path, prev_index, index),'');#salvataggio immagine


                #VENGONO RIMOSSI I LIVELLI PRECEDENTEMENTE INSERITI

                pdb.gimp_image_remove_layer(img,merged_layer);

    
    
    
    
    
    
    
register(
    "Load-images",
    N_("Caricamento immagini"),
    "Modulo per il caricamento delle immagini",
    "Emanuele Procacci",
    "Emanuele Procacci",
    "2016,2017",
    N_("_Load Images"),
    "RGB*, GRAY*",
    [
     (PF_DIRNAME,"path", "Directory to Open", "."),
    ],
    [],
    load_images,
    menu="<Image>/Filters/Render/Clouds",
    )
    
    
main()
