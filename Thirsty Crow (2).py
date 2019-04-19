"""
**************************************************************************
* Team Id: 1753
* Author list: Guruprasad Bhat, Anjaneya Ketkar, Sankirthana Saraswatula, Nilesh Gandhi
* Filename: Thirsty Crow.py
* Theme: Thirsty Crow
* Functions: getCameraMatrix(),init_gl(),resize(),drawGLScene(),detect_markers()
*        draw_background(),init_object_texture(),init_object_texture(),overlay(),main()
*Global Variables: n, waterPitcher, pebble, crow, dimin, texture_object ,texture_background = None
*                camera_matrix,dist_coeff, cap,count,visitingOrder,arena_config ,Robot_start 
**************************************************************************
"""
from pathPlanning import *
import serial
import time
import numpy as np
import cv2
import cv2.aruco as aruco
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import pygame
from objloader import *
n=0
waterPitcher=None
pebble=None
crow=None
dimin=None
texture_object = None
texture_background = None
camera_matrix = None
dist_coeff = None
cap = cv2.VideoCapture(1)
INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [-1.0,-1.0,-1.0,-1.0],
                           [ 1.0, 1.0, 1.0, 1.0]])
count=0
visitingOrder=[]
arena_config = {0: ("Water Pitcher", 6, "2-2"),
2:("Pebble",8, "3-3"),
4:("Pebble",16, "2-2"),
6:("Pebble", 19, "1-1"),
}
Robot_start="start1"

################## Define Utility Functions Here #######################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""
def getCameraMatrix():
        global camera_matrix, dist_coeff
        with np.load('System.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
########################################################################

############# Main Function and Initialisations ########################
"""
Function Name : main()
Input: None
Output: None
Purpose: Initialises OpenGL window and callback functions. Then starts the event
         processing loop.Also takes in the entire path info with list of turns and
		 order of visiting.
"""        
def main():
        global p,turns,visitingOrder   # declaring as global variables
        aruco_idKeys=list(arena_config.keys())
	p,turns,visitingOrder=pathPlanning.flow(Robot_start ,arena_config)  # calling flow function from pathPlanning class file
        turns=list(turns)				#converting into list
        glutInit()
        getCameraMatrix()
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(625, 100)
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
        window_id = glutCreateWindow("OpenGL")
        #print(p)
        #print(turns)
        #print(visitingOrder)
        init_gl()
        glutDisplayFunc(drawGLScene)
        glutIdleFunc(drawGLScene)
        glutReshapeFunc(resize)
        glutMainLoop()

"""
Function Name : init_gl()
Input: None
Output: None
Purpose: Initialises various parameters related to OpenGL scene.
"""  
def init_gl():
        global texture_object, texture_background
        global crow,waterPitcher, pebble
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0) 
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        texture_background = glGenTextures(1)
        texture_object = glGenTextures(1)
		#Loading obj files of blender models of crow, pitcher, pebbles(full & diminished) through OBJ class file
        crow=OBJ('Crow.obj',swapyz=True)
        waterPitcher=OBJ('fullpitcher04.obj',swapyz=True)
        pebble=OBJ('rock2.obj',swapyz=True)
        dimin=OBJ('rock1final.obj',swapyz=True)
"""
Function Name : resize()
Input: None
Output: None
Purpose: Initialises the projection matrix of OpenGL scene
"""
def resize(w,h):
        ratio = 1.0* w / h
        glMatrixMode(GL_PROJECTION)
        glViewport(0,0,w,h)
        gluPerspective(45, ratio, 0.1, 100.0)     
"""
Function Name : drawGLScene()
Input: None
Output: None
Purpose: It is the main callback function which is called again and
         again by the event processing loop. In this loop, the webcam frame
         is received and set as background for OpenGL scene. ArUco marker is
         detected in the webcam frame and 3D model is overlayed on the marker
         by calling the overlay() function.Serial communication is opened in this fumction.
		 The list of turns is passed to the serial com port one by one whenever the port recieves
		 character 'n'.
"""
def drawGLScene():
        global count,n,turns
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ar_list = []
        ret, frame = cap.read() #reading webcam feed
        rec=''
        data=''
        ser = serial.Serial("COM16", 9600, timeout=0.005) # Opening serial comunication at COM port16 with baud rate 9600 
        if ret == True:
                draw_background(frame)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                ar_list = detect_markers(frame)
                time.sleep(1)
                rec=ser.read()	# reading character through serial port
                print(rec)
                if(rec==str.encode('n')): # whenever the bot reaches a node, expect to recieve a 'n' 
                        data=turns[n]
                        print(data)
                        if(data=='p'):		# if bot approaches for pebble pickup/drop
                                count=count+1
                        data=str.encode(data)	
                        ser.write(data)		# write data to bot for giving the turn at each node
                        n=n+1			# increment node counter
                        
                for i in ar_list:
                        if i[0] == aruco_idKeys[0]: #for 
                                if count==0:                    #Calling overlay function with appropiate texture(empty/half/full) depending on the count value             
                                    overlay(frame, ar_list, i[0],"emptypitcherfinal.png")
                                if (count>=2) and (count<4):                                
                                    overlay(frame, ar_list, i[0],"halfpitcherfinal.png")
                                if (count>=4) and (count<6):                                

                                    overlay(frame, ar_list, i[0],"halfpitcher.png")
                                if count==6:                                
                                    overlay(frame, ar_list, i[0],"fullpitcherfinal.png")
                        if i[0] == aruco_idKeys[1]:				
                                overlay(frame, ar_list, i[0],"rock1.png")
                        if i[0] == aruco_idKeys[2]:                                
                                overlay(frame, ar_list, i[0],"rock1.png")
                        if i[0] == aruco_idKeys[3]:
                                overlay(frame, ar_list, i[0],"rock1.png")
                        if i[0] == 10:
                                overlay(frame, ar_list, i[0],"black.png")
                draw_background(frame)                
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
        glutSwapBuffers()
        
