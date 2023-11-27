# pelletcam
Lima pelletcamproject



* LaserCutterBox.ai :  This is the Photoshop illustrator file to use for your lasercutter.
* ESP32SET.stl:  It contains all the files to 3D print the project
* palletcamAP.ino :  This is the sourcefile you need to install on the ESP32CAM.
  

To launch the camera, First you need to connect to the WIFI access point ssid = "PELLET", with password "OPENBIOLAB";
Off course you can change that passsord and SSID in the palletcamAP.ino file before uploading it to your ESP32CAM.

Step 1 :  Open a commandline and execute the pythonscript "python median_pixel_values_from_pictures.py"
Step 2 :  provide the path where you want to store the resultfiles
step 3 :  Place the reference pellet
step 4 :  place the pellet to measure.

The script will automatically calculate the 

![image](https://github.com/mdequanter/pelletcam/assets/74420584/84da7697-67b3-45b2-b5c7-9df7ed83dc8c)


Some pictures :

![20220310_065015_resized](https://github.com/mdequanter/pelletcam/assets/74420584/c54f9bf1-6c69-4060-ba23-52b73b9c86d0)


![20220310_063046_resized](https://github.com/mdequanter/pelletcam/assets/74420584/99a4a812-9dcd-4710-8fd7-079ca37f6a90)
