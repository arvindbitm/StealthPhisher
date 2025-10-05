import tensorflow as tf
import joblib
import numpy as np
import pandas as pd
import os

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from plqfa_new_feature import *  # Ensure this module is correctly implemented

# Define the feature set (this should include all the features used during training, excluding the label column)
fs = ['DomainLengthOfURL', 'URLComplexity', 'IsResponsive', 'HasPaymentKey', 'CntEmptyRef', 'HasIFrame', 'CntImages', 'URLOtherSpclCharRatio', 'LineOfCode', 'HasSocialMediaPage',
            'CharacterComplexity', 'CntSelfHRef', 'NumberOfSubdomains','IsSelfRedirects', 'HavingPath', 'TLDLength', 'CntIFrame', 'URLLetterRatio', 
            'HavingAnchor', 'LongestLineLength', 'HasSubmitButton', 'HasHiddenFields', 'HasFavicon', 'HasRobotsBlocked', 'HasDescription', 'UniqueFeatureCnt', 'CntFilesJS', 'URLDigitRatio',
              'IsURLRedirects', 'IsDomainIP', 'CntExternalRef', 'CntFilesCSS', 'HasSSL', 'HasTitle', 'LengthOfURL', 'WAPBenign', 'FractalDimension', 'LikelinessIndex',
                'HexPatternCnt']

# Load the OfflineDataSet.csv
def load_dataset(file_path):
    return pd.read_csv(file_path)

# Feature extraction function (used during training)
def extract_features(url, features):
    extracted_features = {col: features[col] for col in fs if col in features}
    return np.array([extracted_features.get(col, 0) for col in fs])

# Load model and scaler
def load_model_and_scaler(model_path, scaler_path):
    model = tf.keras.models.load_model(model_path)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  # Recompile the model
    scaler = joblib.load(scaler_path)
    return model, scaler

# Preprocess the URL (scale the extracted features)
def preprocess_url(url, features, scaler):
    features_array = extract_features(url, features)
    features_df = pd.DataFrame([features_array], columns=fs)
    features_scaled = scaler.transform(features_df)
    return features_scaled

# Predict URL classification
def predict_url(model, url, features, scaler):
    processed_url = preprocess_url(url, features, scaler)
    wide_input = processed_url
    deep_input = processed_url
    prediction = model.predict([wide_input, deep_input], verbose=0)
    benign_probability = prediction[0][0] * 100  # Convert to percentage
    phishing_probability = (1 - prediction[0][0]) * 100

    classification = 1 if prediction[0][0] > 0.5 else 0

    return classification, phishing_probability, benign_probability

# Main function
if __name__ == "__main__":
    dataset = load_dataset("OfflineDataSet.csv")
    model, scaler = load_model_and_scaler("wide_deep_model.h5", "scaler.pkl")

    # Get the last row (latest URL) from the dataset
    latest_row = dataset.iloc[-1]
    url = latest_row['URL']
    features = latest_row.drop('URL').to_dict()

    # Predict for the latest URL
    classification, phishing_probability, benign_probability = predict_url(model, url, features, scaler)

    print(f"{url}is classified as: {'Phishing' if classification == 0 else 'Benign'}")
    print(f"Phishing Probability: {phishing_probability:.2f}%")
    print(f"Benign Probability: {benign_probability:.2f}%\n")