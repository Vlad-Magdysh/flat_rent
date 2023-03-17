from message_parser.parser_strategy import BaseParserStrategy, DefaultStrategy


class Parser:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy: BaseParserStrategy):
        self._strategy = strategy

    def parse(self, data: str) -> dict:
        return self._strategy.parse(data)
