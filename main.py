from PIL import Image
import os
import sys

from Analyze import Analyze

sig_char = 'A'

def main():
    
    base_path: str

    #standard parameter checking
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
        os.chdir(base_path)
    else:
        print('image.py: No directory specified, using working directory!')
        base_path = os.getcwd()
        return

    ext_list = ['.bmp','.jpg','.jpeg','.png'] #change list as needed
    
    for subdir, dirs, files in os.walk(base_path):
        for this_file in files:
            curr_path = os.path.join(subdir, this_file)
            is_valid_image_type = os.path.splitext(curr_path)[1].lower() in ext_list
            has_been_processed = isNameProcessed(this_file)
            if (not is_valid_image_type) or has_been_processed:
                print(f'Skipping: Valid:{is_valid_image_type}, Processed:{has_been_processed}')
                continue

            filepath = os.path.join(base_path, curr_path)
            image = Image.open(filepath)
            hsv_hex = Analyze.get_highest_count_color(image)
            
            ext = image.format.lower()
            
            same_color_name_counter = 0
            output = f'{hsv_hex}.{same_color_name_counter}.{sig_char}.{ext}'

            while os.path.exists(rf'{subdir}\{output}'):
                same_color_name_counter = same_color_name_counter + 1
                output = f'{hsv_hex}.{same_color_name_counter}.{sig_char}.{ext}'

            output_path = os.path.join(subdir, output)
            if not os.path.exists(output):
                try:
                    os.rename(curr_path, output_path)
                    print(f'Renamed: {curr_path} -> {output_path}')
                except Exception as ex:
                    print(f'\tUnexpected error naming {output}: {ex}') #something weird happens if we get here
            else:
                print(f'\tError: {output} already exists') #this shouldn't happen due to the iteration of the filename

def isNameProcessed(filename: str):
    valid_sigs = ['A']
    return filename[filename.rfind('.') - 1] in valid_sigs

if __name__ == '__main__':
    main()