import os
import random
from PIL import Image,ImageFont
import string
from rotate_img import draw_rotated_text
import math
import time
from color_picker import color_fill_tuple


ij = 0
if 'output' in os.listdir(os.getcwd()):  #### create a directory to save the output
     pass
else:   
    os.mkdir('output') 

def random_char(y:int) -> None:
       '''
       This function generates a random characters with the combination of letters numbers and symbols
       '''
       characters =  string.digits
       return ''.join(random.choice(characters) for x in range(y))



def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    #print(text_width, text_height)

    return (text_width, text_height)

def get_rotated_coordinates(xcor, ycor, width, height, rot_ang, line):
    angle_rad = math.radians(-rot_ang)
    sin_angle = math.sin(angle_rad)
    cos_angle = math.cos(angle_rad)

    def rotate_point(point):
        return (
            xcor + (point[0] - xcor) * cos_angle - (point[1] - ycor - 100 if angle_rad < 0 else point[1] - ycor) * sin_angle,
            ycor + (point[0] - xcor) * sin_angle + (point[1] - ycor) * cos_angle
        )

    top_left = (xcor, ycor - 3)
    top_right = (xcor + width + 15, ycor - 3)
    bottom_left = (xcor, ycor + height + 3)
    bottom_right = (xcor + width + 15, ycor + height + 3)

    rotated_top_left = rotate_point(top_left)
    rotated_top_right = rotate_point(top_right)
    rotated_bottom_left = rotate_point(bottom_left)
    rotated_bottom_right = rotate_point(bottom_right)

    final_coord = [rotated_top_left, rotated_top_right, rotated_bottom_right, rotated_bottom_left]
    rect_box = [int(coord) for point in final_coord for coord in point]
    rect_box[0]-= (7+random.randrange(1,3))
    rect_box[-2]-=(7+random.randrange(1,3))

    final_result = f"{str(rect_box).replace('[','').replace(']','')}, {line}"
    return final_result

def create_data(img,x1,x2, y1,y2, imgno,font)-> None:
    '''
    Function that generate data within any location of custom image
    *Parameters*
    - Image: Path of a blank image
    - X1,X2: Starting point of coordinates horizontal
    - Y1,Y2: Starting point of coordinates vertical 
    - imgno: Number of Image
    '''
    fontname=font
    for y in range(0,imgno):
        orig_dir = os.getcwd()
        st = time.time()
        image= Image.open(img) 
        font_path = random.choice([
                                   ImageFont.truetype(fontname,random.randint(50,52))
                                  ])  #### to choose a font randomly
        
        # ImageFont.truetype('fonts/inkjet/MerchantCopy-GOXq.ttf',random.randint(55,60)),
        # ImageFont.truetype('fonts/inkjet/inkjet-regular.ttf',random.randint(55,60))
        
        line1= "Rs." + random_char(random.randint(2,3)) + " (Re " + "0." + random_char(random.randint(2,3)) + "/ml)  " + chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z'))) + random_char(random.randint(4,7)) + chr(random.randint(ord('A'), ord('Z'))) + '/' + random_char(random.randint(1,2)) 
        line2= chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z')))  + " " + random_char(random.randint(4,5)) 
        line3 = chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z'))) + chr(random.randint(ord('A'), ord('Z'))) + " " + random_char(random.randint(4,5))
        # line3 = "MRPRS " + random_char(random.randint(10,12))

        xcor1=random.randint(int(x1),int(x2))
        ycor1=random.randint(int(y1),int(y2))
        xcor2 = xcor1
        ycor2 = ycor1 + random.randint(35,45)
        xcor3 = xcor1 
        ycor3 = ycor2 + random.randint(35,45)
        rot_ang = random.randint(-1,1)
        #print("time0: ", time.time()-st)
        image = draw_rotated_text(image,rot_ang,(xcor1,ycor1),line1,color_fill_tuple,font = font_path)
        image = draw_rotated_text(image,rot_ang,(xcor2,ycor2),line2,color_fill_tuple,font = font_path)
        image = draw_rotated_text(image,rot_ang,(xcor3,ycor3),line3,color_fill_tuple,font = font_path)
       
        name_image_text = str(time.time())
        op_img_name = os.path.join('output',str(name_image_text) + '.jpg')
        op_txt_name = os.path.join('output',str(name_image_text) + '.txt')

    ########=====save image=============#########
        image.save(op_img_name.format(y))
       
    ######## For first Rectangle        
        width1,height1 = get_text_dimensions(line1,font=font_path)    
        final_result1=get_rotated_coordinates(xcor1,ycor1,width1,height1,rot_ang,line1)
     
    ######## For Second Rectangle
        width2,height2 = get_text_dimensions(line2,font = font_path)       
        final_result2=get_rotated_coordinates(xcor2,ycor2,width2,height2,rot_ang,line2)
     
    ######## For Third Rectangle
        width3,height3 = get_text_dimensions(line3,font = font_path)
        final_result3=get_rotated_coordinates(xcor3,ycor3,width3,height3,rot_ang,line3)


        #########
        with open(op_txt_name,'a') as f:
            f.writelines(final_result1)
            f.write('\n')
            f.writelines(final_result2)
            f.write('\n')
            f.writelines(final_result3)
        #######

        print("Time Taken: ", time.time()-st)
        os.chdir(orig_dir)
        
    '''
    ========================================
    give the blank image and adjust the coordinates accordinagly 
    also you need to adjust the fontsize which is in font_path according to needs 
    ========================================
    create_data(image,x1,x2,y1,y2,number_of_image)
      - Image: Path of a blank image
    - X1,X2: Starting point of coordinates horizontal
    - Y1,Y2: Starting point of coordinates vertical 
    - imgno: Number of Image
    =========================================
    '''
# create_data('pink_blank.png',90,100,80,90,1) 
