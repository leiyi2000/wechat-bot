from typing import List, Dict, Tuple

import httpx
import structlog

from bot.schemas import Message
from bot.command import CommandRouter


router = CommandRouter()
log = structlog.get_logger()


def parse_free_game_image(images: List[Dict[str, str]]) -> str:
    filter_type = [
        "Thumbnail",
        "VaultOpened",
        "DieselStoreFrontWide",
        "OfferImageWide",
    ]
    for image in images:
        if image["type"] in filter_type:
            return image["url"] + "?$alias=cloud.jpg"
    return ""


def parse_free_game_date(promotions: Dict | None) -> Tuple[str, str]:
    """解析免费游戏领取的时间范围.

    Args:
        promotions (Dict | None): 促销信息.

    Returns:
        Tuple[str, str]: 开始时间, 结束时间.
    """
    if not promotions:
        return "", ""
    offers = promotions["promotionalOffers"]
    upcoming = promotions["upcomingPromotionalOffers"]
    if offers:
        date = offers[0]["promotionalOffers"][0]
    else:
        date = upcoming[0]["promotionalOffers"][0]
    return date["startDate"][:10], date["endDate"][:10]


def pick_up_link(element: Dict) -> str:
    """解析游戏链接.

    Args:
        element (Dict): 元素信息.

    Returns:
        str: 游戏领取链接.
    """
    if link := element.get("url"):
        return link
    else:
        slugs = (
            [
                x["pageSlug"]
                for x in element.get("offerMappings", [])
                if x.get("pageType") == "productHome"
            ]
            + [
                x["pageSlug"]
                for x in element.get("catalogNs", {}).get("mappings", [])
                if x.get("pageType") == "productHome"
            ]
            + [
                x["value"]
                for x in element.get("customAttributes", [])
                if "productSlug" in x.get("key")
            ]
        )
        return "https://store.epicgames.com/zh-CN{}".format(
            f"/p/{slugs[0]}" if len(slugs) > 0 and slugs[0] else ""
        )


def free_game_message(elements: List[Dict]) -> Message:
    content = ""
    for element in elements:
        try:
            title = element["title"]
            # 未公布的神秘游戏跳过
            if title.startswith("Mystery Game"):
                continue
            description = element["description"]
            discount_price = element["price"]["totalPrice"]["fmtPrice"]["discountPrice"]
            start_date, end_date = parse_free_game_date(element["promotions"])
            link = pick_up_link(element)
            # 拼接消息
            content += f"游戏:\t{title}\n"
            content += f"描述:\t{description}\n"
            content += f"价格:\t{discount_price}\n"
            content += f"时间:\t{start_date} ~ {end_date}\n"
            content += f"领取:\t{link}\n\n\n"
        except Exception as e:
            log.warning(f"free game parse error: {e}")
            continue
    return content.strip()


@router.command("喜加一", event_arg=False)
async def free_game():
    async with httpx.AsyncClient() as client:
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
        params = {
            "locale": "zh-CN",
            "country": "CN",
            "allowCountries": "CN",
        }
        response = await client.get(url, params=params)
    elements = response.json()["data"]["Catalog"]["searchStore"]["elements"]
    return free_game_message(elements)
