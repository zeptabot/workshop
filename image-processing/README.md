# 🖼️ Image Processing Tool

This tool is designed to apply various image filters to images using image processing libraries. It can process images from URLs and apply different types of filters including blur, grayscale, and unsharp mask.

## 🔍 What the Script Does

1. Fetches an image from a specified URL
2. Applies one of the following filters:
   - Gaussian Blur
   - Grayscale conversion
   - Unsharp Mask
3. Saves the processed image to the output directory

## 📊 Available Filters

| Filter      | Description                                    |
| ----------- | :--------------------------------------------: |
| `blur`      | Applies Gaussian blur with radius 5           |
| `grayscale` | Converts the image to grayscale               |
| `unsharp`   | Applies unsharp mask filter with radius 5     |

## 📁 Input

- Image URL (currently set to a sample Lena image)
- Filter type to apply

## 📁 Output

- Processed image saved as `filtered_image.png` in the `/data/outputs` directory

# Python
## Requirements

- Python 3.8+
- Pillow (PIL)
- requests

### Install dependencies:

```bash
pip install Pillow requests
```

### Use existing docker image `oceanprotocol/c2d_examples:py-general`:
- Docker image: `oceanprotocol/c2d_examples`
- Docker tag: `py-general`

# Node
## Requirements

- Node.js 18+
- sharp
- axios

### Install dependencies:

```bash
npm install sharp axios
```

### Use existing docker image `oceanprotocol/c2d_examples:js-general`:
- Docker image: `oceanprotocol/c2d_examples`
- Docker tag: `js-general`


