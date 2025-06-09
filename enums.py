from enum import IntEnum

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class IssueType(IntEnum):
    TWSE = 1 # Taiwan Stock Exchange（上市）
    TPEx = 2 # Taipei Exchange（上櫃）