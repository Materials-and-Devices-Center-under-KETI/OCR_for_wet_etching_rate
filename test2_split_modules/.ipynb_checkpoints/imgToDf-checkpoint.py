import pandas as pd
import pyautogui
import pytesseract
import datetime as dt

today = str(dt.datetime.now()).split(' ')[0]

def mergeDfs(dfs):
    return pd.concat([df for df in dfs])

def savePNG(root, frame, name): # get a file name as an input
    screenshot = pyautogui.screenshot(region=getTargetRegion(root, frame)) # must concern the aread inside the transparent frame
    screenshot.save(f'data/{today}/img_{name}.png')
    print(f'{name}.png saved') # change a color of button
    
def readNumbers(img):
    numbers = pytesseract.image_to_string(img, config=custom_config)
    return numbers

def topNumbersToDf(numbers):
    n_row = len(numbers.split('\n')) - 1
    rows = []
    for elem in numbers.split('\n'):
        rows.append(elem.split(' '))
    df_top = pd.DataFrame(rows[:n_row], columns=['W2','W1','C','E1','E2'])
    df_top['cm'] = [5+i for i in range(len(df_top))]
    df_top.set_index('cm', inplace=True)
    return df_top
    
def bottomNumbersToDf(start,numbers):
    n_row = len(numbers.split('\n')) - 1
    rows = []
    for elem in numbers.split('\n'):
        # rows.insert(0, elem.split(' ')) # insert a new to the top
        rows.append(elem.split(' '))
    df_bottom = pd.DataFrame(rows[:n_row], columns=['E2','E1','C','W1','W2']) # inverse order
    df_bottom = df_bottom.iloc[:,np.arange(len(df_bottom.columns)-1,-1,-1).tolist()] # reverse
    df_bottom['cm'] = [start+1+i for i in range(len(df_bottom))]
    df_bottom.set_index('cm', inplace=True)
    return df_bottom

def topPointNumbersToDf(numbers): # need to get position in cm
    n_row = len(numbers.split('\n')) - 1
    rows = []
    for elem in numbers.split('\n'):
        rows.append(elem.split(' '))
    df_top = pd.DataFrame(rows[:n_row], columns=['W2','W1','C','E1','E2'])
    df_top = df_top.astype(float)
    return pd.concat([df_top, df_top.agg(['count', 'min', 'max', 'mean', 'std'])]).round(3)
    
def bottomPointNumbersToDf(numbers):
    n_row = len(numbers.split('\n')) - 1
    rows = []
    for elem in numbers.split('\n'):
        # rows.insert(0, elem.split(' ')) # insert a new to the top
        rows.append(elem.split(' '))
    df_bottom = pd.DataFrame(rows[:n_row], columns=['E2','E1','C','W1','W2']) # inverse order
    df_bottom = df_bottom.iloc[:,np.arange(len(df_bottom.columns)-1,-1,-1).tolist()] # reverse
    df_bottom = df_bottom.astype(float)
    return pd.concat([df_bottom, df_bottom.agg(['count', 'min', 'max', 'mean', 'std'])]).round(3)

def preciseTopNumbersToDf(numbers):
    n_row = len(numbers.split('\n')) - 1
    rows = []
    for elem in numbers.split('\n'):
        rows.append(elem.split(' '))
    df_top = pd.DataFrame(rows[:n_row], columns=['W2','W1','C','E1','E2'])
    df_top['cm'] = [5+0.25*i for i in range(len(df_top))]
    df_top.set_index('cm', inplace=True)
    return df_top
    
def preciseBottomNumbersToDf(numbers):
    n_row = len(numbers.split('\n')) - 1
    rows = []
    for elem in numbers.split('\n'):
        # rows.insert(0, elem.split(' ')) # insert a new to the top
        rows.append(elem.split(' '))
    df_bottom = pd.DataFrame(rows[:n_row], columns=['E2','E1','C','W1','W2']) # inverse order
    df_bottom = df_bottom.iloc[:,np.arange(len(df_bottom.columns)-1,-1,-1).tolist()] # reverse
    df_bottom['cm'] = [16-0.25*i for i in range(len(df_bottom))]
    df_bottom.set_index('cm', inplace=True)
    df_bottom = df_bottom.sort_index() # sort df by index
    return df_bottom