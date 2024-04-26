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

    @staticmethod
    def optimize_question(params):
        optimized_params = []
        total_length = 0

        for item in reversed(params):
            content = item['content']
            content_length = len(content)
            if total_length + content_length <= 760:
                optimized_params.insert(0, item)
                total_length += content_length
            else:
                remaining_length = 800 - total_length
                truncated_content = content[:remaining_length]
                item['content'] = truncated_content
                optimized_params.insert(0, item)
                break  # 结束循环，因为已经达到800字符长度

        return optimized_params
