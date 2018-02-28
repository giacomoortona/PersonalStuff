#	new file:   FCC/cardMaker.py
#	new file:   FCC/ch.py
#	new file:   FCC/convertHistos.py
#	new file:   FCC/readHisto.py

Macros to prepare FCC HH analysis cards (bbgg)
See inside the macros for various options.
The macros have been finetuned to work for bbgg, modifications will likely be needed for other uses

To prepare the morphed signal analysis:
1) run convertHistos.py (this creates the data_obs histogram and changes a few names to ease the reading of the histogram)
2) run readHistos.py to create one card for each lambda value in the scan
3) run ch.py This macro builds the morphed PDF and create the final workspace

To prepared the parametric signal analysis (my favourite right now)
1) run cardMaker.py
This creates one single card where the signal lineshape and rate depend on kl. One can then simply use combine with -P kl to define kl as POI
