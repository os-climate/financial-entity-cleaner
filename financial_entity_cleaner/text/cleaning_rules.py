cleaning_rules_dict = {
    "remove_email": [" ", "\S*@\S*\s?"],
    "remove_url": [" ", "https*\S+"],
    "remove_word_the_from_the_end": [" ", "the$"],
    "place_word_the_at_the_beginning": [" ", "the$"],
    "remove_www_address": [" ", "https?://[.\w]{3,}|www.[.\w]{3,}"],
    "enforce_single_space_between_words": [" ", "\s+"],
    "replace_amperstand_by_AND": [" and ", "&"],
    "add_space_between_amperstand": [" & ", "&"],
    "replace_amperstand_between_space_by_AND": [" and ", "\s+&\s+"],
    "replace_hyphen_by_space": [" ", "-"],
    "replace_hyphen_between_spaces_by_single_space": [" ", "\s+-\s+"],
    "replace_underscore_by_space": [" ", "_"],
    "replace_underscore_between_spaces_by_single_space": [" ", "\s+_\s+"],
    "remove_all_punctuation": [" ", "([^\w\s])"],
    "remove_all_letters": ["", "[a-zA-Z]+"],
    "remove_spaces": ["", "\s"],
    "remove_punctuation_except_dot": [" ", "([^\w\s.])"],
    "remove_mentions": [" ", "@+"],
    "remove_hashtags": [" ", "#+"],
    "remove_asterisk": [" ", "\*+"],
    "remove_numbers": [" ", "\w*\d+\w*"],
    "remove_text_puctuation": [" ", "\;|\:|\,|\.|\?|\!|\"|\\|\/|\|"],
    "remove_text_puctuation_except_dot": [" ", "\;|\:|\,|\?|\!|\"|\\|\/|\|"],
    "remove_math_symbols": [" ", "\+|\-|\*|\>|\<|\=|\%"],
    "remove_math_symbols_except_dash": [" ", "\+|\*|\>|\<|\=|\%"],
    "remove_parentheses": [" ", "\(|\)"],
    "remove_brackets": [" ", "\[|\]"],
    "remove_curly_brackets": [" ", "\{|\}"],
    "remove_single_quote_next_character": [" ", "'\w+"],
    "remove_single_quote": [" ", "'"],
    "remove_double_quote": [" ", "\""],
    "remove_words_in_parentheses": [" ", "\([^()]*\)*"],
    "remove_words_in_asterisk": [" ", "\*[^()]*\*"],
    "remove_question_marks_in_parentheses": [" ", "\([?*^()]*\)"],
    "repeat_remove_words_in_parentheses": [" ", "remove_words_in_parentheses"]
}

default_company_cleaning_rules = [
    "place_word_the_at_the_beginning",
    "remove_words_in_parentheses",
    "repeat_remove_words_in_parentheses",
    "remove_words_in_asterisk",
    "add_space_between_amperstand",
    "replace_amperstand_between_space_by_AND",
    "replace_hyphen_by_space",
    "replace_underscore_by_space",
    "remove_text_puctuation_except_dot",
    "remove_math_symbols",
    "remove_parentheses",
    "remove_brackets",
    "remove_curly_brackets",
    "remove_single_quote_next_character",
    "remove_double_quote",
    "enforce_single_space_between_words"
]


def is_valid(list_cleaning_rules):
    """
    This method checks if all the names of cleaning rules informed in a list exist as a
    regex rule in the dictionary of cleaning rules.

    Parameters:
        list_cleaning_rules(list): a list with the names of cleaning rules to be applied
    Returns:
        True: if all the items exist in the dictionary of cleaning rules.
        False: if at least one item does not exist in the in the dictionary of cleaning rules.
    Raises:
        No exception is raised.
    """
    for cleaning_rule in list_cleaning_rules:
        if not (cleaning_rule in cleaning_rules_dict):
            return False
    return True
