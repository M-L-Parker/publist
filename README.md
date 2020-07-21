# publist
Script to generate a publication list pdf from an ORCID. Queries ADS to find all relevant publications, adds them to a latex document, then runs xelatex to generate a pdf.

<br />

### Requirements:
https://github.com/andycasey/ads

Make sure to read the documentation for this, specifically the section on getting an ADS API key.


<br />

### Generating publication list:
Replace the ordcid and author names in publist_short.py then run.
Publication list formatting is all contained in preamble.tex, which is easy to modify or replace.

