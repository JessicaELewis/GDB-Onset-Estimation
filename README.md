# Gestational Diabetes Onset Estimation
### By Jessica Lewis
## Introduction
Gestational diabetes (GDB) is a type of diabetes that occurs during pregnancy. The placenta takes over hormone production for both the fetus and the host; in some pregnancies the placenta mismanages the uptake of blood sugar. This is what causes GDB. Without a prior diagnosis of gestational diabetes or a history of non-gestational diabetes, pregnant people are typically tested for GDB between 24 and 28 weeks of pregnancy. 
### Problem Statement
Can I reverse a time series of gestational diabetes data to pinpoint the onset in my pregnancy?
#### SUCCESS CRITERIA
There are two aspects to this project: making predictions on a reversed time series and estimating the onset of GDB in my pregnancy. I consider this project a success if either of these criteria succeed.
<ol>
    <li>I make predictions for dates before my data starts</li>
    <li>My predictions cross a threshold chosen using target blood sugar levels for pregnant people. These values depend on what I end up using as my target variable:
        <ul><li>Fasting Levels > 95</li>
            <li>Non-Fasting Levels > 130</li>
            <li>Daily average of both > 120</li>
        </ul>
    </li>
</ol>

### Context
I became pregnant in 2021 and at 27 weeks I was diagnosed with GDB. I immediately scheduled an appointment with a specialist and at 29 weeks I changed my diet and began taking blood sugar readings 4 times per day: when I woke up and an hour after each meal. I was also given carb and protein targets for meals/snacks and recorded my carb intake. I took up to 10 records per day, until I went into labor, totalling roughly 11 weeks of data.
