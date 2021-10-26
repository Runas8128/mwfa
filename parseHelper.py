from typing import Callable, Union, List, Dict

PathType = Union[str, List[int]]
SettingType = Dict[str, Union[int, str, bool]]
EventType = Dict[str, Union[int, str]]

MapType = Dict[str, Union[PathType, SettingType, List[EventType]]]

angleForPath: Dict[str, Union[int, float]] = {
    'R':   0, 'p':  15, 'J':  30, 'E':  45, 'T':  60, 'o':  75,
    'U':  90, 'q': 105, 'G': 120, 'Q': 135, 'H': 150, 'W': 165,
    'L': 180, 'x': 195, 'N': 210, 'Z': 225, 'F': 240, 'V': 255,
    'D': 270, 'Y': 285, 'B': 300, 'C': 315, 'M': 330, 'A': 345,
    
    # Midspin
    '!': 999,

    # Pentagon
    'a': 72, 'b': 144, 'c': 216, 'd': 288, 'e': 360,

    # Heptagon 51.42857, 102.8571, 154.2857, 205.7143, 257.1429, 308.5714, 360
    'f': 51.42857, 'g': 102.8571, 'h': 154.2857, 'i': 205.7143, 'j': 257.1429, 'k': 308.5714, 'l': 360
}

def fixPath(path: str):
    return path\
        .replace('7777777', 'l')\
        .replace('777777', 'k')\
        .replace('77777', 'j')\
        .replace('7777', 'i')\
        .replace('777', 'h')\
        .replace('77', 'g')\
        .replace('7', 'f')\
        .replace('55555', 'e')\
        .replace('5555', 'd')\
        .replace('555', 'c')\
        .replace('55', 'b')\
        .replace('5', 'a')

class ParseException(Exception):
    def __init__(self, err: str):
        self.err = err + '디스코드에 루나스#5980으로 해당 오류를 제보해주시기 바랍니다'
    
    def __str__(self):
        return self.err

class ExpectedParseException(ParseException):
    def __init__(self, err: str):
        super().__init__(err + 'adofai 파일을 다시 확인한 후에도 오류가 지속된다면 ')

def makeBPMDefault(beats: List[int]) -> List[int]:
    pass

def makeBPMInner(beats: List[int]) -> List[int]:
    pass

def makeBPMOuter(beats: List[int]) -> List[int]:
    pass