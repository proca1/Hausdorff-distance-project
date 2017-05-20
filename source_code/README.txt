I file devono essere inseriti nella directory di GIMP, di solito è la segunte:
C:\Program Files\GIMP 2\lib\gimp\2.0\plug-ins


Il file Load-images.py si occupa della lettura e riconoscimento dei file immagine (PNG,JPG) all'interno della directory passata come parametro alla funzione:
	pdb.python_fu_Load_images(path)

Una volta ottenute le immagini, vengono inserite a due a due come livelli e successivamente viene calcolata la distanza di Hausdorff per ogni coppia di immagini.
La funzione che calcola la distanza di Hausdorff si trova nel file Hausdorff-distance.py ed è definita nel modo seguente:
	pdb.python_fu_Hausdorff_distance()

Una volta termionato il calcolo, questo viene salvato nel file distanze_hausdorff.csv  .

Successivamente ai due livelli viene effettuato il merging e salvato nella cartella result_images.