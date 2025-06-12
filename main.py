import streamlit as st
from PIL import Image, UnidentifiedImageError
import io
import pillow_heif

# Register HEIF support
pillow_heif.register_heif_opener()

st.markdown(
    "<h1 style='text-align: center;'>Image Extension Converter</h1>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    input_option = st.selectbox("Select input image type", ("heic", "png", "jpg", "jpeg"))

with col2:
    output_option = st.selectbox("Select output image type", ("png", "jpg", "jpeg"))

# Upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "heic"])

if uploaded_file:

    convert_button = st.button("Convert")

    format_mapping = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        # Add more formats if needed
    }

    img_format = format_mapping.get(output_option)

    # Convert the image to a defined type
    if convert_button:
        try:
            img = Image.open(uploaded_file)
            buffer = io.BytesIO()
            img.save(buffer, format=img_format)
            buffer.seek(0)

            converted_image = Image.open(buffer)
            st.image(img, width=300)

            # Download button
            st.download_button(
                label="Download",
                data=buffer,
                file_name=f"converted_image.{output_option}",
                mime="image/png"
            )

        except UnidentifiedImageError:
            st.error("Failed to identify the image file. Please upload a supported and valid image.")
        except KeyError:
            st.error(f"Saving in the selected format '{output_option}' is not supported.")
        except Exception as e:
            st.error("An unexpected error occurred while processing the image.")
            st.text(f"Error details: {e}")