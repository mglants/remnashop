from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    NewType,
    Optional,
    TypeAlias,
    Union,
)

from aiogram.types import (
    BufferedInputFile,
    ForceReply,
    FSInputFile,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from pydantic import PlainValidator

from app.core.enums import Locale

if TYPE_CHECKING:
    ListStr: TypeAlias = list[str]
    ListLocale: TypeAlias = list[Locale]
else:
    ListStr = NewType("ListStr", list[str])
    ListLocale = NewType("ListLocale", list[Locale])

AnyInputFile: TypeAlias = Union[BufferedInputFile, FSInputFile]

I18nFormatter: TypeAlias = Callable[[str, Optional[dict[str, Any]]], str]

AnyKeyboard: TypeAlias = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
]

StringList: TypeAlias = Annotated[
    ListStr, PlainValidator(lambda x: [s.strip() for s in x.split(",")])
]
LocaleList: TypeAlias = Annotated[
    ListLocale, PlainValidator(func=lambda x: [Locale(loc.strip()) for loc in x.split(",")])
]

Int16: TypeAlias = Annotated[int, 16]
Int32: TypeAlias = Annotated[int, 32]
Int64: TypeAlias = Annotated[int, 64]
DictStrAny: TypeAlias = dict[str, Any]
