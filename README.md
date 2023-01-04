# Diamond_Music
Code and notebooks for working with Harry Partch's Tonality Diamond using Csound

Specifically, it's a repo for code that simplifies creating music using a Tonality Diamond to the 31-limit. Simplify might be too strong a term here. In order to use this, you will need some pretty awesome Csound chops, and a fair to middling Python skill set. A degree in music composition would help. Fortunately, that's my talent stack. 

The tonality diamond is a structure that is built using the overtones of a root key. The Wiki page has more information here: 

[Wiki Tonality Diamond Entry](https://en.wikipedia.org/wiki/Tonality_diamond)

Harry Partch first created a diamond with the overtones from 1 to 11. That is, he used pitches constructed from the ratios 1/1, 9/8, 5/4, 11/8, 3/2, 7/4. These notes are close to the 12 tone equal G, A, B, C+, D, F-, where minus is just a bit below natural, but not quite as low as a flat. He then constructed undertones on those overtones. An undertone is the inverse of an overtone, made by flipping the ratios upside down, so you have 2/1, 16/9, 8/5, 16/11, 4/3, 8/7. The overtone ratios are often notated as 8,9,10,11,12,14/8 and the undertones as 16/8, 9, 10, 11, 12, 14. 
I extended the Tonality Diamond first to the 15-limit, then the 31-limit, meaning the overtones from 16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31/16, and the undertones from 32/32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16.
If you have 16 overtones and 16 undertones on each, you end up with 256 pitches in the tonality diamond. Many are duplicates. Eliminating duplicates you end up with 213 pitches.

Here is a picture of the diamond, with ratios, a note name in Sagittal notation, and the step in a 217 tone version to the octave scale. I used the 2113 in the diamond and added two more at the top and bottom to fill out the spectrum. In these notebooks I started out using that 217 tone scale, then switched to the 256 tone version for mathematical simplification. The 256 tone verion includes many duplicates, but csound doesn't care.

![Diamond_31-limit](https://user-images.githubusercontent.com/16214057/187750941-36d333f3-bddc-42a2-83a0-e8103719bc77.jpg)

This repo contains a jupyter notebook and some python modules that can be used to send notes to an instance of Csound, a tool that takes text files as input and generates an audio file. If you do it right, it is a marvelous way to create music. My use of Csound consists of taking samples of actual instruments and creating music from the samples. But Csound can generate almost every kind of electronic synthesis every conceived. My code requires samples of musical instruments. I've included a subset of samples in this repo that include finger piano, balloon drums, guitars, and various percussion instruments. 

## Installation Requirements 

I've found that the simplest way to set up the minimal environment to run this code is to do the following:
1.    I recommend the a container builder called toolbox to create containers, but that is optional. It builds containers behind the scenes and give you access to the host file system. 
            toolbox create virtual_python
            toolbox enter virtual_python
2.    Inside the toolbox install python3.11            
            sudo dnf install python3.11 -y
3.    verify it's the right version
            python3.11 --version
4.    create a REPL to try some python code
            python3.11
5.    execute some sample python code:
            print('Hello World!")
            quit()
6.    create a test directory
            mkdir ~/virtual_python && cd ~/virtual_python
7.    build a python virtual environment
            python3.11 -m venv virtual_python
8.    Activate the environment
            source virtual_python/bin/activate
9.    install pip in the virtual environment             
            python3.11 -m pip install --upgrade pip
10.   install other packages:
            pip3.11 install jupyterlab
            # I also use these libraries, but I can't find them at the moment importlib pprint pprint copy logging os
            pip3.11 install numpy 
            pip3.11 install matplotlib
            pip3.11 install scipy

11.   If you have trouble installing specific packages using PIP, you should install the following packages:
            sudo dnf install gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget make -y
12.   If you want to run csound:
            sudo dnf install csound-devel sox            
13.   Once this is done, to start up a jupyter lab session:
            jupyter-lab            
13.   When you have finished, you can exit the virtual environment:
            deactivate                         

### Installation info for toolbox:
https://github.com/containers/toolbox            

# Installation instructions are in the jupyter notebook called Diamond_music_combined_voices.ipynb
