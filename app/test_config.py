from config import Config

config = Config()

print(

    config.get(

        "quality",

        "blur_threshold"

    )

)