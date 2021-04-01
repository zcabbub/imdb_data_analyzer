# IMDb Data Analyzer

#### What this script does: 

Starting from an input movie, this script outputs data about the Box Office revenues based: 

- the previous 10 movies of:

  - the lead actor
  - second lead actor
  - director
  - producer
  
- the top 100 movies of their main genre
- the top 100 movios of their secondary genre



### Getting started:
In order to use this python script you need to run it from a virtual environment. Please follow the next steps:

- open a terminal and navigate to the project folder
- create a virtual environment at your choice, e.g.:

        virtualenv .venv

- enter the virtual environment:

        source .venv/bin/activate

- install the required packages:

        pip install -r requirements.txt
 
#### Next, create a new folder and name it **"input_data"**.

Please use this website to download the required input files:

https://datasets.imdbws.com/


Please download the following packages: **title.basics.tsv.gz** and **title.ratings.tsv.gz**.
After downloading, **unarchive** and move them both to *input_data* folder.

*Every once in a while you must download this data again in order to keep the results up to date.*

Using these 2 files, the script will generate a JSON file called *movies_by_genre.json* that can be found in the project root directory.
If that file already exists, the script will simply read it and use it. 
This file contains all the movies categorized by *genre* and sorted descending by the **number of votes**. 

### Usage

This script takes as input an IMDb movie ID, e.g. *0372784*.

**WARNING**: ***Please input only digits.*** In their URLs and databases, IMDb writes the IDs with *tt* before, i.e.: *tt0372784*. Anyway, in IMDbPy, only the digits are used.

Make sure that you run the script while being into a virtual environment (*see the command above*).

*The script takes only 1 argument. If you provide more, only the first one will be considered.*

        python3 main.py <ID>


### Outputs

Running the script will populate *output_data* folder. Every file name has the same format:

**ID_DATE_DESCRIPTION.file**

ID - the input movie ID without the "tt" prefix
DATE - the date of running the script

This scrip generates the following files:

- *ID*_*DATE*.json : this contains all the data in JSON format. Both **opening weekend revenues** and **worldwide revenues**
- *ID*_*DATE*_weekend.csv : table that stores the Box Office revenue data from the **opening weekdend**
- *ID*_*DATE*_worldwide.csv : table that stores the **worldwide** Box Office revenue data 
- *ID*_*DATE*_averages.json : for each category (i.e., *lead actor*), the average is calculated for **both** opening weekend and worldwide revenues. *It counts only the non-null values.*
- *ID*_*DATE*_ratios.json : for each movie, other than the inputted one, the **opening weekend revenue / worldwide revenue** is calculated.


### Conclusion
This can be easily extended to take as input multiple IDs. Anyway the program takes quite a lot of time to completely run, since IMDbPy is quite slow and it has to take the data from 240 movies. 














