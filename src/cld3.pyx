from libcpp.vector cimport vector
from libcpp.string cimport string

from collections import namedtuple


cdef extern from "nnet_language_identifier.h" namespace "chrome_lang_id::NNetLanguageIdentifier":
    cdef struct Result:
        string language
        float probability
        bint is_reliable
        float proportion


cdef extern from "nnet_language_identifier.h" namespace "chrome_lang_id":
    cdef cppclass NNetLanguageIdentifier:
        NNetLanguageIdentifier(int min_num_bytes, int max_num_bytes);
        Result FindLanguage(string &text)
        vector[Result] FindTopNMostFreqLangs(string &text, int num_langs)
        const char kUnknown[]


LanguagePrediction = namedtuple("LanguagePrediction",
                                ("language", "probability", "is_reliable",
                                 "proportion"))


def get_language(unicode text, int min_bytes=0, int max_bytes=1000):
    """Get the most likely language for the given text.

    The prediction is based on the first N bytes where N is the minumum between
    the number of interchange valid UTF8 bytes and max_bytes. If N is less
    than min_bytes long, then this function returns None.

    If the language cannot be determined, None will be returned.
    """
    cdef NNetLanguageIdentifier *ident = new NNetLanguageIdentifier(
        min_bytes, max_bytes)
    cdef Result res = ident.FindLanguage(text.encode('utf8'))

    if str(res.language) != ident.kUnknown:
        language = res.language.decode('utf8')
        return LanguagePrediction(language, res.probability, res.is_reliable,
            res.proportion)
    else:
        return None


def get_frequent_languages(unicode text, int num_langs, int min_bytes=0,
                           int max_bytes=1000):
    """Find the most frequent languages in the given text.

    Splits the input text (up to the first byte, if any, that is not
    interchange valid UTF8) into spans based on the script, predicts a language
    for each span, and returns a list storing the top num_langs most frequent
    languages along with additional information (e.g., proportions). The number
    of bytes considered for each span is the minimum between the size of the
    span and max_bytes. If more languages are requested than what is available
    in the input, then the list returned will only have the number of results
    found. Also, if the size of the span is less than min_bytes long, then the
    span is skipped. If the input text is too long, only the first 1000 bytes
    are processed.
    """
    cdef NNetLanguageIdentifier *ident = new NNetLanguageIdentifier(
        min_bytes, max_bytes)
    cdef vector[Result] results = ident.FindTopNMostFreqLangs(
        text.encode('utf8'), num_langs)

    out = []
    for res in results:
        if str(res.language) != ident.kUnknown:
            language = res.language.decode('utf8')
            out.append(LanguagePrediction(
                language, res.probability, res.is_reliable, res.proportion))
    return out

del namedtuple
