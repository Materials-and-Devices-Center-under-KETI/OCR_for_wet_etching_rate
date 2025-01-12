import pyautogui
import cv2
import datetime as dt
import pandas as pd

today = str(dt.datetime.now()).split(' ')[0]

def topMeasurement(root, frame):
    screenshot = pyautogui.screenshot(region=getTargetRegion(root, frame))
    ss_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY) # ss stands for screenshot..
    df_top = topNumbersToDf(readNumbers(ss_gray))
    df_top.to_csv(f'data/{today}/top.csv', index=True)
    print('Top saved')

def bottomMeasurement(root, frame):
    screenshot = pyautogui.screenshot(region=getTargetRegion(root, frame))
    ss_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY) # ss stands for screenshot..
    df_top = pd.read_csv(f'data/{today}/top.csv',index_col='cm')
    df_bottom = bottomNumbersToDf(df_top.index[-1],readNumbers(ss_gray))
    df_bottom.to_csv(f'data/{today}/bottom.csv', index=True)
    print('Bottom saved')
    df_merged = mergeDfs([df_top, df_bottom])
    df_merged = df_merged.astype(float)
    df_merged.to_csv(f'data/{today}/top+bottom.csv', index=True)
    print('Top & Bottom merged')
    # draw plots
    drawHeatmap(df_merged,'top+bottom')
    print('2D plot of top & bottom saved')
    draw3DPlot(df_merged,'top+bottom')
    print('3D plot of top & bottom saved')
    
def topPointMeasurement(root, frame): 
    screenshot = pyautogui.screenshot(region=getTargetRegion(root, frame))
    ss_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY) # ss stands for screenshot..
    df_top_point = topPointNumbersToDf(readNumbers(ss_gray))
    df_top_point.to_csv(f'data/{today}/top_point.csv', index=True)
    print('Top point saved')

def bottomPointMeasurement(root, frame): 
    screenshot = pyautogui.screenshot(region=getTargetRegion(root, frame))
    ss_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY) # ss stands for screenshot..
    df_bottom_point = bottomPointNumbersToDf(readNumbers(ss_gray))
    df_bottom_point.to_csv(f'data/{today}/bottom_point.csv', index=True)
    print('Bottom point saved')

def preciseTopMeasurement(root, frame):
    screenshot = pyautogui.screenshot(region=getTargetRegion(root, frame))
    ss_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY) # ss stands for screenshot..
    df_top = preciseTopNumbersToDf(readNumbers(ss_gray))
    df_top.to_csv(f'data/{today}/precise_top.csv', index=True)
    print('Top of precision saved')
    # plot
    drawHeatmap(df_top,'precise_top')
    print('2D plot of top of precision saved')

def preciseBottomMeasurement(root, frame):
    screenshot = pyautogui.screenshot(region=getTargetRegion(root, frame))
    ss_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY) # ss stands for screenshot..
    df_bottom = preciseBottomNumbersToDf(readNumbers(ss_gray))
    df_bottom.to_csv(f'data/{today}/precise_bottom.csv', index=True)
    print('Bottom of precision saved')
    # plot the bottom first
    drawHeatmap(df_bottom,'precise_bottom')
    print('2D plot of bottom of precision saved')    

def getFinalResults(root, frame):
    df_tb = pd.read_csv(f'data/{today}/top+bottom.csv', index_col='cm') # top+bottom
    df_pt = pd.read_csv(f'data/{today}/precise_top.csv',index_col='cm') # precise top
    df_pb = pd.read_csv(f'data/{today}/precise_bottom.csv',index_col='cm') # precise bottom
    df_all = mergeDfs([df_tb, df_pt, df_pb])
    df_all = df_all.groupby('cm').mean() # average out rows having the same index
    df_all.to_csv(f'data/{today}/top+bottom+precision.csv', index=True)
    # plots
    drawHeatmap(df_all,'top+bottom+precision')
    print('2D plot of final data saved')
    draw3DPlot(df_all,'top+bottom+precision')
    print('3D plot of final data saved')