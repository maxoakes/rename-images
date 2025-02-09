import datetime
from PIL import Image
import webcolors

class Analyze:

    def get_web_color(rgb,colorList):
        min_colors = {}
        for key, name in colorList:
            rCSS, gCSS, bCSS = webcolors.hex_to_rgb(key)
            rd = (rCSS - rgb[0]) ** 2
            gd = (gCSS - rgb[1]) ** 2
            bd = (bCSS - rgb[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def get_average_color(image: Image):
        detail = 5 #int, the smaller, the better, but slower to process
        im = image.convert('RGB') #standardize images do they can be processed by this file
        width, height = image.size
        r, g, b = 0, 0, 0
        count = 0
        #print('INFO: Processing '+f) #info, for debug
        for x in range(0, width-1,detail): #loop through each pixel, get totals
            for y in range(0, height-1,detail):
                pixel = im.getpixel((x,y))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
                count += 1
        r = int(r/count)
        g = int(g/count)
        b = int(b/count)
        
        print('R:'+str(r)+' G:'+str(g)+' B:'+str(b))
        return (r,g,b)

    def get_median_color(image: Image):
        detail = 5 #int, the smaller, the better, but slower to process
        im = image.convert('RGB') #standardize images do they can be processed by this file
        width, height = image.size
        r, g, b = 0, 0, 0
        #print('INFO: Processing '+f) #info, for debug
        count = 0
        for x in range(0, width-1,detail): #loop through each pixel, get totals
            for y in range(0, height-1,detail):
                pixel = im.getpixel((x,y))
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
                count += 1
        
        r = int(r/count)
        g = int(g/count)
        b = int(b/count)
        
        #print('R:'+str(r)+' G:'+str(g)+' B:'+str(b))
        return (r,g,b)

    def get_highest_count_color(image: Image, detail=4, rounding=15) -> str:
        try:
            im = image.convert('HSV')
            width, height = image.size
            counts: dict[(int,int,int), int] = {}
            for x in range(0, width-1,detail):
                for y in range(0, height-1,detail):
                    (h,s,v) = im.getpixel((x,y))
                    mod_value = (rounding*round(h/rounding), rounding*round(s/rounding), rounding*round(v/rounding))
                    key = f'{format(mod_value[0],"02x")}{format(mod_value[1],"02x")}{format(mod_value[2],"02x")}'
                    if key in counts:
                        counts[key] = counts[key] + 1
                    else:
                        counts[key] = 1
            
            # import json
            # import datetime
            # with open(f'{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")}.json', 'w') as fp:
            #     json.dump(counts, fp, indent=2)
        
            s = sorted(((v,k) for k,v in counts.items()))
            return f'{s[-1][1]}.{s[-2][1]}'
        except:
            return f"unknown.{datetime.datetime.now().timestamp()}"
        
        
