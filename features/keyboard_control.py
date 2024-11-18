import time
import pyautogui
from features.expressions import ExpressionEnum

def press_keys(expression):
    key_mapping = {
        ExpressionEnum.Happy: 'a',
        ExpressionEnum.Neutral: 'b',
        ExpressionEnum.Shocked: 'c',
        ExpressionEnum.Angry: 'd',
        ExpressionEnum.Shy: 'e',
        ExpressionEnum.Excited: 'f',
        ExpressionEnum.Laugh: 'g',
        ExpressionEnum.Sad: 'h'
    }

    if expression in key_mapping:
        key = key_mapping[expression]

        pyautogui.keyDown('ctrlright')
        time.sleep(0.05)
        pyautogui.keyDown('shiftleft')
        time.sleep(0.05)
        pyautogui.keyDown(key)
        time.sleep(0.05)
    else:
        print(f"No mapping found for expression: {expression}")

def release_keys(expression):
    key_mapping = {
        ExpressionEnum.Happy: 'a',
        ExpressionEnum.Neutral: 'b',
        ExpressionEnum.Shocked: 'c',
        ExpressionEnum.Angry: 'd',
        ExpressionEnum.Shy: 'e',
        ExpressionEnum.Excited: 'f',
        ExpressionEnum.Laugh: 'g',
        ExpressionEnum.Sad: 'h'
    }

    if expression in key_mapping:
        key = key_mapping[expression]
        # Release the keys
        pyautogui.keyUp('ctrlright')
        time.sleep(0.05)
        pyautogui.keyUp('shiftleft')
        time.sleep(0.05) 
        pyautogui.keyUp(key)
        time.sleep(0.05)
    else:
        print(f"No mapping found for expression: {expression}")
