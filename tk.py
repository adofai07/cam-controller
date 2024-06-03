from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import wmi
import ctypes
import pyautogui
import time
import speech_recognition as sr
import tkinter as tk
from pynput.mouse import Button, Controller


class COMPUTER:
    def __init__(self):
        self.volume = 0.0
        self.brightness = 50

        self.mouse = Controller()
        self.recognizer = sr.Recognizer() # Recognizer 객체 생성
        
        root = tk.Tk()
        root.withdraw()  # 화면에 Tk 창을 표시하지 않음
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        window_manager = wmi.WMI(namespace='wmi')
        self.brightness_manager = window_manager.WmiMonitorBrightnessMethods()[0]
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_manager = cast(interface, POINTER(IAudioEndpointVolume))

        #초기화 (밝기 50, 음성 0.0)
        
        self.set_system_volume(self.volume)
        self.set_brightness(self.brightness)


    def set_brightness(self,level):
        # 밝기 설정
        self.brightness_manager.WmiSetBrightness(level, 0)
    
    def set_system_volume(self,level):
        # 음소거 해제
        self.volume_manager.SetMute(0, None)
        # 볼륨 설정
        self.volume_manager.SetMasterVolumeLevelScalar(level, None)
    
    def volume_up(self):
        if self.volume >= 1.0:
            self.volume =1.0
            self.set_system_volume(self.volume)
            return False, "최대 볼륨을 넘어 볼륨이 증가하지 않음"
        self.volume += 0.1
        self.set_system_volume(self.volume)
        return True, f"볼륨이 {self.volume}으로 설정됨"
    
    def volume_down(self):
        if self.volume <= 0.0:
            self.volume =0.0
            self.set_system_volume(self.volume)
            return False, "최소 볼륨을 넘어 볼륨이 감소하지 않음"
        self.volume -= 0.1
        self.set_system_volume(self.volume)
        return True, f"볼륨이 {self.volume}으로 설정됨"
    
    def brightness_up(self):
        if self.brightness >= 100:
            self.brightness =100
            self.set_brightness(self.brightness)
            return False, "최대 밝기를 넘어 밝기가 증가하지 않음"
        self.brightness += 10
        self.set_brightness(self.brightness)
        return True, f"밝기가 {self.brightness}으로 설정됨"
    
    def brightness_down(self):
        if self.brightness <= 0:
            self.brightness =0
            self.set_brightness(self.brightness)
            return False, "최소 밝기를 넘어 밝기가 감소하지 않음"
        self.brightness -= 10
        self.set_brightness(self.brightness)
        return True, f"밝기가 {self.brightness}으로 설정됨"

    def window_lock(self):
        ctypes.windll.user32.LockWorkStation()
        return True, "컴퓨터 잠금"

    def toggle_windows(self):
        pyautogui.hotkey('win', 'd')
        return True, "윈도우 창 모두 닫기"

    def switch_to_left(self):
        pyautogui.hotkey('ctrl', 'win', 'left')
        return True, "왼쪽으로 화면전환"

    def switch_to_right(self):
        pyautogui.hotkey('ctrl', 'win', 'right')
        return True, "오른쪽으로 화면전환"

    def move_mouse(self,x_ratio, y_ratio):
        self.mouse.position = (self.screen_width * x_ratio, self.screen_height * y_ratio)
        self.mouse.click(Button.left, 1)

    def type_text(self,text):
        # 입력 언어를 영어(미국)로 설정하기
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        KLF_SETFORPROCESS = 0x00000100
        HWND_TOP = 0
        HKL_NEXT = 1
        # 0x0409: English (United States) layout
        layout_id = user32.LoadKeyboardLayoutW("00000409", KLF_SETFORPROCESS)
        if layout_id == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        # Set the layout for the current thread
        result = user32.ActivateKeyboardLayout(layout_id, 0)
        if result == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        
        pyautogui.write(text, interval=0.1)  # 각 글자 사이에 0.1초 간격을 두고 입력

    
    def audio_to_search(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("음성을 말하세요:")
                    audio = self.recognizer.listen(source)
                
                text = self.recognizer.recognize_google(audio, language="en-US")
                break
            except:
                time.sleep(1.0)
                print('다시',end=' ')
        print(text)

        
        self.move_mouse(0.02,1.0)
        # 예제 실행
        time.sleep(0.6)  # 2초 대기하여 사용자가 준비할 시간을 줍니다
        self.type_text('chrome')
        
        pyautogui.press('enter')
        time.sleep(1.2)

        self.move_mouse(0.27,0.85)
        
        pyautogui.press('f6')
        self.type_text(str(text))
        pyautogui.press('enter')
        time.sleep(1.2)
        
        pyautogui.press('f11')
        
        time.sleep(1.2)

        self.move_mouse(0.3,0.2)
        
        time.sleep(1.2)
        
        pyautogui.press('f11')