import random
import os
from PIL import Image,ImageFont,ImageDraw


def random_code(lenth=4):
    vcode_str='0123456789'
    return ''.join(random.sample(vcode_str,lenth))

def random_color(s=0,e=255):
    return random.randint(s,e),random.randint(s,e),random.randint(s,e)

def random_vcode(lenth=4,width=160,height=40,size=28):
    image=Image.new('RGB',(width,height),(255,255,255))
    file_path=os.path.dirname(os.path.abspath(__file__))
    font=ImageFont.truetype(f'{file_path}/BASKVILL.TTF',size=size)
    draw=ImageDraw.Draw(image)
    for x in range(0,width,2):
        for y in range(height):
            draw.point((x,y),fill=random_color(56,255))
    code=random_code()
    for i in range(lenth):
        draw.text((40*i+5,5),code[i],font=font,fill=random_color(65,107))
    return image,code


if __name__=='__main__':
    image,code=random_vcode()
    with open('test.jpg','wb') as f:
        image.save(f)
