# Lease Mileage Prediction

## Overview

This project aims to provide a prediction for the number of miles you will travel by the end of your lease period. It utilizes a statistical approach and time series forecasting to generate accurate forecasts and estimate the accuracy probability.

## Algorithm

The algorithm follows these steps:

1. **Gather daily mileage data**: Collect the daily mileage data for your lease vehicle from a xlsx file.

2. **Calculate the average daily mileage**: Calculate the average of all the recorded daily mileages to get an estimate of your typical daily mileage.

3. **Handle outliers**: Identify and handle outliers using statistical methods like the interquartile range (IQR) or Z-score. This helps account for infrequent road trips or other unusual mileage data points.

4. **Determine the remaining lease days**: Calculate the number of days remaining in your lease agreement. This will be used to forecast the mileage for the remaining period.

5. **Fit a time series forecasting model**: Utilize an ARIMA (AutoRegressive Integrated Moving Average) model to fit the historical mileage data. This model captures patterns and trends in the data to make accurate predictions.

6. **Generate a forecast for the remaining lease period**: Utilize the fitted ARIMA model to generate a mileage forecast for the remaining lease days.

7. **Calculate the accuracy probability**: Estimate the prediction intervals around the forecasted mileage to determine the accuracy probability. Wider prediction intervals indicate higher uncertainty, while narrower intervals suggest higher accuracy.

8. **Provide the forecasted total mileage and accuracy probability**: Return the forecasted total mileage for the remaining lease period, along with the accuracy probability based on the calculated prediction intervals.

## Requirements

- Python 3.x
- pandas library
- numpy library
- statsmodels library
- tkinter library

## Usage

1. Install the required libraries using pip:  `pip install pandas numpy statsmodels tkinter` .
2. Run the code using a Python interpreter.  `python main.py`
3. Select the input data file in Excel format (.xlsx) through the "Select File" button.
4. Enter the lease end date in the provided field.
5. Click the "Calculate" button to perform the mileage forecast.
6. The forecasted total mileage and accuracy probability will be displayed in the user interface.

Please ensure that the input data file contains a column named 'Miles Traveled' with the daily mileage data.

If you encounter any issues or have any questions, please don't hesitate to reach out.

Enjoy using the Mileage Forecast tool!

Please let me know if you need any further information or have any specific requirements!
