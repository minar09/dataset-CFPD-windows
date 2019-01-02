import h5py
import numpy as np

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
    print(struArray[0, 0])  # this is the HDF5 reference
    print(file[struArray[0, 0]]['segmentation'])  # this is the actual data
    print(file[struArray[0, 0]]['segmentation'][0])  # this is the actual data
    print(file[struArray[0, 0]]['segmentation'].value)  # this is the actual data
