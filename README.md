# pelletcam
Lima pelletcamproject

# design and production

* LaserCutterBox.ai :  This is the Photoshop illustrator file to use for your lasercutter.
* ESP32SET.stl:  It contains all the files to 3D print the project.  Use black PLA to print all parts
* pelletcamAP.ino :  This is the sourcefile you need to install on the ESP32CAM.
  

To launch the camera, First you need to connect to the WIFI access point ssid = "PELLET", with password "OPENBIOLAB";
Off course you can change that passsord and SSID in the pelletcamAP.ino file before uploading it to your ESP32CAM.

Connections are as follows :

![image](https://github.com/mdequanter/pelletcam/assets/74420584/6b70f90a-863b-4643-a1b7-81c548564fef)


# How to use the software?

Step 1 :  Open a commandline and execute the pythonscript "pallet.py"
Step 2 :  provide the path where you want to store the resultfiles
step 3 :  Place the reference pellet
step 4 :  click with your mouse on the center of the spot you want to measure.
step 5 :  Now you can enter process a sample and select the spot.
step 6 :  each time you press "Enter" you will be able to process a new sample.  

You can also install those shortcuts on your laptop.  How to use this is described in the pdf MANUAL_PELLETCAM_2_1_EN.pdf

When you want to start a new testset, press "r", then you will again have to add a reference sample. 

The result is a csv file with following values :

sampleID,picture_path,date,colour_info_dict["median_R"],colour_info_dict["median_G"],colour_info_dict["median_B"],reference_R,reference_G,reference_B

All the pictures are stored in the output folder for later analyses

![image](https://github.com/mdequanter/pelletcam/assets/74420584/84da7697-67b3-45b2-b5c7-9df7ed83dc8c)


# Some pictures 

![20220310_065015_resized](https://github.com/mdequanter/pelletcam/assets/74420584/c54f9bf1-6c69-4060-ba23-52b73b9c86d0)


![20220310_063046_resized](https://github.com/mdequanter/pelletcam/assets/74420584/99a4a812-9dcd-4710-8fd7-079ca37f6a90)
