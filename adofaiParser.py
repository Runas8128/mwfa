import json

import parseHelper
from parseHelper import Callable, Union, List, Dict
from parseHelper import PathType, EventType, SettingType, MapType
from parseHelper import ParseException, ExpectedParseException

def dataToAngle(data: PathType) -> List[int]:
    if isinstance(data, str):
        try:
            data = [parseHelper.angleForPath[path] for path in parseHelper.fixPath(data)]
        except KeyError:
            raise ExpectedParseException("알 수 없는 pathData입니다.\n")

    try:
        return [(data[i] - data[i-1]) % 360 for i in range(1, len(data))]
    except TypeError:
        raise ExpectedParseException("알 수 없는 pathData 혹은 angleData입니다.\n")

def makeBPMMuls(beats: List[int], style: str) -> List[int]:
    if style == 'styleDefault':
        return parseHelper.makeBPMDefault(beats)
    
    elif style == 'styleInner':
        return parseHelper.makeBPMInner(beats)
    
    elif style == 'styleOuter':
        return parseHelper.makeBPMOuter(beats)

    else:
        raise ParseException("알 수 없는 소용돌이 형식입니다.\n")

def mulToBPM(muls: List[int], BPM: int) -> List[int]:
    pass

def delSppeed(Map: MapType) -> MapType:
    return Map

def addSpeed(Map: MapType, Speeds: List[EventType]) -> MapType:
    return Map

def run(fileName: str, isBPM: bool, BPM: str, style: str, logger: Callable[[str], None]):
    logger("Loading Map file")
    with open(fileName, 'r') as adofaiFile:
        Map: MapType = json.load(adofaiFile)
    
    # pathData for Hallowen or complementable version
    logger("Loading pathData/angleData")
    data: Union[PathType, None] = Map.get("pathData", Map.get("angleData", None))
    if not data:
        raise ParseException("얼불춤 파일이 아닙니다. 얼불춤 파일을 선택해주세요!")
    
    logger("Caculating needed multipliers")
    Multipliers = makeBPMMuls(dataToAngle(data), style)
    if isBPM:
        Multipliers = mulToBPM(Multipliers, int(BPM))
    
    logger("Making new map")
    newMap = addSpeed(delSppeed(Map), Multipliers)
    
    logger("dump new map")
    with open(fileName[:-7] + '_Magic.adofai', 'w') as newFile:
        json.dump(newMap, newFile)
