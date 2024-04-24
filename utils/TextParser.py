# -*- coding: utf-8 -*-

class SparkTextParser:
    @staticmethod
    def parse_text(data):
        content = ""
        if getattr(data, 'generations', None):
            for generation in getattr(data, 'generations', None):
                for item in generation:
                    if getattr(item, 'text', None):
                        content = item.text
                        print("content:", content)
        return content

    @staticmethod
    def filter_params(params, keys):
        return {key: params[key] for key in keys if key in params}
