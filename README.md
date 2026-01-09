# https://chatgpt.com/c/6958a410-5f04-8324-a486-ddd1e8beeed9
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#about-jwt
- python -m venv venv
- pip install fastapi uvicorn motor
- pip install -r requirements.txt
- pip freeze > requirements.txt
- uvicorn main:app --reload
- pip install "fastapi[standard]"
- pip install motor
- python.exe -m pip install --upgrade pip