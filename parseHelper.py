from typing import Callable, Union, List, Dict

PathType = Union[str, List[Union[int, float]]]
SettingType = Dict[str, Union[int, str, bool]]
EventType = Dict[str, Union[int, str, float]]

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

class ParseException(Exception):
    pass

class UnExpectedParseException(ParseException):
    def __init__(self, err: str):
        super().__init__(err + '디스코드에 루나스#5980으로 해당 오류를 제보해주시기 바랍니다')

class ExpectedParseException(UnExpectedParseException):
    def __init__(self, err: str, suggest: str):
        super().__init__(err + suggest + '한 후에도 오류가 지속된다면 ')

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

def SpeedEvent(floor: int, mul: float) -> EventType:
    return { "floor": floor, "eventType": "SetSpeed", "speedType": "Multiplier", "beatsPerMinute": 100, "bpmMultiplier": mul }

def Twirl(floor: int) -> EventType:
    return { "floor": floor, "eventType": "Twirl" }

def makeTwirl(Map: MapType, isInner: bool) -> MapType:
    actions: List[EventType] = [action for action in Map['actions'] if action["eventType"] != "Twirl"]
    angles: List[float] = []
    isTwirl: bool = False
    pred: Callable[[float], bool] = (lambda diff: diff > 180) if isInner else (lambda diff: diff < 180)
    
    if "pathData" in Map:
        try:
            angles = [angleForPath[path] for path in fixPath(Map["pathData"])][:]
        except KeyError: # From angleForPath dict
            raise ExpectedParseException("알 수 없는 pathData입니다.\n", ".adofai파일을 다시 확인")
    else:
        angles = Map["angleData"][:]
    
    for idx in range(1, len(angles)):
        if angles[idx - 1] == 999:
            continue

        diff = (angles[idx] - angles[idx - 1]) % 360
        
        if isTwirl:
            diff = 360 - diff
        
        if pred(diff):
            actions.append(Twirl(idx))
            isTwirl = not isTwirl

    Map["actions"] = actions
    return Map
