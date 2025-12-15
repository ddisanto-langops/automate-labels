# Goal
To eliminate the need to manually label PT strings with their corresponding article title. 

# Method
We will set up an application, whether via Blackbird.io or my own LangOps server, allowing for strings in any .IDML file to automatically be labeled according to the articles contained in the magazine. There are two possible ways to accomplish this. One is simpler: scraping article titles and content from a URL. This is currently working for PT, and could theoretically be adapted for LSS. The second method, ingesting a Word document (.docx), may be necessary because for RV due to authentication requirements (yet to be tested).

# Deployment
It is necessary to run deploy_setup.sh to create the virtual environment, install Python packages and their dependencies.

# Parameters
The similarity threshold for string matching can be set. Currently it is at 50, which seems to be a little bit greedy (some false positives).
