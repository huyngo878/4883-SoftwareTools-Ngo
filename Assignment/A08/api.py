from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import pandas as pd
from typing import Optional

app = FastAPI()

# Load the data.csv file into a pandas dataframe for easier manipulation
data = pd.read_csv('data.csv', parse_dates=['Date_reported'])

# Extract the year from the 'Date_reported' column
data['Year'] = data['Date_reported'].dt.year

# Redirects the base URL to the FastAPI auto-generated documentation page.
@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")

# Returns a list of all unique countries present in the dataset.
@app.get("/countries/")
async def countries():
    return data['Country'].unique().tolist()

# Returns a list of all unique WHO_regions present in the dataset.
@app.get("/regions/")
async def regions():
    return data['WHO_region'].unique().tolist()

# Returns the total deaths from all countries and regions in the dataset.
@app.get("/deaths")
async def total_deaths():
    total_deaths = data['Cumulative_deaths'].sum()
    return {"total_deaths": total_deaths}

# Returns the total deaths for the specified country.
@app.get("/deaths_by_country/{country}")
async def deaths_by_country(country: str):
    try:
        filtered_data = data[data['Country'] == country]
        total_deaths = filtered_data['Cumulative_deaths'].sum().item()
        return {"total_deaths": total_deaths}
    except Exception as e:
        return {"error": str(e)}

# Returns the total deaths for the specified WHO_region.
@app.get("/deaths_by_region/{region}")
async def deaths_by_region(region: str):
    filtered_data = data[data['WHO_region'] == region]
    total_deaths = filtered_data['Cumulative_deaths'].sum().item()
    return {"total_deaths": total_deaths}

# Returns the total deaths for the specified country and year.
@app.get("/deaths_by_country_year/{country}/{year}")
async def deaths_by_country_year(country: str, year: int):
    filtered_data = data[(data['Country'] == country) & (data['Year'] == year)]
    total_deaths = filtered_data['Cumulative_deaths'].sum().item()
    return {"total_deaths": total_deaths}

# Returns the total deaths for the specified WHO_region and year.
@app.get("/deaths_by_region_year/{region}/{year}")
async def deaths_by_region_year(region: str, year: int):
    filtered_data = data[(data['WHO_region'] == region) & (data['Year'] == year)]
    total_deaths = filtered_data['Cumulative_deaths'].sum().item()
    return {"total_deaths": total_deaths}

# Returns the country with the maximum number of deaths within the specified date range.
@app.get("/max_deaths/")
async def max_deaths(min_date: Optional[str] = None, max_date: Optional[str] = None):
    try:
        if min_date and max_date:
            date_filtered_data = data[(data['Date_reported'] >= min_date) & (data['Date_reported'] <= max_date)]
        else:
            date_filtered_data = data

        max_death_country = date_filtered_data.loc[date_filtered_data['Cumulative_deaths'].idxmax()]['Country']

        return {
            "country": max_death_country,
            "success": True,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "params": {
                "min_date": min_date,
                "max_date": max_date
            },
        }

# Returns the country with the minimum number of deaths within the specified date range.
@app.get("/min_deaths/")
async def min_deaths(min_date: Optional[str] = None, max_date: Optional[str] = None):
    try:
        if min_date and max_date:
            date_filtered_data = data[(data['Date_reported'] >= min_date) & (data['Date_reported'] <= max_date)]
        else:
            date_filtered_data = data

        min_death_country = date_filtered_data.loc[date_filtered_data['Cumulative_deaths'].idxmin()]['Country']

        return {
            "country": min_death_country,
            "success": True,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "params": {
                "min_date": min_date,
                "max_date": max_date
            },
        }

# Returns the average number of deaths across all countries and regions in the dataset.
@app.get("/avg_deaths/")
async def avg_deaths():
    try:
        avg_deaths = data['Cumulative_deaths'].mean()

        return {
            "average": avg_deaths,
            "success": True,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
