from abc import ABC, abstractmethod
from typing import Optional, List
import re

USD = "USD"
UAH = "UAH"


class ParsedFieldName:
    PRICE = "price"
    CURRENCY = "currency"
    LOCATION = "location"
    PHONE_NUMBER = "phone_number"
    ROOMS = "rooms"
    TAGS = "tags"


class BaseParserStrategy(ABC):
    @abstractmethod
    def parse(self, data) -> dict:
        raise NotImplementedError()


class DefaultStrategy(BaseParserStrategy):
    UAH_PATTERN = r"\b\d{1,3}(?:\.|,|\s)?\d{3}(?=\+ку|\b|\s|грн)"
    USD_PATTERN = r"(?:\$\s?)\b\d{3,5}|\b\d{3,5}(?:\s?\$)"

    def parse(self, data):
        results = dict()
        results[ParsedFieldName.PRICE] = self._get_price(data)
        results[ParsedFieldName.CURRENCY] = self._get_currency(data)
        results[ParsedFieldName.LOCATION] = self._get_location(data)
        results[ParsedFieldName.PHONE_NUMBER] = self._get_phone_number(data)
        results[ParsedFieldName.ROOMS] = self._get_rooms(data)
        results[ParsedFieldName.TAGS] = self._get_tags(data)
        return results

    @staticmethod
    def _get_price(data) -> Optional[int]:
        price = None
        uah_price_match = re.search(DefaultStrategy.UAH_PATTERN, data)
        if uah_price_match:
            price = uah_price_match.group(0).replace(".", "").replace(",", "").replace(" ", "").replace("грн", "")

        usd_price_match = re.search(DefaultStrategy.USD_PATTERN, data)
        if usd_price_match:
            price = usd_price_match.group(0).replace("$", "").replace(" ", "")

        return int(price) if price is not None else price

    @staticmethod
    def _get_currency(data) -> Optional[str]:
        uah_price_match = re.search(DefaultStrategy.UAH_PATTERN, data)
        if uah_price_match:
            return UAH

        usd_price_match = re.search(DefaultStrategy.USD_PATTERN, data)
        if usd_price_match:
            return USD

        return None

    @staticmethod
    def _get_rooms(data) -> Optional[int]:
        rooms_pattern = r"\b\d{1}(?:\s?к)"
        room_match = re.search(rooms_pattern, data)
        if room_match:
            rooms = room_match.group(0).replace("к", "").replace(" ", "")
            return int(rooms)
        return None

    @staticmethod
    def _get_phone_number(data) -> Optional[str]:
        phone_regex = r"(?:\+38)?\(?\d{3}\)?-?\d{3}-?\d{4}\b"
        phone_match = re.search(phone_regex, data)
        if phone_match:
            return phone_match.group(0).replace("(", "").replace(")", "")
        return None

    @staticmethod
    def _get_location(data) -> List[str]:
        # TODO improve this method
        location_regex = r"\b[A-Z][a-z]+\b(?:\s+\b[A-Z][a-z]+\b)*"
        return re.findall(location_regex, data)

    @staticmethod
    def _get_tags(data) -> List[str]:
        tags = r"\b(ЖК|студия)"
        return re.findall(tags, data)
