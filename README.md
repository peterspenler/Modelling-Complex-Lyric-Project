# README

## Description
There are 2 main components to this project. First is the trainer notebook which is used to scrape lyrics from genius.com, and then to use those lyrics to train a neural network language model. Second is the generator notbook which loads a trained model and generates unique lyrics using that model.

## Steps to run
There are a couple nesseccary steps to perform before using this project.
First you should set up the appropriate conda environment. If you have an Nvidia GPU this is in the 'environment.yml' file. If not you should use the 'environment-cpu.yml' file instead to run the project only with your CPU. In addition to using this environment, to run on a CPU you must change the instances of 'torch.cuda.LongTensor' into 'torch.LongTensor'. All of these instances should be present in the 'generate_text' funcitons.

Next you also need to download our trained models and the wt103 model. These are available in the 'models.tar.gz' file here:

https://github.com/peterspenler/Modelling-Complex-Lyric-Project/releases/tag/v1.0

Extract the 'models' folder into the 'data' directory in the root of the project.After these steps you should be able to run the project by activating the appropriate conda environment and running the command 'jupyter notebook' in the root of the project. You can then run the 'Song Model Trainer' or 'Song Model Generator' noebook to train a model or generate lyrics respectively.
