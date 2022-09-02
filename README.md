# Diamond_Music
Code and notebooks for working with Harry Partch's Tonality Diamond using Csound

Specifically, it's a repo for code that simplifies creating music using a Tonality Diamond to the 31-limit. Simplify might be too strong a term here. In order to use this, you will need some pretty awesome Csound chops, and a fair to middling Python skill set. A degree in music composition would help. Fortunately, that's my talent stack. 

The tonality diamond is a structure that is built using the overtones of a root key. The Wiki page has more information here: 

[Wiki Tonality Diamond Entry](https://en.wikipedia.org/wiki/Tonality_diamond)

Harry Partch first created a diamond with the overtones from 1 to 11. That is, he used pitches constructed from the ratios 1/1, 9/8, 5/4, 11/8, 3/2, 7/4. These notes are close to the 12 tone equal G, A, B, C+, D, F-, where minus is just a bit below natural, but not quite as low as a flat. He then constructed undertones on those overtones. An undertone is the inverse of an overtone, made by flipping the ratios upside down, so you have 2/1, 16/9, 8/5, 16/11, 4/3, 8/7. The overtone ratios are often notated as 8,9,10,11,12,14/8 and the undertones as 16/8, 9, 10, 11, 12, 14. 
I extended the Tonality Diamond first to the 15-limit, then the 31-limit, meaning the overtones from 16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31/16, and the undertones from 32/32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16.
If you have 16 overtones and 16 undertones on each, you end up with 256 pitches in the tonality diamond. Many are duplicates. Eliminating duplicates you end up with 213 pitches. I added four more pitches to my collection to reduce the gaps at either end of the octave (the intervals ['104/103', '52/51']
 at the bottom and ['51/26', '103/52'] at the top). That makes a total of 217. But the diamond itself has 213 unique pitches per octave. 

Here is a picture of the diamond, with ratios, a note name in Sagittal notation, and the step in the 217 tone to the octave scale.

![Diamond_31-limit](https://user-images.githubusercontent.com/16214057/187750941-36d333f3-bddc-42a2-83a0-e8103719bc77.jpg)

This repo contains a jupyter notebook and some python modules that can be used to send notes to an instance of Csound, a tool for creating music from text file. Most of the Csound code requires samples of musical instruments. I've included a subset of samples in this repo that include finger piano, balloon drums, guitars, and various percussion instruments. 
