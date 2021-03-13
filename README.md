<!-- Project Intro -->
<br />
<p align="center">
  <h3 align="center">ICS Search Engine</h3>
  <p align="center">
    A simple search engine of UCI's ICS web pages. 
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributors">Contributors</a></li>
  </ol>
</details>

<!-- About The Project -->
## About The Project
This search engine was a group assignment for a class at UCI Winter 2021. We were
given a large corpus (roughtly 56000 web pages). 

### Features
* Uses an inverted index containing tf-idf scores
* **No** databases! The inverted index is not loaded in memory. It is kept in a text file. 
* Less than 300ms search retrieval for queries

### Built With
* Python 3.6+ 
  * Libraries - [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [nltk](https://www.nltk.org/)
* Flask
* HTML 

<!-- Getting Started -->
## Getting Started

To create a local copy and run the program, follow these steps on a Windows OS. 

### Prerequisite
You would first need to obtain the course's corpus file and extract it. 
There should be less than 56000 files after extraction, totaling about 3GB of disk space. 

You may also need to install a few libraries if you have never used them before.
Click the links under <a href=#built-with>Built With</a> and follow the 
instructions on how to install the libraries. 

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/lilwon/ICS_Search_Engine.git
    ```
2. Run the indexer on PowerShell
    ```ps1
    py -3 inverted_index.py
    ```
3.  Wait for the indexer to finish creating the inverted index. Takes about 20 minutes.
4.  Run the search retrieval on Powershell
    ```ps1
    py -3 search_component.py
    ```
5. **(Optional)** You can also use the search retrieval on a Web Browser
    ```ps1
    py -3 webgui.py
    ```
6. **(Optional)** When running the `webui.py`  file, open a browser and paste the following url to your adderess bar: http://127.0.0.1:5000/

<!-- Contributors -->
## Contributors
See the contributors section on the side of this Github page. 