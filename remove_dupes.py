import glob
import os

"""
/parent_folder
    | -- img_folder and/or label_folder
        | -- img**.jpg
        | -- label**.txt
    | -- remove_dupes.py
    
"""


def remove_dupes():
    img_folder = 'obj'
    label_folder = 'obj'

    done = False

    while not done:
        imgls_filename = glob.glob(f'{img_folder}/*.jpg')
        labells_filename = glob.glob(f'{label_folder}/*.txt')

        count = 0
        del_list = []

        print('\n<< Dupes found: >>')
        if len(imgls_filename) >= len(labells_filename):
            for i in range(len(imgls_filename)):
                img_index_name_short = imgls_filename[i][len(img_folder)+1:-4]
                img_index_name = f'{label_folder}\{img_index_name_short}.txt'

                if img_index_name not in labells_filename:
                    del_list.append(f'{img_folder}\{img_index_name_short}.jpg')
                    print(f"{count+1}. {del_list[count]}")
                    count += 1

        elif len(imgls_filename) < len(labells_filename):
            for i in range(len(labells_filename)):
                img_index_name_short = labells_filename[i][len(
                    label_folder)+1:-4]
                img_index_name = f'{img_folder}\{img_index_name_short}.jpg'

                if img_index_name not in imgls_filename:
                    del_list.append(
                        f'{label_folder}\{img_index_name_short}.txt')
                    print(f"{count+1}. {del_list[count]}")
                    count += 1

        print(f"\nDiff: {len(del_list)}")
        print(f"{len(imgls_filename) = }")
        print(f"{len(labells_filename) = }")

        done = abs(len(imgls_filename) - len(labells_filename)
                   ) == len(del_list) and len(del_list) == 0

        if not done:
            print('\nDelete duplicate? (Y/n)')
            opt = input('>> ')

            if opt == 'Y':
                for item in del_list:
                    os.remove(item)
            else:
                print('Cancelled, nothing done')
        else:
            print("No more dupes found!")


if __name__ == '__main__':
    remove_dupes()
