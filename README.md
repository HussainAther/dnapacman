# DNA Pac-Man

![Screenshot](http://i.imgur.com/hXfYnMp.png)

## Background:

In a biological twist on a retro title, Pac-Man (playing the role of ribosomal RNA) must transcribe sequences of mRNA into amino acids. You must turn as many bases into amino acids as possible. Start your amino acid chain by finding a START sequence ("AUG") and, after that, transcribe as many bases as possible. Look for the STOP Codon ("UAA", "UAG", and "UGA") to finish an amino acid. Your amino acid strings will print as you play. Good luck!

## Instructions:

    1. Click "Download ZIP" on the right column.

    2. unzip the directory

    Either:

    3. cd into the directory from the Terminal and run: python pacman.py

    or:
    
    3. Right-click on pacman.py and open with Python Launcher
    
## Options:
    Use "python pacman.py --help for full options"

    -g	Ghost Mode: Can be set to “RandomGhost” (ghosts move randomly) or “DirectionalGhost” (ghosts chase you)

    -k	Number of Ghosts: Can be set to 0, 1, 2, 3, or 4.

    -l	Layout: Can be set to “mediumClassic”, “minimaxClassic”, “openClassic”, “originalClassic”, “smallClassic”, “testClassic”, “trappedClassic”, or “trickyClassic”

    -n	How many games in a row you will play: Can be set to whatever.

## Credits

Hussain Ather (hussainather.com)
Jonathan Lu

## AMINO ACID CHART:
"UUU":"Phe" (F) Phenylalanine

"UUC":"Phe" (F) Phenylalanine

"UUA":"Leu" (L) Leucine

"UUG":"Leu" (L) Leucine

"UCU":"Ser" (S) Serine

"UCC":"Ser" (S) Serine

"UCA":"Ser" (S) Serine

"UCG":"Ser" (S) Serine

"UAU":"Tyr" (Y) Tyrosine

"UAC":"Tyr" (Y) Tyrosine

"UAA":" *"  ( ) STOP

"UAG":" *"  ( ) STOP

"UGU":"Cys" (C) Cysteine

"UGC":"Cys" (C) Cysteine

"UGA":" *"  ( ) STOP

"UGG":"Trp" (W) Tryptophan

"CUU":"Leu" (L) Leucine

"CUC":"Leu" (L) Leucine

"CUA":"Leu" (L) Leucine

"CUG":"Leu" (L) Leucine

"CCU":"Pro" (P) Proline

"CCC":"Pro" (P) Proline

"CCA":"Pro" (P) Proline

"CCG":"Pro" (P) Proline

"CAU":"His" (H) Histidine

"CAC":"His" (H) Histidine

"CAA":"Gln" (Q) Glutamine

"CAG":"Gln" (Q) Glutamine

"CGU":"Arg" (R) Arginine

"CGC":"Arg" (R) Arginine

"CGA":"Arg" (R) Arginine

"CGG":"Arg" (R) Arginine

"AUU":"Ile" (I) Isoleucine

"AUC":"Ile" (I) Isoleucine

"AUA":"Ile" (I) Isoleucine

"AUG":"Met" (M) Methionine (START)

"ACU":"Thr" (T) Threonine

"ACC":"Thr" (T) Threonine

"ACA":"Thr" (T) Threonine

"ACG":"Thr" (T) Threonine

"AAU":"Asn" (N) Asparagine

"AAC":"Asn" (N) Asparagine

"AAA":"Lys" (K) Lysine

"AAG":"Lys" (K) Lysine

"AGU":"Ser" (S) Serine

"AGC":"Ser" (S) Serine

"AGA":"Arg" (R) Arginine

"AGG":"Arg" (R) Arginine

"GUU":"Val" (V) Valine

"GUC":"Val" (V) Valine

"GUA":"Val" (V) Valine

"GUG":"Val" (V) Valine

"GCU":"Ala" (A) Alanine

"GCC":"Ala" (A) Alanine

"GCA":"Ala" (A) Alanine

"GCG":"Ala" (A) Alanine

"GAU":"Asp" (D) Aspartic acid (Aspartate)

"GAC":"Asp" (D) Aspartic acid (Aspartate)

"GAA":"Glu" (E) Glutamic acid (Glutamate)

"GAG":"Glu" (E) Glutamic acid (Glutamate)

"GGU":"Gly" (G) Glycine

"GGC":"Gly" (G) Glycine

"GGA":"Gly" (G) Glycine

"GGG":"Gly" (G) Glycine
