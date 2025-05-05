# 🔄 Fyers API Automation

This tool gets the list of all inside value CPR and Camarilla Nifty50 stocks. This project automates the OAuth token flow and API request handling for the [Fyers API](https://myapi.fyers.in/), enabling secure and seamless access to trading data using a service-account-like flow. It uses encrypted token storage, auto-refresh logic, and modular API wrappers for downstream requests.

---

## 🚀 Features

* ✅ Semi automated login and token generation using `fyers-apiv3`
* 🔐 Secure token storage (encrypted at rest)
* 🔁 Token auto-refresh without user interaction
* 🌐 Configurable API request wrapper with injected auth headers
* 📦 Modular, extensible Python code for easy trading/data automation

---

## 🚠 Tech Stack

* **Python 3.10+**
* `fyers-apiv3`
* `cryptography`
* `python-dotenv`
* `requests`
* `logging`

---

## 📁 Project Structure

```
fyers-api-automation/
├── auth/
    ├── callback_server.py           # Server to take care of manual login
    ├── token_manager.py             # Encryption, decryption, save/load token
    ├── fyers_auth.py                # OAuth logic using service credentials
    └── token_data.json              # Stores the encrypted token info

├── utils/
    │── get_data.py                  # Returns the Inside value stocks
    ├── indicators.py                # Code for Cam, CPR and MAZ indicators
    ├── stock_list                   # Script to get Nifty50 stocks. RUN ONCE

├── Output/
    │── NiftyTrending_Watchlist.txt  # Trading view watch to import

├── config.py                        # Stores credentials and sensitive info
├── main.py                          # Main script

└── README.md
```

---

## ⚙️ Setup

1. **Clone the repo**

```bash
git clone https://github.com/ArutselvanManivannan/fyers-api-automation.git
cd fyers-api-automation
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create a **\`.env\`** file**

```env
CLIENT_ID=your_app_id
SECRET_KEY=your_app_secret
REDIRECT_URI=https://yourdomain.com/callback
FYERS_ID=your_fyers_id
FYERS_PASSWORD=your_password
PIN=your_4_digit_pin
ENC_KEY=your_custom_encryption_key
```

4. **Run the main script**

```bash
python main.py
```

---

## 🔐 Token Encryption

Tokens are stored locally in an encrypted format using the `cryptography` library. The encryption key is defined in your `.env` file.

---

## 🧠 How It Works

1. User has to create a app get all the necessary details to set up the API like `CLIENT_ID`, `SECRET_KEY` and so on. [Dashboard](https://login.fyers.in/?cb=https://myapi.fyers.in/dashboard)
2. User has to enter two dates which is needed to compare(manual for now, but do watch for upgrades!!)
3. Authorization is initiated. First login is manual and once successful, we'll leverage the refresh_token which is valid for 15 days for subsequent logins.
4. The script fetches the data for all Nifty50 stocks and checks for if there are any Inside value Cam and CPR stocks
5. We store all the results in the `Output` directory which is ready to be imported in TradingView.


---

## 📈 Example Usage

```python
#This is all the user needs to input once the access_token in received. On first run, an browser will be triggered to initiate the login process
from_date, to_date = '30', '02' #Hardcode dates
from_month, to_month = '04', '05' #Hardcode month(s)
```

---

## 📌 To-Do

* Create an app in Fyers Dashboard.
* Store the credentials in a `.env` file in the main directory.
* Make sure to give valid date and month values. Single digit should be prefixed with 0 like `01`

---

## 👷‍♂️ Author

Built by [Arutselvan M](https://github.com/ArutselvanManivannan)
Inspired by real-world trading automation needs 🚀
