import pygame

class inventoryManage:
    def __init__(self):
        self.inventory = [
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None]
        ] #기본 인벤토리 텅 빈거

    def itemManager(self):
        domeItem = {
            "name": "돔 설치 도구",
            "image": "pics/UI/items/DomeItem.png",
            "placeimage": "pics/buildings/domeBuilding1.png",
            "IsBuilding": True,
            "IsSeed": False,
            "IsFood": False,
            "foodValue": None,
            "placeType": "dome",
            "description": "돔 설치 도구\n\n돔을 건설할 수 있는 아이템입니다.\n원하는 위치에 클릭하여 기지를 건설하세요.",
            "count": 1
        }
        
        potato = {
            "name": "감자",
            "image": "pics/UI/items/potatoItem.png",
            "placeimage": None,
            "IsBuilding": False,
            "IsSeed": False,
            "IsFood": True,
            "foodValue": 10,
            "placeType": None,
            "description": "감자\n\n탄수화물이 풍부해 생존에 아주 적합한 음식\n성장속도가 빨라 대량생산이 가능해서 최적이다.\n\n섭취시 포만감: 10",
            "count": 1
        }

        potatoSeed = {
            "name": "감자 씨앗",
            "image": "pics/UI/items/potatoSeed.png",
            "placeimage": "pics/plant/potato",
            "IsBuilding": False,
            "IsSeed": True,
            "IsFood": False,
            "foodValue": None,
            "placeType": "potato",
            "description": "감자 씨앗\n\n감자는 고온다습한 환경을 제외하면 잘자라고\n성장속도가 빨라 대량생산이 가능합니다.\n\n화성에 흙에 심을 순 없지만 온실엔 심을 수 있습니다.",
            "count": 1
        }