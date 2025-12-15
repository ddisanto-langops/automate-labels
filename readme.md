# Goal
Eliminate the need to manually label PT strings with their corresponding article title in inDesign files. We expect to save between 30 minutes to 1 hour in manual work. 

# Method
This will be the first app set up on the langops-ca server. It will allow for strings in any .IDML file to automatically be labeled according to the articles contained in the magazine. The current implementation uses a web scraper to populate a database with article title and strings. A comparison is then made between the XLIFF strings and the database. Matches which exceed a given threshold are labeled with the corresponding article title via the Crowdin API.

# Deployment
It is necessary to run deploy_setup.sh to create the virtual environment, install Python packages and their dependencies.

# Usage
The end user must create and post a comment, with the text '#label' and all URLs of articles to be labeled.

# Parameters
**Similarity threshold:** *for string matching can be set inside main.py (not currently accessible to end-users). A setting of 50, the default, seems to be a little bit greedy (some false positives).*  
**Article URLs** *The end-user must insert all URLS of the desired articles.*

# Known Issues
**Matching will never be perfect:** *inDesign files contain strings not belonging to any article (e.g. table of contents ). These will still need manual classification; at best, they can be labeled as unclassified if desired.*  
**Labeling RV articles:** *Need to determine authentication/access*
