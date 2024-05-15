# com3528-team06

## Link to Download the Dataset
Download the [Dataset](https://drive.google.com/file/d/1-yfLj6kGllW8euEd0NepM4jNen8-IOrg/view?usp=sharing) here.

core -> miro's code
model_training.py -> python file for training the facial recognition model
requirement.txt -> specified the required packages information

Making sure the laptop is in 'Real Robot Mode':
robot_switch robot

Making sure the laptop is in miro mode:
robot_mode miro

Pairing the miro replace 'num' with the actual miro number, due to package discrepancy, the miro has to be connected using:
pair_with_miro [num]
instead of:
ssh miro@dia-miro[num]

Cloning our github repository:
git clone https://github.com/githubuser-acf21jl/com3528-team06.git

Go to the core directory:
cd com3528-team06/core

Making sure to install all the required packages before running the code:
pip3 install -r requirement.txt

After the environment is set up, go to core folder and run to activate the miro's demo mode:
./client_demo.py

If you want to test out the model performance using the webcam, uncomment the line 23 in subscriber_cam.py and run:
python3 subscriber_cam.py
when you want to run ./client_demo.py

