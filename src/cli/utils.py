# -*- coding: UTF-8 -*-
import ast
from pathlib import Path
from typing import Any, Callable, List


def convert_literal(value: str) -> Any:
    try:
        value = ast.literal_eval(value)
        return value
    except Exception:
        return value


def check_configuration(key: str, value: Any):
    match key:
        case 'mode':
            if not isinstance(value, str):
                raise TypeError('value must be a string.')
            if value not in ['single', 'item']:
                raise ValueError('Unexpected value of mode, it can only be "single" or "item".')
        case 'root':
            if not isinstance(value, str):
                raise TypeError('value must be a string.')
            if not Path(value).is_dir():
                raise ValueError('value must be a directory.')
        case _:
            pass


def complete_items(candidates: List[Any]) -> Callable[[str], List[str]]:
    def complete(incomplete: str) -> List[str]:
        return [str(candidate) for candidate in candidates if str(candidate).startswith(incomplete)]

    return complete


def decode_stdout(output):
    try:
        return output.decode('utf-8')
    except UnicodeDecodeError:
        return output.decode('gbk')
