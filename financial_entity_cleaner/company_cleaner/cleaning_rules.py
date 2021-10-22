cleaning_rules_dict = {
    "remove_email": ["", "\S*@\S*\s?"],
    "remove_url": ["", "https*\S+"],
    "remove_www_address": ["", "https?://[.\w]{3,}|www.[.\w]{3,}"],
    "enforce_single_space_between_words": [" ", "\s+"],
    "treat_AND": [" and ", "(&)"],
    "replace_hyphen_underscore_by_space": [" ", "(-|_)"],
    "remove_all_punctuation": ["", "([^\w\s])"],
    "remove_mentions": ["", "@\S+"],
    "remove_hashtags": ["", "#\S+"],
    "remove_numbers": ["", "\w*\d+\w*"],
    "remove_single_quote_next_character": ["", "'\w+"],
    "remove_words_in_parentheses": ["", "\([^()]*\)"],
}

default_company_cleaning_rules = [
    "remove_email",
    "remove_url",
    "remove_www_address",
    "remove_words_in_parentheses",
    "remove_numbers",
    "replace_hyphen_underscore_by_space",
    "remove_all_punctuation",
    "enforce_single_space_between_words",
]