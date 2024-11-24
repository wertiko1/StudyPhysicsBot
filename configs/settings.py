class CacheSettings:
    redis_url: str = "redis://redis:6379/0"
    state_ttl: int | None = None
    data_ttl: int | None = None


class Colors:
    RED: str = "#FF5733"
    GREEN: str = "#33FF57"
    BLUE: str = "#3357FF"
    YELLOW: str = "#F5FF33"
    PURPLE: str = "#800080"
    ORANGE: str = "#FFA500"
    PINK: str = "#FFC0CB"
    CYAN: str = "#00FFFF"
    MAGENTA: str = "#FF00FF"
    LIME: str = "#00FF00"
    TEAL: str = "#008080"
    BROWN: str = "#A52A2A"
    GRAY: str = "#808080"
    LIGHT_BLUE: str = "#ADD8E6"
    DARK_BLUE: str = "#00008B"
    LIGHT_GREEN: str = "#90EE90"
    DARK_GREEN: str = "#006400"
    GOLD: str = "#FFD700"
    SILVER: str = "#C0C0C0"
    BEIGE: str = "#F5F5DC"
    INDIGO: str = "#4B0082"
    VIOLET: str = "#EE82EE"
    TURQUOISE: str = "#40E0D0"
    CORAL: str = "#FF7F50"
    IVORY: str = "#FFFFF0"
    MINT: str = "#98FF98"
    PEACH: str = "#FFDAB9"
