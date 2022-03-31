# Gestational Diabetes Onset Estimation
### By Jessica Lewis

## Introduction
Gestational diabetes (GDB) is a type of diabetes that occurs during pregnancy. The placenta takes over hormone production for both the fetus and the host; in some pregnancies the placenta mismanages the uptake of blood sugar. This is what causes GDB. Without a prior diagnosis of gestational diabetes or a history of non-gestational diabetes, pregnant people are typically tested for GDB between 24 and 28 weeks of pregnancy.

### Problem Statement
**Can I reverse a time series of gestational diabetes data to pinpoint the onset in my pregnancy?**

#### SUCCESS CRITERIA
There are two aspects to this project: making predictions on a reversed time series and estimating the onset of GDB in my pregnancy. I consider this project a success if either of these criteria succeed.
<ol>
    <li>I make predictions for dates before my data starts</li>
    <li>My predictions cross a threshold chosen using target blood sugar levels for pregnant people. These values depend on what I end up using as my target variable</li>
</ol>

### Context
I became pregnant in 2021 and at 27 weeks I was diagnosed with GDB. I immediately scheduled an appointment with a specialist and at 29 weeks I changed my diet and began taking blood sugar readings 4 times per day: when I woke up and an hour after each meal. I was also given carb and protein targets for meals/snacks and recorded my carb intake. I took up to 10 records per day, until I went into labor, totalling roughly 11 weeks of data.

## Approach

### The Data
All of the data had been saved to a mobile app called One Touch Reveal, a popular tracking app for people with diabetes and their healthcare professionals. I was able to log into the website application and load a report with all of my data and although there was an export function it was unhelpful for this project; it compiled a pdf file. There was also an API working to generate the report, but it was not accessible to me.

I re-downloadied the app onto my phone and found the export button. Unfortunately the export feature only worked from the current date; I couldn’t set custom export parameters. I was able to get around this by manually setting the system data on my phone to the last day of my data and then running the “Last 90 days” export option, which was enough to include everything. Once I had the spreadsheet on my phone storage I copied it to google sheets and was then able to grab it on my laptop for this project.

#### A COUPLE NOTES ON TERMINOLOGY
There are some terms that I use interchangeably throughout this project. Blood glucose is the same thing as blood sugar. Also, readings and records both mean rows in the dataframe.

## Data Cleaning and Preprocessing
After loading the data I began by fixing the datatypes and I set the index to the datetime column. I removed rows where the value was 0 and checked for other null values. Next up was feature extraction. Overall the data didn’t need a lot of cleaning.

## Feature Extraction
In order to work with the data by day, instead of by datetime, I added a column that counted up from 1 for each calendar day. I called this daycount and used it to iterate through each day while setting the next feature: subtypes.

Each record came in with a type: either Blood Sugar Reading or Carbs. But each of those also broke down into more specific subtypes that I wanted to be able to compare.

Once I had subtypes for each record I noticed that there were quite a few repeated subtypes within the same day. In these cases I had, say, eaten two snacks instead of one, or had some more lunch before taking my blood sugar reading. I wanted to combine the extra readings so that each day only had one of each subtype so I built a function to do this but still ended up having to make quite a few individual decisions.

Once I had all of the subtypes in I created another column to flag values that are outOfRange. 

## EDA

### Full Dataframe
![Time Series of Blood Sugar Readings](/vis/all_bg.png)
![Time Series of Carb Readings](/vis/all_carbs.png)

### Daily Dataframe
![Daily Fasting, Non-Fasting, and Carb Readings](/vis/daily_graphs.png)


## Pre-processing
From here on out I decided to consider three potential target variables:
<ul>
	<li>bg_fasting: Daily Fasting Readings</li>
	<li>bg_avg: Daily Blood Sugar Averages</li>
	<li>all: All Blood Sugar Readings</li>
</ul>

### Full Dataframe

#### TESTING FOR STATIONARITY
Dickey Fuller and KPSS tests indicate that the time series is non-stationary.

#### ACF AND PACF
![Full Dataframe ACF and PACF](/vis/full_acf-pacf.png)

The ACF and PACF contradicts the results of the Dickey Fuller test: a higher order of differencing is not necessary.

### Daily Fasting Readings

#### TESTING FOR STATIONARITY
Dickey Fuller and KPSS tests indicate that the time series is non-stationary.

#### ACF AND PACF
![Daily Fasting ACF and PACF](/vis/daily_fasting_acf-pacf.png)

The ACF and PACF confirms the results of the Dickey Fuller test.

**Differenced**

![Daily Fasting ACF and PACF Differenced](/vis/daily_fasting_acf-pacf-diff.png)

The differenced ACF and PACF look slightly over-differenced because that first lag is almost -0.5. We’re on the right track, but let’s make sure we have at least one MA order.

### Daily Blood Sugar Averages

#### TESTING FOR STATIONARITY
Dickey Fuller and KPSS tests indicate that the time series is BARELY non-stationary. This is a case where the p-level threshold can be interpreted differently if we have good reason.

#### ACF AND PACF
![Daily Averages ACF and PACF](/vis/daily_avg_acf-pacf.png)

The ACF and PACF aren't convincing that any differencing needs to be done, and because of how close the Dickey Fuller and KPSS tests were I’m going to go forward without differencing.

## Machine learning models

I tested two models and assessed their performance on the data:
<ul>
    <li>ARIMA</li>
    <li>auto_arima</li>
</ul>

## Model selection and performance

![Model Performance Comparison](/vis/all_models_performance_comparison.png)

## Final Model
**Target Variable:** bg_avg
**Model:** ARIMA (3, 0, 0)

![GDB Forecasts using ARIMA with bg_avg](/vis/arima_avg_final.png)

The predictions after fitting the model on the entire dataset were, expectedly, not as good as I saw in the training/test model. There is a fast reversion to the mean, which is exactly what you would expect to see here. Unfortunately it happens really fast and goes nowhere near the green threshold I was hoping would estimate onset. 

## Final Thoughts

### Ideas for Improvement
<ul>
	<li>Optimize ARIMA order by RMSE instead of AIC or BIC
		<ul>
			<lu>This could lead to overfitting, but since I have so little data, and only a small trend at the very end I want to focus on, I’d like to see if that actually helps with the prediction.</lu>
		</ul>
	</li>
	<li>Focus on data before meds, either by isolating that data or by giving it extra weight or duplicating it</li>
	<li>Split up training/test sets better
		<ul>
			<li>I split my data without shuffling, but because the most important trend in my data ended up in the test set I suspect my prediction results suffered</li>
		<li>I’d like to try using TimeSeriesSplit, or making 5 or so splits manually, and then averaging out the prediction results between the models</li>
		</ul>
	</li>
</ul>

### Success Criteria
How did I do?
<ol>
    <li>SUCCESS: Make predictions for dates before my data starts</li>
    <li>FAILURE: Predictions cross a threshold chosen using target blood sugar levels for pregnant people. These values depend on what I end up using as my target variable</li>
</ol>

Despite the failed predictions of the final model I still call this experiment a moderate success. The goal was to see if I could reverse a time series to make predictions in the past and I found a way to do that.
