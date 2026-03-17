from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {}
accounts = {}

@app.get("/")
def root():
    return {"message": "Bank API running"}

@app.post("/register")
def register(username: str, password: str):
    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[username] = {"password": password}
    return {"message": "User created"}

@app.post("/login")
def login(username: str, password: str):
    if username not in users or users[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}

@app.post("/create-account")
def create_account(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    account_id = len(accounts) + 1
    accounts[account_id] = {
        "id": account_id,
        "user": username,
        "balance": 0
    }
    return accounts[account_id]

@app.get("/accounts")
def get_accounts():
    return accounts

@app.post("/deposit")
def deposit(account_id: int, amount: float):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    accounts[account_id]["balance"] += amount
    return accounts[account_id]

@app.post("/withdraw")
def withdraw(account_id: int, amount: float):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    if accounts[account_id]["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    accounts[account_id]["balance"] -= amount
    return accounts[account_id]
