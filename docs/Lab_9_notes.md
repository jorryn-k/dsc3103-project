
### Part 2 — Model Training and Persistence

**Objective:** Train a market-price prediction model and save it for use by an online prediction API.

**Implementation:** A linear regression model was trained using market, commodity, and rainfall information from the processed Parquet dataset.

Categorical features were encoded using one-hot encoding, while missing rainfall values were handled using median imputation.

The dataset was divided into training and testing subsets using an 80:20 split.

**Model artifacts:**

- `models/model.joblib` — stores the trained regression model and preprocessing pipeline.
- `models/model_metadata.json` — stores model information, feature names, training details, and evaluation metrics.

**Evaluation:**

- Mean Absolute Error (MAE): [INSERT ACTUAL RESULT]
- Root Mean Squared Error (RMSE): [INSERT ACTUAL RESULT]

**Conclusion:** Separating model training from inference allows the trained model to be loaded by an API without retraining for every request. Saving the preprocessing steps alongside the model also helps maintain consistency between training and prediction.



### Model Training Results

The market-price prediction model was trained using 889 records from the processed Parquet dataset.

The dataset was split into 711 training records and 178 testing records.

**Evaluation results:**

- Mean Absolute Error (MAE): 1,039.42
- Root Mean Squared Error (RMSE): 1,222.12

The model was saved as `models/model.joblib`, while the model configuration, features, evaluation metrics and training timestamp were saved as `models/model_metadata.json`.

The MAE indicates an average absolute prediction error of approximately 1,039 price units on the test dataset. The RMSE of 1,222.12 indicates that larger prediction errors also occurred.

The model uses market, commodity and rainfall as input features. Although the API accepts a date field, date is not currently used by the trained model.

The trained preprocessing pipeline is included in the saved model artifact, allowing the API to apply the same transformations during inference.



### API Testing and Input Validation

The trained market-price prediction model was deployed through a FastAPI service.

**Test 1: Valid prediction**

A POST request was submitted to `/predict` with the following inputs:

- Market: Kansanga
- Commodity: Beans
- Rainfall: 25 mm
- Date: 2026-11-06

The API returned HTTP 200 and a predicted price of 2,672.88.

This confirmed that the API successfully accepted the request, loaded the saved model and generated a prediction.

**Test 2: Invalid input**

A second request used the same market, commodity and date, but supplied rainfall of -50 mm.

The API returned HTTP 422 because the rainfall value violated the minimum allowed value of zero.

This demonstrated that Pydantic input validation rejected invalid data before model inference.

**Conclusion**

The API successfully served predictions and enforced input validation. Separating training from inference allows the model to be reused without retraining for each request.



### Training–Serving Skew Experiment

**Objective:** Demonstrate the consequences of inconsistent feature transformations between model training and API inference.

The model was trained using rainfall measurements in millimetres.

During the experiment, the API was deliberately modified to divide rainfall values by 1,000 before passing them to the model.

This introduced a mismatch between training and serving because a request containing 25 mm of rainfall was interpreted by the model as 0.025 mm.

**Results:**

- Original prediction: 2,672.88
- Prediction with skew: [INSERT ACTUAL RESULT]
- Prediction after restoring the API: [INSERT ACTUAL RESULT]

**Conclusion:**

Training–serving skew can cause inconsistent or inaccurate predictions when feature transformations differ between training and inference.

The problem can be prevented by sharing preprocessing logic, storing transformations with the trained model, and testing that identical inputs produce consistent results across environments.

The original API implementation was restored after the experiment.



### Training–Serving Skew Experiment — Results

The original prediction for Beans in Kansanga with 25 mm of rainfall was 2,672.88.

To simulate training–serving skew, the API was modified to divide rainfall values by 1,000 before passing them to the trained model.

The prediction decreased to 2,463.15, representing a difference of 209.73 price units, or approximately 7.85%.

This demonstrates that inconsistent feature transformations can significantly affect model predictions even when the API successfully processes the request.

The original API code was restored after the experiment.

