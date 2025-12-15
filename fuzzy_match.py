from rapidfuzz import fuzz

def get_similarity(string1: str, string2: str) -> float:
    """
    Calculate text similarity using fuzzy matching for times when strings are not identical.
    
    :param string1: string of XLIFF document (will be transformed to lowercase if not already)
    :param string2: string from SQlite database (will be transformed to lowercase if not already)
    """
    score = fuzz.ratio(string1.lower(), string2.lower())

    return score