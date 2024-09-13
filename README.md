# sqlalchemy-challenge
 # Climate Analysis

This project involves analyzing climate data and designing a climate app using Flask. The steps are outlined below:

## Part 1: Analyze and Explore the Climate Data

In this section, you will use Python and SQLAlchemy for basic climate analysis and data exploration of your climate database. Specifically, you will:

- Use SQLAlchemy ORM queries to interact with the database.
- Employ Pandas for data manipulation and analysis.
- Utilize Matplotlib for data visualization.

## Part 2: Design Your Climate App

After completing your initial analysis, you will design a Flask API based on the queries developed in Part 1. To accomplish this, you will:

- Use Flask to create API routes.
- Implement the following endpoints:
  - `/api/v1.0/precipitation` - Returns precipitation data for the last 12 months.
  - `/api/v1.0/stations` - Lists all stations in the dataset.
  - `/api/v1.0/tobs` - Provides temperature observations for the most active station for the previous year.
  - `/api/v1.0/<start>` - Calculates TMIN, TAVG, and TMAX for dates greater than or equal to the start date.
  - `/api/v1.0/<start>/<end>` - Calculates TMIN, TAVG, and TMAX for dates between the start and end dates.

Follow these steps to design your Flask API based on your data analysis results.

