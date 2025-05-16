# 🖼️ Real Estate Average Pricing Tool

This tool calculates the average property prices by the number of rooms from a dataset of real estate listings in Dubai. It supports implementations in both Node.js and Python, enabling data scientists and developers to compute averages efficiently using their language of choice.

## 🔍 What the Script Does

1. Fetch the remote JSON file
2. Loaded file contains real estate listings with:
   - price
   - zone
   - nr of rooms
   - surface
   - nr of bathrooms
3. Computes the average property price grouped by roomsNo
4. Saves the summarized result to the output folder

## 📊 Example Property Structure
```json
{
"ccy": "AED",
"url": "https://www.bayut.com/property/details-5646432.html",
"type": "Villa",
"zone": "Whispering Pines, Jumeirah Golf Estates, Dubai",
"price": 6800000,
"refNo": "Bayut - DUB206522",
"roomsNo": 4,
"surface": 4573,
"createdOn": "7 August 2023",
"bathroomsNo": 5
}
```
## 📁 Input

- Directory of JSON files containing Dubai property data

## 📁 Output

- JSON file results.json saved to /data/outputs with average prices like:
```json
{
"1": {
"totalPrice": 1000000,
"count": 2,
"averagePrice": 500000.0
},
"3": {
"totalPrice": 2500000,
"count": 2,
"averagePrice": 1250000.0
}
}
```
## How to run your algorithm on Ocean Node

```bash
1. Open Ocean Protocol vscode-extension
2. Select Algorithm file
3. Select Results folder
4. Press Start Compute Job
```

# Python

### Use existing docker image `oceanprotocol/c2d_examples:py-general`:

- Docker image: `oceanprotocol/c2d_examples`
- Docker tag: `py-general`

# Node

### Use existing docker image `oceanprotocol/c2d_examples:js-general`:

- Docker image: `oceanprotocol/c2d_examples`
- Docker tag: `js-general`
### Zeptabot (Brad) : I improved the prediction accuracy by using a Random Forest Regressor ML algorithm, incorporating all meaningful features, and implemented a 80: 20 Train-Test Split. I achieved a high prediction accuracy with a Coefficient of determination of 82.5% through this approach.