########################################################################

######################## Aruco Detection Function ######################
"""
Function Name : detect_markers()
Input: img (numpy array)
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""
def detect_markers(img):
        aruco_list = []
        ################################################################
        #################### Same code as Task 1.1 #####################
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
        parameters = cv2.aruco.DetectorParameters_create()
        corners,aruco_id, _ = cv2.aruco.detectMarkers(img, aruco_dict,parameters = parameters)
        rvec, tvec,_= cv2.aruco.estimatePoseSingleMarkers(corners,100, camera_matrix, dist_coeff)
        aruco_centre=[]
        if np.all(aruco_id != None):
                for i in range(len(aruco_id)):
                        aruco_centre=list(np.mean(corners[i][0],axis=0))
                        aruco_list.append((aruco_id[i],tuple(map(int,aruco_centre)),np.reshape(rvec[i],(1,1,3)),np.reshape(tvec[i],(1,1,3))))
        
        ################################################################
        return aruco_list

"""
Function Name : draw_background()
Input: img (numpy array)
Output: None
Purpose: Takes image as input and converts it into an OpenGL texture. That
         OpenGL texture is then set as background of the OpenGL scene
"""
def draw_background(img):
        bg_image = cv2.flip(img, 0)
        bg_image = Image.fromarray(bg_image)     
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
        

        glEnable(GL_TEXTURE_2D)      
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
         
        glBindTexture(GL_TEXTURE_2D, texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-10.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd( )
        glPopMatrix()
             
        
        return None

"""
Function Name : init_object_texture()
Input: Image file path
Output: None
Purpose: Takes the filepath of a texture file as input and converts it into OpenGL
         texture. The texture is then applied to the next object rendered in the OpenGL
         scene.
"""
def init_object_texture(image_filepath):
        
        tex=cv2.imread(image_filepath)
        tex=cv2.flip(tex,0)
        tex=Image.fromarray(tex)
        glEnable(GL_TEXTURE_2D)
               
        ix = tex.size[0]
        iy = tex.size[1]
        tex = tex.tobytes("raw", "RGBX", 0, -1)
 
        glBindTexture(GL_TEXTURE_2D, texture_object)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE,tex)
                
        return None

"""
Function Name : overlay()
Input: img (numpy array), aruco_list, aruco_id, texture_file (filepath of texture file)
Output: None
Purpose: Receives the ArUco information as input and overlays the 3D Model of a teapot
         on the ArUco marker. That ArUco information is used to
         calculate the rotation matrix and subsequently the view matrix. Then that view matrix
         is loaded as current matrix and the 3D model is rendered.

         Parts of this code are already completed, you just need to fill in the blanks. You may
         however add your own code in this function.
"""
def overlay(img, ar_list, ar_id, texture_file):
        for x in ar_list:
                if ar_id == x[0]:
                        centre, rvec, tvec = x[1], x[2], x[3]
        rmtx = cv2.Rodrigues(rvec)[0]
        view_matrix =  np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],(tvec[0][0][0]+50)/240],
                                [rmtx[1][0],rmtx[1][1],rmtx[1][2],(tvec[0][0][1]-240)/225],
                                [rmtx[2][0],rmtx[2][1],rmtx[2][2],(tvec[0][0][2]-240)/230],
                                [0.0       ,0.0       ,0.0       ,1.0    ]])
        view_matrix = view_matrix * INVERSE_MATRIX
        view_matrix = np.transpose(view_matrix)

        
        init_object_texture(texture_file)
        glPushMatrix()
        glLoadMatrixd(view_matrix)
        #glutSolidTeapot(0.5)
        #print(tvec[0][0][0])
        #print(tvec[0][0][1])
        #print(tvec[0][0][2])
        if(ar_id ==aruco_idKeys[0]):
                glCallList(waterPitcher.gl_list) # Render Water Pitcher      
        if (count >= 1) and (count <3):			# Render corresponding pebble (full/ diminished depending on the count value
                if(ar_id ==int(visitingOrder[0])):
                    glCallList(dimin.gl_list)
                if(ar_id ==int(visitingOrder[1])):
                    glCallList(pebble.gl_list)        
                if(ar_id ==int(visitingOrder[2])):
                    glCallList(pebble.gl_list)
        if (count >= 3) and (count <5):
                if(ar_id ==int(visitingOrder[0])):
                    glCallList(dimin.gl_list)
                if(ar_id ==int(visitingOrder[1])):
                    glCallList(dimin.gl_list)        
                if(ar_id ==int(visitingOrder[2])):
                    glCallList(pebble.gl_list)
        if count >= 5:
                if(ar_id ==int(visitingOrder[0])):
                    glCallList(dimin.gl_list)
                if(ar_id ==int(visitingOrder[1])):
                    glCallList(dimin.gl_list)        
                if(ar_id ==int(visitingOrder[2])):
                    glCallList(dimin.gl_list)        
        if count==0:
                if(ar_id ==int(visitingOrder[0])):
                    glCallList(pebble.gl_list)
                if(ar_id ==int(visitingOrder[1])):
                    glCallList(pebble.gl_list)        
                if(ar_id ==int(visitingOrder[2])):
                    glCallList(pebble.gl_list)        

        if(ar_id ==10):
                glCallList(crow.gl_list)	#render crow
        glPopMatrix()

########################################################################

if __name__ == "__main__":
        main()

        
