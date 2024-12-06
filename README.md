# Project Title: Putting Analyzer 

**Project Description**: A program that turns on live video through webcam, and allows users to take videos on the spot of their putting stroke from behind/down-the-line. If they so choose, they can also import mp4 files of their putting stroke. After recording using key presses or importing a video, users can then mark the corners of their putter for a set amount of frame intervals and after the stroke is completely marked, a score of the quality and consistency of the recorded stroke is outputted through an algorithm. Specific feedback can be generated (such as the stroke arc needs to be worked on, or the impact position). A previous recorded video function is also implemented, as after the user initially records a video through the program, and then goes to import a file, they have the ability to pull up the previously recorded video to potentially reanalyze. This is accompanied by a simple, aesthetic, and fitting UI for users to clearly and understandably interact with the program. 

**Run Instructions**: Putting Analyzer utilizes a variety of libraries and modules to run properly. Here's a rundown of the steps to run and installations needed to run the program properly. 

To run the project, run *only* `final.py`. If you would like to import any mp4 files of your putting stroke, put them in the same directory/folder that final.py is apart of in order for Putting Analyzer to have access to them. Be aware that through starting the app, both previousRecording.mp4 and finalOutput.mp4 files will pop up. Do not worry, as previousRecording.mp4 is the file path that allows the ability to bring up the previous recording, and finalOutput.mp4 is the recording currently being recorded, for replay purposes. 

1. **os**
By importing os, the functionality of selecting mp4 files (of one's putting stroke) in the directory is possible through pathlib. Simply add "import os" to the program.
2. **OpenCV as cv2**
OpenCV is a library of functions related to real-time computer vision, and allows Putting Analyzer to use the computer's default webcam to record putting strokes, and do frame-by-frame reading and cycling.
In order to install, use `pip install opencv-python` for the basic package (which is sufficient for Putting Analyzer) or `pip install opencv-contrib-python` for the entire package. Adjust to pip3 if needed.
3. **CMU Graphics**
CMU Graphics is the graphics package that the program revolves around. Instructions to download by installing the folder and adding to the directory can be reached here: https://academy.cs.cmu.edu/desktop. If you would like to pip install, follow the instructions on this website depending on your operating system: https://pypi.org/project/cmu-graphics/.
4. **Python Imaging Library (PIL)**
PIL is a library that allows for opening and altering image files. It is the main functionality that allows the integration between CMU graphics and cv2. To install, use `pip install pillow`. Adjust to pip3 if needed.
5. **Python Urllib Module**
Urllib allows for the opening of URLs within Putting Analyzer, and is mainly for the user interface and presentation of the program. To install, use `pip install urllib`. Adjust to pip3 if needed.
6. **NumPy**
NumPy is a mathematical library that enables programs to utilize high-level math functions needed for calculations. It plays a vital role in the algorithm for the rating system in Putting Analyzer. To install, use `pip install numpy`. Adjust to pip3 if needed. 

**Shortcut Commands**
There are no shortcut commands to be used in Putting Analyzer. 
