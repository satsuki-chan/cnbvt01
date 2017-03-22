# Webscraping project to extract and download all the Mexican investment funds registered and listed at the [National Banking and Stock Commission](http://www.cnbv.gob.mx/SECTORES-SUPERVISADOS/SOCIEDADES-DE-INVERSION/Buscador-de-Sociedades-de-Inversi%C3%B3n/Paginas/Buscador-de-Sociedades-de-Inversion.aspx) (CNBV, *Comisión Nacional Bancaria y de Valores*), until October, 2015.

## Python version 2.7
Platform: x86_64-suse-linux-gnu (64-bit)
>**Python Software Foundation**. *Welcome to Python.org*.

>http://www.python.org


## Python packages:
### Scrapy - Version == 1.0.3
>**Pablo Hoffman (2015)**. *Scrapy | A Fast and Powerful Scraping and Web Crawling Framework*. Python Package Index version 1.0.3.

>https://scrapy.org/


### Simple search of mutual funds at the CNBV website:
>[http://www.cnbv.gob.mx/SECTORES-SUPERVISADOS/SOCIEDADES-DE-INVERSION/Buscador-de-Sociedades-de-Inversi%C3%B3n/Paginas/B%C3%A1sico.aspx](http://www.cnbv.gob.mx/SECTORES-SUPERVISADOS/SOCIEDADES-DE-INVERSION/Buscador-de-Sociedades-de-Inversi%C3%B3n/Paginas/B%C3%A1sico.aspx)


### Web address of outsourced funds searcher to *Morningstar México*:
>[http://lt.morningstar.com/7ap7omrzjm/fundquickrank/default.aspx](http://lt.morningstar.com/7ap7omrzjm/fundquickrank/default.aspx)


##Execution instructions
####Script files:
* `cnbvt01/cnbvt01/`
  * `items.py`
  * `pipelines.py`
  * `settings.py`
* `cnbvt01/cnbvt01/spiders/`
  * `cnbvt01_spider.py`

####Requiriments configuration file:
* `requirements.txt`

####Output files:
* `<funds_data_file>.json`

####To execute the script:

1. Verify that you have installed Python version 2.7 and the required packages listed in file `requirements.txt`
2. Check that all the files are in the same directory and that you have reading and writing permissions
3. Open a terminal window in the directory and execute:
  * `scrapy crawl cnbvt01 -o <funds_data_file>.json`
