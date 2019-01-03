import h5py
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import json
import subprocess
import pandas as pd


def test():
    with h5py.File('fashon_parsing_data.mat', 'r') as file:
        print(list(file.keys()))
        # print(file)
        # ['#refs#', 'all_category_name', 'all_colors_name', 'fashion_dataset']

        for each in file.keys():
            try:
                
                data = file.get(each) # Get a certain dataset
                data = np.array(data)
                print(data)
            
                print(file[each])
                print(file[each][0])
                print(file[each][0][0])

                for every in file[each][0]:
                    st = every
                    obj = file[st]
                    str1 = ''.join(chr(i) for i in obj)
                    print(str1)
            except Exception as e:
                print(e)

        data = file.get('fashion_dataset/segmentation') # Get a certain dataset
        data = np.array(data)
        print(data)
        
        print(file['fashion_dataset'])
        print(file['fashion_dataset'][0])
        print(file['fashion_dataset'][0][0])
        # ['category_label', 'color_label', 'img_name', 'segmentation']
        for every in file['fashion_dataset'][0]:
            st = every
            obj = file[st]
            for i in obj:
                print(i)
        print(file[file['fashion_dataset'][0][0]])
        print(file['fashion_dataset'][0, 0])
        struArray = file['fashion_dataset']
        print(len(struArray))
        print(struArray[0, 0])  # this is the HDF5 reference
        print(file[struArray[0, 0]]['category_label'])  # this is the actual data
        print(file[struArray[0, 0]]['color_label'])  # this is the actual data
        print(file[struArray[0, 0]]['img_name'])  # this is the actual data
        print(file[struArray[0, 0]]['segmentation'])  # this is the actual data
        
        
def hdf5_to_list(data):
    x = data[:]
    #x = x.tolist()
    return x

        
def read_mat(annotation_file_path):
    fashion_dataset = []

    with h5py.File(annotation_file_path, 'r') as file:
        print(list(file.keys()))
        # print(file)
        # ['#refs#', 'all_category_name', 'all_colors_name', 'fashion_dataset']
        fashion_data = file['fashion_dataset']
        # ['category_label', 'color_label', 'img_name', 'segmentation']

        for each in tqdm(fashion_data):
            temp = []
            temp.append(hdf5_to_list(file[each[0]]['category_label']))
            temp.append(hdf5_to_list(file[each[0]]['color_label']))
            temp.append(hdf5_to_list(file[each[0]]['img_name']))
            temp.append(hdf5_to_list(file[each[0]]['segmentation']))
            fashion_dataset.append(temp)

    return fashion_dataset
    
    
def convert_mat_to_dict(mat_file='fashon_parsing_data.mat'):
    f = h5py.File(mat_file, 'r')
    all_ctgs = get_all_ctgs(f)
    iter_ = iter(f.get('#refs#').values())
    df = pd.DataFrame()
    for outfit in tqdm(iter_, total=len(f.get('#refs#'))):
        try:
            # img_name
            ascii_codes = list(outfit.get('img_name').value[:,0])
            img_name = ''.join([chr(code) for code in ascii_codes ])
            print(img_name)
            
            # super pix 2 category
            spix2ctg = outfit.get('category_label').value[0]
            #pd.Series(spix2ctg).value_counts().plot(kind='bar')
            #print(spix2ctg.shape)
            #plt.plot(spix2ctg)
            #plt.show()
            
            # super pix 2 color
            spix2clr = outfit.get('color_label').value[0]
            #print(spix2clr.shape)
            #plt.plot(spix2clr)
            #plt.show()

            # super pix
            spixseg = outfit.get('segmentation').value.T
            #print(spixseg.shape)
            # plt.imshow(spixseg)
            #plt.plot(spixseg)
            #plt.show()
            # plt.savefig('image.png')

            # super pix -> semantic segmentation
            semseg = np.zeros(spixseg.shape)
            for i, c in enumerate(spix2ctg):
                semseg[spixseg == i] = c-1

            # semseg -> bbox
            items = []
            for i, ctg in enumerate(all_ctgs):
                region = np.argwhere(semseg == i)
                if region.size != 0:
                    bbox = {
                        'ymin':int(region.min(0)[0]),
                        'xmin':int(region.min(0)[1]),
                        'ymax':int(region.max(0)[0]),
                        'xmax':int(region.max(0)[1]),
                    }
                    items.append({
                        'bbox': bbox,
                        'category': ctg,
                    })

            df = df.append({
                'img_name': img_name,
                'category_label': category_label,
                'color_label': color_label,
                'segmentation': segmentation,
                'items': items,
            }, ignore_index=True)
        except AttributeError:
            pass

    d = df.to_dict(orient='records')
    return d
    
    
def get_all_ctgs(h5pyfile):
    refs = h5pyfile.get('all_category_name').value[0]
    all_ctgs = []
    for ref in refs:
        ctg = ''.join([chr(c) for c in h5pyfile[ref].value])
        all_ctgs.append(ctg)
    return all_ctgs
    

# fashion_dataset = read_mat('fashon_parsing_data.mat')
# print(len(fashion_dataset))
# print(len(fashion_dataset[0]))
# print(len(fashion_dataset[0][0]), len(fashion_dataset[0][0][0]))
# print(len(fashion_dataset[0][1]), len(fashion_dataset[0][1][0]))
# print(len(fashion_dataset[0][2]), len(fashion_dataset[0][2][0]))
# print(len(fashion_dataset[0][3]), len(fashion_dataset[0][3][0]))
# plt.plot(fashion_dataset[0][3])
# plt.show()

make_bbox_json()