To prevent training–serving skew, preprocessing should be shared between training and inference, feature units should remain consistent, and automated tests should verify prediction consistency.



### Docker Packaging and Reproducibility

The market-price prediction API was successfully packaged into a Docker image named `market-price-api:1.0`.

The image contains the Python runtime, required libraries, FastAPI application, trained model, and model metadata.

The container was started using port mapping `8000:8000`, making the API accessible through `http://localhost:8000`.

**Reproducibility test**

- Input: Kansanga, Beans, 25 mm rainfall, 2026-11-06
- Original local API prediction: 2,672.88
- Docker prediction: [INSERT ACTUAL RESULT]
- Prediction after restarting container: [INSERT ACTUAL RESULT]

The same input was submitted before and after restarting the container to verify prediction consistency.

The Docker image was built successfully, and the container started without errors.

**Conclusion**

Docker provides a portable execution environment for the model-serving application. Consistent predictions across container restarts demonstrate repeatability within the same image.

For stronger reproducibility, dependency versions and the base image should be pinned, and the image should be tested in a separate environment.



## Final Results and Reflections — Lab 09 Part 2

### Model Training

A Linear Regression model was trained using 889 market-price records. The dataset was split into 711 training records and 178 testing records.

The model used market, commodity and rainfall as prediction features.

The evaluation produced:

- Mean Absolute Error (MAE): 1,039.42
- Root Mean Squared Error (RMSE): 1,222.12

The trained model and preprocessing pipeline were saved in `models/model.joblib`, while model metadata was saved in `models/model_metadata.json`.

### API Development and Validation

The trained model was exposed through a FastAPI service with two endpoints:

- `GET /health` — reports the service status and model metadata.
- `POST /predict` — accepts input data and returns a predicted market price.

A valid prediction request for Beans in Kansanga with 25 mm of rainfall returned HTTP 200 and a predicted price of 2,672.88.

An invalid request containing -50 mm of rainfall returned HTTP 422, demonstrating successful input validation.

### Training–Serving Skew

Training–serving skew was simulated by dividing the rainfall input by 1,000 during inference.

The prediction changed from 2,672.88 to 2,463.15, a difference of 209.73 price units.

This demonstrated that inconsistent feature transformations can affect predictions even when the API executes successfully.

The original API implementation was restored after the experiment.

### Docker Packaging and Reproducibility

The API was packaged into a Docker image named `market-price-api:1.0`.

The container successfully loaded the trained model and exposed the API on port 8000.

The `/health` endpoint returned a successful status and confirmed that the model was loaded.

**Reproducibility results:**

| Test                     | Predicted Price |
| ------------------------ | --------------: |
| Local API                |        2,672.88 |
| Docker API               |        2,672.88 |
| Docker API after restart |        2,672.88 |

The predictions remained identical across the three tests.

### Key Lessons

1. **Training and inference should be separated.** The model should be trained beforehand, saved and loaded by the API rather than retrained for each request.
2. **Preprocessing consistency is essential.** Differences in feature units or transformations between training and serving can change predictions.
3. **Input validation improves reliability.** Invalid requests should be rejected before reaching the prediction model.
4. **Model metadata supports traceability.** Saving feature names, model type, training date and evaluation metrics makes the model easier to understand and maintain.
5. **Containerisation supports portability and repeatability.** Packaging the model and API dependencies together makes deployment more consistent. Identical predictions after restarting the container demonstrated repeatability within the tested environment.

### Limitations

The model uses only market, commodity and rainfall information. Although the API accepts a date, the current model does not use it as a prediction feature.

The model's prediction errors indicate that further feature engineering, model comparison and evaluation would be needed before using it for real-world decisions.

The Docker experiment verified consistency within one container image and environment; it did not establish reproducibility across different operating systems or servers.

### Conclusion

Lab 09 Part 2 successfully demonstrated the process of transforming a trained machine-learning model into a functioning data product.

The implementation covered model training, artifact persistence, REST API development, input validation, training–serving skew, Docker packaging and prediction reproducibility.
