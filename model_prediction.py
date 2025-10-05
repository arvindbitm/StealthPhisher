import tensorflow as tf
import joblib
import numpy as np
import pandas as pd

FEATURES = [
    'DomainLengthOfURL', 'URLComplexity', 'IsResponsive', 'HasPaymentKey', 'CntEmptyRef', 'HasIFrame', 'CntImages',
    'URLOtherSpclCharRatio', 'LineOfCode', 'HasSocialMediaPage', 'CharacterComplexity', 'CntSelfHRef',
    'NumberOfSubdomains', 'IsSelfRedirects', 'HavingPath', 'TLDLength', 'CntIFrame', 'URLLetterRatio',
    'HavingAnchor', 'LongestLineLength', 'HasSubmitButton', 'HasHiddenFields', 'HasFavicon', 'HasRobotsBlocked',
    'HasDescription', 'UniqueFeatureCnt', 'CntFilesJS', 'URLDigitRatio', 'IsURLRedirects', 'IsDomainIP',
    'CntExternalRef', 'CntFilesCSS', 'HasSSL', 'HasTitle', 'LengthOfURL', 'WAPBenign', 'FractalDimension',
    'LikelinessIndex', 'HexPatternCnt'
]
# Load ML models & scaler
def load_models_and_scaler(hybrid_model_path, tabnet_model_path, scaler_path):
    # Load the hybrid model (Wide & Deep)
    hybrid_model = tf.keras.models.load_model(hybrid_model_path)
    hybrid_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Load the TabNet model (saved using TensorFlow's model.save())
    tabnet_model = tf.keras.models.load_model(tabnet_model_path)

    # Load the scaler
    scaler = joblib.load(scaler_path)

    return hybrid_model, tabnet_model, scaler
hybrid_model, tabnet_model, scaler = load_models_and_scaler('full_hybrid_model.h5', 'tabnet_model.h5', 'scaler.pkl')

# Preprocess features
def extract_features(features):
    processed_features = []
    for col in FEATURES:
        value = features.get(col, 0)
        if isinstance(value, bool):
            value = int(value)
        elif isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                value = 0
        processed_features.append(value)
    return np.array(processed_features)


def preprocess_url(features, scaler):
    features_array = extract_features(features)
    features_df = pd.DataFrame([features_array], columns=FEATURES)
    features_scaled = scaler.transform(features_df)
    return features_scaled

# Predict TabNet output
def predict_tabnet(tabnet_model, features):
    features_array = extract_features(features).reshape(1, -1)
    features_array = features_array.astype(np.float32)
    tabnet_prediction = tabnet_model.predict(features_array)
    return tabnet_prediction
# def predict_tabnet(tabnet_model, features):
#     features_array = extract_features(features).reshape(1, -1)
#     tabnet_prediction = tabnet_model.predict(features_array)  # Direct prediction from TabNet
#     return tabnet_prediction

# Predict with hybrid ML model
def predict_hybrid(features, hybrid_model=hybrid_model, tabnet_model=tabnet_model, scaler=scaler):
    processed_url = preprocess_url(features, scaler)
    wide_input = processed_url
    deep_input = processed_url
    tabnet_input = predict_tabnet(tabnet_model, features)
    prediction = hybrid_model.predict([wide_input, deep_input, tabnet_input], verbose=0)
    benign_probability = prediction[0][0] * 100
    phishing_probability = (1 - prediction[0][0]) * 100
    classification = "Benign" if prediction[0][0] > 0.5 else "Phishing"
    return classification, phishing_probability, benign_probability
