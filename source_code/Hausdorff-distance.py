#!/usr/bin/env python

from gimpfu import *
import sys
import math


def hausdorff_distance():
    

    #COSTANTI
    WHITE = 255;
    ALPHA = 255;
    POWER = 2;
    ADDITION_MODE = 7;
    X_DEFAULT = 100;
    Y_DEFAULT = 100;
    
    NC1 = 4;
    NC2 = 4;
    WHITE_CHANNEL1 = (WHITE,WHITE,WHITE,ALPHA);#colore e canali primo layer
    WHITE_CHANNEL2 = (WHITE,WHITE,WHITE,ALPHA);#colori e canali secondo layer
    
    PIXEL_COLOR_GREEN1 = [0, 255, 0, 255];
    
    
    
    #vengono settati i colori di foreground e background
    pdb.gimp_context_set_background((0,0,0,255));
    pdb.gimp_context_set_foreground((255,255,255,255));
    
    
    
    #SELEZIONE DELL'IMMAGINE E DEI PRIMI 2 LIVELLI

    # viene recuperata l'immagine
    img = gimp.image_list()[0];

    #vengono recuperati i livelli dell'immagine
    layer1 = img.layers[0];
    layer2 = img.layers[1];



    #SELEZIONE DEL BORDO DEL PRIMO LIVELLO E SUCCESSIVA DESELEZIONE
    
    #recupero pixel di default
    NC1,p1 = pdb.gimp_drawable_get_pixel(layer1,X_DEFAULT,Y_DEFAULT);
    if NC1 == 3:#se il layer1 ha 3 canali
        NC1 = 3;
        WHITE_CHANNEL1 = (WHITE,WHITE,WHITE);
        PIXEL_COLOR_GREEN1 = [0, 255, 0];

    # selezione dell'area dello stesso colore del pixel individuato da X_DEFAULT e Y_DEFAULT
    pdb.gimp_image_select_contiguous_color(img, 0, layer1, X_DEFAULT, Y_DEFAULT);

    #se l'area selezionata non e' quella bianca, viene invertita la selezione (gestione numero canali)
    if p1 != WHITE_CHANNEL1:
        pdb.gimp_selection_invert(img);
  
    
    
    # ristringe di un pixel la selezione
    pdb.gimp_selection_shrink(img, 1);
    # riempe il contenuto selezionato
    pdb.gimp_edit_bucket_fill(layer1, 1, 0, 100, 0, FALSE, X_DEFAULT, Y_DEFAULT);
    # deseleziona 
    pdb.gimp_selection_clear(img);



    #SELEZIONE DEL BORDO DEL SECONDO LIVELLO E SUCCESSIVA DESELEZIONE
    
    #recupero pixel di default
    NC2, p2 = pdb.gimp_drawable_get_pixel(layer2,X_DEFAULT,Y_DEFAULT);
    if NC2 == 3:#se il layer1 ha 3 canali
        NC2 = 3;
        WHITE_CHANNEL2 = (WHITE,WHITE,WHITE);

    # selezione dell'area dello stesso colore del pixel individuato da X_DEFAULT e Y_DEFAULT
    pdb.gimp_image_select_contiguous_color(img, 0, layer2, X_DEFAULT, Y_DEFAULT);

    #se l'area selezionata non e' quella bianca, viene invertita la selezione
    if p2 != WHITE_CHANNEL2:
        pdb.gimp_selection_invert(img);
    
    
    
    # ristringe di un pixel la selezione
    pdb.gimp_selection_shrink(img, 1);
    # riempe il contenuto selezionato
    pdb.gimp_edit_bucket_fill(layer2, 1, 0, 100, 0, FALSE, X_DEFAULT, Y_DEFAULT);
    # deseleziona 
    pdb.gimp_selection_clear(img);

    
    
    #INSERIMENTO PIXEL BIANCHI DEI 2 LIVELLI

    #array contenente i pixel bianchi del layer1 e del layer2
    layer1_white_pixels = [];
    layer2_white_pixels = [];

    for x in range(0,img.width):
        for y in range(0,img.height):

            #viene recuperato il pixel e il numero dei canali ad esso associati per il layer 1
            num_channels1, pixel1 = pdb.gimp_drawable_get_pixel(layer1,x,y);

            #viene recuperato il pixel e il numero dei canali ad esso associati per il layer 2
            num_channels2, pixel2 = pdb.gimp_drawable_get_pixel(layer2,x,y);

            #vengono popolati gli arrey contenenti tutti i pixel bianchi dei 2 layer
            if pixel1 == WHITE_CHANNEL1:
                pos = Pos(x,y);
                layer1_white_pixels.append(pos);
            else:
                if pixel2 == WHITE_CHANNEL2:
                    pos = Pos(x,y);
                    layer2_white_pixels.append(pos);
                    
                    
    
    #CALCOLO DISTANZA HAUSDORFF

    max_dis1 = -sys.maxsize;
    max_dis2 = -sys.maxsize;

    #punti a distanza minima
    x1_temp1 = 0;
    x2_temp1 = 0;
    y1_temp1 = 0;
    y2_temp1 = 0;

    x11_temp = 0;
    y11_temp = 0;
    x22_temp = 0;
    y22_temp = 0;

    x1 = 0;
    y1 = 0;
    x2 = 0;
    y2 = 0;

    x11 = 0;
    y11 = 0;
    x22 = 0;
    y22 = 0;
    
    
    #sup x (inf y)
    for i in range(0,len(layer1_white_pixels)):

        min_dis1 = sys.maxsize;

        for j in range(0,len(layer2_white_pixels)):
            
            #(x1 - x2)^2
            x_dis = layer1_white_pixels[i].x - layer2_white_pixels[j].x;
            pow_abs_x_dis = pow(x_dis, POWER);

            #(y1 - y2)^2
            y_dis = layer1_white_pixels[i].y - layer2_white_pixels[j].y;
            pow_abs_y_dis = pow(y_dis, POWER);

            #(x1 - x2)^2 + (y1 - y2)^2
            sum_value = pow_abs_x_dis + pow_abs_y_dis;

            #sqrt( (x1 - x2)^2 + (y1 - y2)^2 )
            dis = math.sqrt(sum_value);

            if dis < min_dis1:
                min_dis1 = dis;
                x1_temp1 = layer1_white_pixels[i].x;
                y1_temp1 = layer1_white_pixels[i].y;
                x2_temp1 = layer2_white_pixels[j].x;
                y2_temp1 = layer2_white_pixels[j].y;

        #viene calcolato il sup ad ogni ciclo, ottimizzazione     
        if min_dis1 > max_dis1:
            max_dis1 = min_dis1;
            x1 = x1_temp1;
            y1 = y1_temp1;
            x2 = x2_temp1;
            y2 = y2_temp1;
    
    
    
    
    
    
    #sup y (inf x)
    for i in range(0,len(layer2_white_pixels)):

        min_dis2 = sys.maxsize;

        for j in range(0,len(layer1_white_pixels)):

            #(x2 - x1)^2
            x_dis = layer2_white_pixels[i].x - layer1_white_pixels[j].x;
            pow_abs_x_dis = pow(x_dis, POWER);

            #(y2 - y1)^2
            y_dis = layer2_white_pixels[i].y - layer1_white_pixels[j].y;
            pow_abs_y_dis = pow(y_dis, POWER);

            #(x2 - x1)^2 + (y2 - y1)^2
            sum_value = pow_abs_x_dis + pow_abs_y_dis;

            #sqrt( (x2 - x1)^2 + (y2 - y1)^2 )
            dis = math.sqrt(sum_value);

            if(dis < min_dis2):
                min_dis2 = dis;
                x11_temp = layer2_white_pixels[i].x;
                y11_temp = layer2_white_pixels[i].y;
                x22_temp = layer1_white_pixels[j].x;
                y22_temp = layer1_white_pixels[j].y;

        #viene calcolato il sup ad ogni ciclo, ottimizzazione     
        if min_dis2 > max_dis2:
            max_dis2 = min_dis2;
            x11 = x11_temp;
            y11 = y11_temp;
            x22 = x22_temp;
            y22 = y22_temp;


 



    


    #DISTANZA DI HAUSDORFF
    
    hausdorff_dis = max([max_dis1,max_dis2])
    
    
    
    
    
    
    #VIENE VISUALIZZATA LA DISTANZA DI HAUSDORFF
    
    pdb.gimp_context_set_foreground((153,0,0,255));
    pdb.gimp_context_set_brush_size(1.0);
    
    
    if(hausdorff_dis == max_dis1):
        
        pdb.gimp_pencil(layer1, 4, [x1,y1,x2,y2]);
        
        
        #estremi(e loro intorno) del segmento relativo alla distanza di Hausdorff colorati di verde
        pdb.gimp_drawable_set_pixel(layer1,x1,y1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2,y2,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1+1,y1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2+1,y2,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1-1,y1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2-1,y2,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1,y1+1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2,y2+1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1,y1-1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2,y2-1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1+1,y1+1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2+1,y2+1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1-1,y1+1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2-1,y2+1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1-1,y1-1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2-1,y2-1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x1+1,y1-1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x2+1,y2-1,NC1,PIXEL_COLOR_GREEN1);
        
    else:
        
        pdb.gimp_pencil(layer1, 4, [x11,y11,x22,y22]);
        
        
        #estremi(e loro intorno) del segmento relativo alla distanza di Hausdorff colorati di verde
        pdb.gimp_drawable_set_pixel(layer1,x11,y11,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22,y22,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11+1,y11,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22+1,y22,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11-1,y11,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22-1,y22,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11,y11+1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22,y22+1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11,y11-1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22,y22-1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11+1,y11+1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22+1,y22+1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11-1,y11+1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22-1,y22+1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11-1,y11-1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22-1,y22-1,NC1,PIXEL_COLOR_GREEN1);

        pdb.gimp_drawable_set_pixel(layer1,x11+1,y11-1,NC1,PIXEL_COLOR_GREEN1);
        pdb.gimp_drawable_set_pixel(layer1,x22+1,y22-1,NC1,PIXEL_COLOR_GREEN1);
    
    
    
    #SOMMA DEI 2 LIVELLI
    
    pdb.gimp_layer_set_mode(layer1,ADDITION_MODE);
    
    
    
    

    return hausdorff_dis;
    
    
    
    
    
    
    
    
    
class Pos:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;    


register(
    "Hausdorff-distance",
    N_("Calcolo della distanza di Hausdorff"),
    "Calcolo della distanza di Hausdorff",
    "Emanuele Procacci",
    "Emanuele Procacci",
    "2016,2017",
    N_("_Hausdorff Distance"),
    "RGB*, GRAY*",
    [
    ],
    [
     (PF_FLOAT, "dist", "Hausdorff distance", hausdorff_distance),
    ],
    hausdorff_distance,
    menu="<Image>/Filters/Render/Clouds",
    )
    
    
main()
