<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

## About The Project
This project consists in a web scraper that collects daily news from the Russian news sources, store them in a Postgres database.

### Built With
* Python
* Postgresql
* Docker

## Getting Started

### Prerequisites
1. Clone the repo
  ```sh
  git clone ...
  ```

2. Make and activate virtual environment
  ```sh
  python -m venv venv
  ```
  ```sh
  source venv/Scripts/activate
  ```

### Installation

1. Upgrade pip, install requirements
  ```sh
  python -m pip install --upgrade pip
  ```
  ```sh
  pip install -r requirements.txt
  ```

2. Change environment variables in the docker-compose.yml and main.py
  ```docker
  - POSTGRES_USERNAME=
  - POSTGRES_PASSWORD=
  - POSTGRES_DBNAME=
  - POSTGRES_PORT=
  - POSTGRES_ADDRESS=
  ```

## Usage
  Go to the docker folder and then run:
  ```sh
  docker-compose up
  ```
  ```sh
  main.py
  ```
### Database requests
  
  Use categories_data.sql in DBeaver to get necessary info



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Sqlalchemy](https://www.sqlalchemy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Docker](https://www.docker.com/)
* [Postgresql](https://www.postgresql.org/)
