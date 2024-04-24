# -*- coding: utf-8 -*-

from fastapi import HTTPException


class ParamValidator:

    @staticmethod
    def check_params(params, required_fields):
        for field in required_fields:
            if field not in params or not params[field]:
                error_message = f"{field.capitalize()} is required and cannot be empty"
                raise HTTPException(status_code=400, detail=error_message)
