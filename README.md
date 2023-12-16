# Minilab3

# Tracking & Financial Accounting application for cryptocurrency traffic arbitrage

This is a python application for financial accounting of cryptocurrency traffic arbitrage. 
You can track market prices and growth trends right there.

1. **Add the new deal into Database:** `/add_deal`
2. **Get the current rates of BTC, TON, ETH, USDT, BNB:** `/update_rates`
3. **Get margin and spread for a certain period:** `/filter_deals`

## Prerequisites

Make sure you have the following installed:

- Python (version 3.x)
- Requests library (`pip install requests`)
- Flask library (`pip install flask`)
- Flask SQLAlchemy (`pip install flask_sqlalchemy`)

## Usage

Run the application using the following command:

```
python source/app.py
```

The application will start serving on port 5000.

## Installion

1) You have to clone this repository on your own device
2) You have to create 'config.py' file in 'source' folder
3) You have to get the API key on https://www.coinapi.io/ website and write "API_KEY" = *your_api_key*

## Endpoints

### 1. Add the new deal into Database

   - **Endpoint:** `/add_deal`

   - **Parameters:**
    - `amount_rub`: Transaction amount in fiat currency.
    - `cryptocurrency`: Name of circulating cryptocurrency
    - `exchange_rate`: Deal Rate "Crypto/Fiat"
    - `deal_type`: Type of deal (Buying or selling)
    - `creating_time`: Time of deal creation
     

   - **Example:**
     ```
     http://127.0.0.1:5000/add_deal?amount_rub=5000&cryptocurrency="BTC"&exchange_rate=3600000&deal_type="Продажа"&creating_time=2023-12-02T14:30
     ```

### 2. Get the current rates of BTC, TON, ETH, USDT, BNB

   - **Endpoint:** `/update_rates`
     

   - **Example:**
     ```
     http://127.0.0.1:5000/update_rates
     ```

### 3. Get the margin and spread in the chosen period

   - **Endpoint:** `/filter_deals`

   - **Parameters:**
    - `start_date`: time, which is the left boundary of the sample
    - `end_date`: time, which is the right boundary of the sample

   - **Example:**
     ```
     http://127.0.0.1:5000/filter_deals?start_date=2023-11-30T18:36&end_date=2023-12-01T19:36
     ```

