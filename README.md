# CLD3 Python bindings
These are Python bindings for [cld3](https://github.com/Google/cld3), a
language classifying library used in Google Chrome.

Included are Python bindings (via Cython). Building the extension does not
require the chromium repository, instead only these libraries need to
be installed:

- Cython
- msgpack
- Protobuf (with headers and protoc)

To install the extension, just run `pip install` on the repository URL, or use
`pip install cld3`.

## Usage
Here's some examples:

```python
>>> cld3.get_language("This is a test")
LanguagePrediction(language='en', probability=0.9999980926513672, is_reliable=True, proportion=1.0)

>>> cld3.get_frequent_languages("This piece of text is in English. Този текст е на Български.", 5)
[LanguagePrediction(language='bg', probability=0.9173890948295593, is_reliable=True, proportion=0.5853658318519592), LanguagePrediction(language='en', probability=0.9999790191650391, is_reliable=True, proportion=0.4146341383457184)]
```

In short:

`get_language` returns the most likely language as the named tuple `LanguagePrediction`. Proportion is always 1.0 when called in this way.

`get_frequent_languages` will return the top number of guesses, up to a maximum specified (in the example, 5). The maximum is mandatory. Proportion will be set to the proportion of bytes found to be the target language in the list.

In the normal cld3 library, "und" may be returned as a language for unknown languages (with no other stats given). This library filters that result out as extraneous; if the language couldn't be detected, nothing will be returned. This also means, as a consequence, `get_frequent_languages` may return fewer results than what you asked for, or none at all.
