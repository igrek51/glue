import inspect
from typing import List, Any

from cliglue.builder.rule import ValueRule
from cliglue.builder.typedef import TypeOrParser


def parse_value_rule(rule: ValueRule, arg: str) -> Any:
    return parse_typed_value(rule.type, arg)


def parse_typed_value(_type: TypeOrParser, arg: str) -> Any:
    if _type is None:
        return arg
    # custom parser
    if callable(_type):
        return _type(arg)
    # cast to custom type or default types
    return _type(arg)


def generate_value_choices(rule: ValueRule) -> List[Any]:
    if not rule.choices:
        return []
    elif isinstance(rule.choices, list):
        return rule.choices
    else:
        (args, _, _, _, _, _, _) = inspect.getfullargspec(rule.choices)
        return rule.choices()