import typing

import os
import sys
import webbrowser

import tkinter
import tkinter.font
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk

import adofaiParser

PosType = typing.Dict[str, int]
ElementType = typing.Tuple[tkinter.Widget, PosType]

def Pos(x: int = 0, y: int = 0, width: int = 0, height: int = 0, anchor: str = '') -> PosType:
    pos: PosType = {}

    if x != 0: pos['x'] = x
    if y != 0: pos['y'] = y
    if width != 0: pos['width'] = width
    if height != 0: pos['height'] = height
    if anchor != '': pos['anchor'] = anchor

    return pos

def Font(family, size):
    return tkinter.font.Font(family=family, size=size)

class UI:
    def __init__(self):
        self.Elements: typing.List[ElementType] = []
        self.adofaiFileName: str = ''

        self.BuildWindow()
        self.InitStrings()
        self.BuildElements()
        self.PlaceElements()

    def BuildWindow(self):
        self.window = tkinter.Tk()

        self.window.title("Magicshape with Free angle v0.1.0a")
        self.window.geometry("640x360")
        self.window.resizable(False, False)

        def closeWindow(event):
            self.window.withdraw()
            sys.exit()
            
        self.window.bind('<Escape>', closeWindow)
    
    def InitStrings(self):
        self.style = tkinter.StringVar()
        self.BPM = tkinter.StringVar()
        self.Log = tkinter.StringVar()

        self.style.set("styleDefault")
        self.BPM.set("bpmBPM")
        self.Log.set('')
    
    def BuildLabel(self, text: str, font: tkinter.font.Font, pos: PosType, parent: tkinter.Widget=None, *, var: tkinter.StringVar=None) -> tkinter.Label:
        label = tkinter.Label(parent if parent else self.window, text=text, height=3, font=font, textvariable=var)
        self.Elements.append((label, pos))
        return label
    
    def BuildEntry(self, pos: PosType, parent: tkinter.Widget=None):
        entry = tkinter.Entry(parent if parent else self.window)
        self.Elements.append((entry, pos))
        return entry
    
    def BuildButton(self, text: str, command: typing.Callable[[], None], pos: PosType, parent: tkinter.Widget=None) -> tkinter.Button:
        button = tkinter.Button(parent if parent else self.window, text=text, command=command, bg='#dfdfdf')
        self.Elements.append((button, pos))
        return button
    
    def BuildFrame(self, text: str, pos: PosType, parent: tkinter.Widget=None) -> tkinter.LabelFrame:
        frame = tkinter.LabelFrame(parent if parent else self.window, text=text, relief=tkinter.GROOVE, bd=2)
        self.Elements.append((frame, pos))
        return frame
    
    def BuildRadioButton(self, text: str, variable: tkinter.StringVar, value: int, pos: PosType, parent: tkinter.Widget=None, *, command=None) -> tkinter.Radiobutton:
        radio = tkinter.Radiobutton(parent if parent else self.window, text=text, variable=variable, value=value, anchor='w', command=command)
        self.Elements.append((radio, pos))
        return radio

    def BuildProgressBar(self, pos: PosType, parent: tkinter.Widget=None) -> tkinter.ttk.Progressbar:
        progress = tkinter.ttk.Progressbar(parent if parent else self.window, length=550)
        self.Elements.append((progress, pos))
        return progress

    def BuildElements(self):
        self.BuildLabel("마법진 승수 프로그램", Font("Arial", 20), Pos(200, 0))
        fileNameEntry = self.BuildEntry(Pos(60, 100, 400, 30))

        def onClickBrowseButton():
            adofaiFileName = tkinter.filedialog.askopenfilename(
                initialdir="/",
                title="Select file",
                filetypes=(
                    ("adofai files", "*.adofai"),
                )
            )

            fileNameEntry.delete(0, "end")
            fileNameEntry.insert(0, adofaiFileName)
            self.adofaiFileName = adofaiFileName

        self.BuildButton("Browse...", onClickBrowseButton, Pos(490, 100, 100, 30))

        StyleFrame = self.BuildFrame("소용돌이 형식", Pos(75, 150, 150, 100))
        
        self.BuildRadioButton("기본(소용돌이 X)", self.style, "styleDefault", Pos(0, 5), StyleFrame)
        self.BuildRadioButton("내각", self.style, "styleInner", Pos(0, 30), StyleFrame)
        self.BuildRadioButton("외각", self.style, "styleOuter", Pos(0, 55), StyleFrame)

        BPMFrame = self.BuildFrame("BPM 형태", Pos(245, 150, 200, 100))

        BPMEntry = self.BuildEntry(Pos(60, 18, 80, 20), BPMFrame)

        def enableEntry():
            BPMEntry.configure(state="normal")
            BPMEntry.update()

        def disableEntry():
            BPMEntry.configure(state="disabled")
            BPMEntry.update()

        self.BuildRadioButton("BPM", self.BPM, "bpmBPM", Pos(0, 15), BPMFrame, command=enableEntry)
        self.BuildRadioButton("승수", self.BPM, "bpmMultiply", Pos(0, 40), BPMFrame, command=disableEntry)
        self.BuildLabel("BPM", Font("Arial", 10), Pos(150, 0), BPMFrame)

        progress = self.BuildProgressBar(Pos(50, 280))

        def Run():
            fileName = fileNameEntry.get()
            isBPM = self.BPM.get() == "bpmBPM"
            bpm = BPMEntry.get()

            if not fileName or not os.path.isfile(fileName):
                tkinter.messagebox.showerror("error", "파일을 선택해주세요!")
                return
            
            if isBPM and not bpm.isdigit():
                tkinter.messagebox.showerror("error", "BPM을 숫자로 입력해주세요!")
                return
            
            def logger(log: str):
                self.Log.set(log)
                progress.step(20)
            
            try:
                adofaiParser.run(fileName, isBPM, bpm, self.style.get(), logger)
            except adofaiParser.ParseException as Error:
                tkinter.messagebox.showerror("error", str(Error))
            except Exception as Error:
                tkinter.messagebox.showerror("fatal", f"예상치못한 오류가 발생했습니다.\n{Error}")
            finally:
                progress.stop()
                self.Log.set('')

        self.BuildButton("실행!", Run, Pos(470, 150, 100, 100))
        self.window.bind('<Return>', lambda event: Run())

        self.BuildLabel('', Font('Arial', 10), Pos(50, 320), var=self.Log)
        copyright = self.BuildLabel('Copyright (c)', Font("Arial", 15), Pos(450, 320))
        copyright.bind('<Button-1>', lambda e: webbrowser.open_new(''))
    
    def PlaceElements(self):
        for Element in self.Elements:
            Element[0].place(**Element[1])

    def start(self):
        self.window.mainloop()
