RU_VIDEOS = {
    "start": "BAACAgIAAxkBAAIDI2YBZ-Zl_SAKhwLnDygWyLR7HINfAAKgSwACdMIISNjshueJO-vJNAQ"
}

EN_VIDEOS = {
    "start": "BAACAgIAAxkBAAIDI2YBZ-Zl_SAKhwLnDygWyLR7HINfAAKgSwACdMIISNjshueJO-vJNAQ"
}

VIDEOS = {
    "ru": RU_VIDEOS,
    "en": EN_VIDEOS,
}


def get_videos(language_code: str):
    return VIDEOS[language_code]
