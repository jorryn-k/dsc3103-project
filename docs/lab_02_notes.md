\# Lab 02 Notes



I rejected rows with non-positive prices, invalid dates, and both kinds of duplicates because these are clear data errors that would break analysis. Missing markets were imputed with "Unknown" rather than dropped so that we keep as much information as possible. Commodity names were normalized to consistent title case so that "MAIZE", "maize" and "Maize" are treated as the same category.



I treated negative prices and impossible dates as errors (they cannot be real) while unusually high prices would be considered outliers that might still be valid.



If this data were later used for prediction, leakage would occur if I used information from the cleaning process that would not be available at prediction time (for example, using the global median of the whole dataset to impute values, or using future dates that would not yet exist when making a real-time prediction).

