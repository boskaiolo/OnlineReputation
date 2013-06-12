OnlineReputation
================

An Online Reputation tool


Requirements:
--

You do need the following packages to run the project:

`nltk`
`TwitterSearch`
`senti_classifier`
`gitpython`
`cPickle`

For all of them, just simply `pip install <package>` or `easy_install <package>`



Running it:
--

Insert your Twitter parameters in `params.py` (there is a template file, named `params.py.TEMPLATE.py`. Modify and rename it)


Then, run `py/main.py`


--


__Remarks__

If it appears the error
`[ERROR] HTTP status 429 - Too Many Requests: Request cannot be served due to the application's rate limit having been exhausted for the resource`

try waiting a few minutes. Twitter APIs have rate limitations.


Try it:
--
Just open `sample.html`