 GAZEMATE

 A Low-Cost Eye-Gaze Based Communication and Control Access System for Paralysed Patients

GAZEMATE is an assistive technology system designed to help people with limited or no physical interaction communicate and control a computer using eye-gaze movements.

The system uses a webcam to detect the user's face and eyes, estimate gaze direction, control the mouse cursor, perform dwell-based clicks, provide an accessible virtual keyboard, and convert entered text into speech.



 Project Workflow

Webcam  
↓  
Face & Eye Detection  
↓  
Iris Detection  
↓  
Gaze Estimation  
↓  
Calibration  
↓  
Cursor Control  
↓  
Dwell Click  
↓  
Accessible Virtual Keyboard  
↓  
Text-to-Speech



 Project Structure


GAZEMATE

 main.py
    |
 integrated_eye_detection.py
 integrated_gaze.py
 integrated_calibration.py
 integrated_cursor.py
 integrated_dweell.py
 integrated_keyboard.py
 integrated_text_speech.py
      |
 dummy_keyboard.py
      |
 test_cursor.py
 test_dwell.py
      |
 .gitignore
 README.md

 File                           Purpose                                                           
 
 main.py                      Main program that integrates all modules and runs the system      
 integrated_eye_detection.py  Detects the user's face, eyes and iris landmarks                  
 integrated_gaze.py           Estimates gaze direction using eye and iris landmarks             
 integrated_calibration.py    Performs gaze calibration and maps gaze coordinates to the screen 
 integrated_cursor.py         Converts gaze coordinates into mouse cursor movement              
 integrated_dweell.py         Implements dwell-based clicking using gaze                        
 integrated_keyboard.py       Provides an accessible virtual keyboard controlled using gaze     
 integrated_text_speech.py    Converts entered text into speech                                 
 dummy_keyboard.py            Simplified keyboard implementation used for testing               
 test_cursor.py               Used to test cursor control functionality                         
 test_dwell.py                Used to test dwell-click functionality                            
 .gitignore                   Specifies files and folders that should not be tracked by Git     
 README.md                    Contains project documentation, structure and usage information   
