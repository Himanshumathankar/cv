import streamlit as st
import os
import numpy as np
from model import get_features
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

st.title("👕 Outfit Recommendation System")

uploaded_file = st.file_uploader("Upload an outfit image", type=["jpg", "png"])

dataset_path = "dataset/"
dataset_features = []
image_paths = []

# Precompute dataset features
# for img_name in os.listdir(dataset_path):
#     path = os.path.join(dataset_path, img_name)
#     image_paths.append(path)
#     dataset_features.append(get_features(path))

for img_name in os.listdir(dataset_path):
    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    path = os.path.join(dataset_path, img_name)
    image_paths.append(path)
    dataset_features.append(get_features(path))

dataset_features = np.vstack(dataset_features)

if uploaded_file:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    query_feature = get_features("temp.jpg")

    similarities = cosine_similarity(query_feature, dataset_features)[0]
    top_indices = similarities.argsort()[-3:][::-1]

    st.image(uploaded_file, caption="Uploaded Image")

    st.subheader("Recommended Outfits:")
    for idx in top_indices:
        st.image(image_paths[idx])