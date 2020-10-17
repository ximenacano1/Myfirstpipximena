from nltk import ngrams
from unidecode import unidecode
from fuzzywuzzy import fuzz
from langid import classify
from googletrans import Translator


def __jc_similarity_base(title1, title2, n=3):
    '''
    Utility function to avoid code duplication, implementation below.
    '''
    n1 = ngrams(title1.split(), n)
    n2 = ngrams(title2.split(), n)
    n1 = set(n1)
    n2 = set(n2)
    unilen = len(n1.union(n2))
    lenmin = min([len(n1), len(n2)])

    if unilen == 0 or lenmin == 0:
        S = 0
    else:
        J = len(n1.intersection(n2))/unilen
        C = len(n1.intersection(n2))/lenmin
        if J+C != 0:
            S = 2*J*C/(J+C)
        else:
            S = 0
    return S


def jc_similarity(title1, title2, n=3, boolean=False, threshold=0.8, use_traslation=True):
    '''
    Computes titles similarity according to section 2.6 of
    https://arxiv.org/pdf/1911.02782.pdf

    Parameters
    ----------
    title1 : str
        text to compare
    title2 : str
        second text to compare
    n : int (optional)
        number n in n-gram partition of titles
    boolean : bool
        If you want the output to be a bool
    threshold : float
        Threshold for the boolean outpput
    use_traslation : str
        enable translation support

    Returns
    -------
    similarity : float/bool
        Number between 0 and 1. 1 means the titles are the same and 0 means completely different
        Or True if similarity is avobe threshold, false otherwise
    '''
    title1 = unidecode(title1.lower())
    title2 = unidecode(title2.lower())

    S = __jc_similarity_base(title1, title2, n)

    if S < threshold and use_traslation:
        lang, _ = classify(title1)
        if lang != "en":
            translator = Translator()
            title1 = translator.translate(title1).text
        lang, _ = classify(title2)
        if lang != "en":
            translator = Translator()
            title2 = translator.translate(title2).text

    S = __jc_similarity_base(title1, title2, n)

    if boolean:
        if S >= threshold:
            return True
        else:
            return False
    else:
        return S


def __colav_similarity(title1, title2, upper_thold=90, bottom_thold=40):
    '''
    Utility function to avoid code duplication, public implementation below.
    '''
    label = False
    ratio = fuzz.partial_ratio(title1, title2)
    if ratio > upper_thold:
        label = True
    elif ratio > upper_thold:
        ratio = fuzz.token_set_ratio(title1, title2)
        if ratio > bottom_thold:
            label = True
        elif ratio > bottom_thold:
            ratio = fuzz.partial_token_set_ratio(title1, title2)
            if ratio > upper_thold:
                label = True
    return label


def colav_similarity(title1, title2, upper_thold=90, bottom_thold=40, use_traslation=True):
    '''
    custom metric for similarity using multiple nested metrics from fuzzywuzzy

    Parameters
    ----------
    upper_thold: int
        upper threshold for partial ratio and token_set_ratio
    bottom_thold: int
        bottom threshold for partial ratio and token_set_ratio
    use_traslation: boolean
        support similarity with translation
    '''
    title1 = unidecode(title1.lower())
    title2 = unidecode(title2.lower())

    label = __colav_similarity(title1, title2, upper_thold, bottom_thold)
    if label is False and use_traslation is True:
        translated = 0
        lang, _ = classify(title1)
        if lang != "en":
            translator = Translator()
            title1 = translator.translate(title1).text
            translated = True
        lang, _ = classify(title2)
        if lang != "en":
            translator = Translator()
            title2 = translator.translate(title2).text
            translated = True
        if translated is True:
            label = __colav_similarity(
                title1, title2, upper_thold, bottom_thold)

    return label
