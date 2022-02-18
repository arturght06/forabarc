import barcode, os
import os.path
 
from barcode.writer import ImageWriter

def decoder(name, barcode_init):
    directory = 'barcoder/'
    ean = barcode.get('ean13', barcode_init, writer=ImageWriter())
    check_file = os.path.exists(directory + name + '.gif') # True
    if check_file == False:
        ean.save(directory + name)
        os.rename( directory + name + '.png', directory + name + '.gif')
        return str(directory + name + '.gif')
    return str(directory + name + '.gif')





