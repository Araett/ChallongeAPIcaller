Challonge API Viewer
====================

Installation
------------

Requires:

- python 3.6+

Requirements:

Install with pipenv from Pipfile::

    pipenv install

Running
-------

Use creds.sample.json as an example to create creds.json and place it at a local directory to the script/executable

bash:
	From `pipenv shell`::

		python CAC.py

Windows:
	Run CAC.exe
	
matchparam.json is a file to control the flow of the script by searching games via given suggested play order::
	{
	"AreCustomParametersNeeded": "true/false",
	"MatchNo1": "1-(maximum match count) or empty",
	"MatchNo2": "1-(maximum match count) or empty"
	}
