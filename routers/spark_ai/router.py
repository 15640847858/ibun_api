# -*- coding: utf-8 -*-

from typing import Dict
from fastapi import APIRouter
from models.spark_ai.model import SparkAiModel

router = APIRouter(prefix="/spark_ai")


@router.post("/v3.5")
def get_spark_ai_content(params: Dict):
    """
    快速调用集成星火认知大模型
    """
    model = SparkAiModel()

    # arsed_texts = model.get_spark_ai_content(params)

    parsed_texts = '```python\nfor i in range(5):\n    print("这是第{}次循环".format(i+1))\n```'

    return parsed_texts


@router.get("/")
def get_str():
    # TODO
    return "test"
