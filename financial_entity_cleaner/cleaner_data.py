""" This module defines a dictionary of legal terms found in company's name."""

legal_terms_dict = {
    "Agrupamento Complementar de Empresas": ["ace", "a.c.e"],
    "Asociacion Civil": ["ac"],
    "Limited": ["ltd", "lt"],
    "Corporation": ["co", "c.o"],
    "Incorporated": ["inc", "inc."],
}

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
    "remove_numbers",
    "remove_words_in_parentheses",
    "replace_hyphen_underscore_by_space",
    "remove_all_punctuation",
    "enforce_single_space_between_words",
]
