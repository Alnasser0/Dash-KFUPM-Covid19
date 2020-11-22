# KFUPM Covid-19 Dashboard

KFUPM COVID19 Dashbaord

## Setup

The project is developed using python **3.7.x**. It is highly recommended that you use [Anaconda](https://www.anaconda.com/products/individual#Downloads) for managing python environments. Below is a guide on how to setup this project locally using anaconda.

First, clone this project and navigate to the folder.

Create a python environment for this project. An existing `environment.yml` file will set up all the required dependencies.

```
conda env create -f environment.yml
```

Then create a `.env` file with following structure and fill the required information.

```
FLASK_APP=app
FLASK_ENV=development

DB_NAME=COVID19-KFUPM
DB_USERNAME=<username>
DB_PASSWORD=<password>
```

## Usage

to be filled

### In Development (contribution is appreciated):

- Data Download Automation (Scheduling) - Done (Part of it in Heroku)
- Codes Optimization - Done
- UI improvements - Done
- Add sliders for Regions and Cities and embed them using call-back functions. - Done
- Add a table of data - Done
- Develop a PWA for phones - Not feasible

### UI Improvements:

- Add a NavBar - Done
- Add the sliders to the DOC - Done
- Add a summary region with x by y px boxes - Done
- Divide the div sections of each graph into 2 graphs with good padding - Done
- Add a footer - Done
- Organize stuff in the dashboard - Done

### Future Improvements to consider:

- Add Simulation done by KFUPM@COE COVID19 Team
- Expand to All Saudi Arabia Regions and Cities
- Make UI more rebust, organized, and mobile friendly.
- Update layout to imitate real dashboard design.
- Add Arabic Language Support.
- Improve CSS in the page.
- Optimize Codes.
- Use MongoDB or Postgre instead of csv files. - Done
