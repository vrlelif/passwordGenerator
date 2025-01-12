from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
import string
import freecurrencyapi
import re
import os
from dotenv import dotenv_values

#create app
app = FastAPI() 

#get index template from templates
templates = Jinja2Templates(directory="../templates/") 

#-----------------------------PASSWORD GENERATION---------------------------------------
#define path and return type for GET
@app.get("/generate-password",response_class=HTMLResponse) 
async def home(request: Request): # return index page for GET
    return templates.TemplateResponse("index.html", {"request": request, "password": None})

@app.post("/generate-password", response_class=HTMLResponse) #define path and return type for POST
async def generate_password( request: Request, # define function to generate password
    length: int = Form(...),
    includeWord: str = Form('')) :
    try:
        if length < 5 or length > 30: # check length
            raise HTTPException(
                status_code=400, 
                detail="You should provide a length between 5 and 30 for your password."
        ) #check if shorten than 5 digits

        if len(includeWord) >= length : #check if word included is shorter than required length
            raise HTTPException(
                status_code=400, 
                detail="The word you want to include must be shorter than the required length for password."
        )

        if not isinstance(includeWord, str) : #check if word included is a string
            raise HTTPException(
                status_code=400, 
                detail="Word to include must be string"
        )
        
        lowerCase = string.ascii_lowercase  #lowercase letters
        upperCase = string.ascii_uppercase  #uppercase letters
        numbers = string.digits #numbers
        specialChars = "!@#$%^&*()-_+=" #special characters
        charList = lowerCase + upperCase + numbers + specialChars

        #create password subtracting the length of word wanted from reqired password length
        password = ''.join(random.choices(charList, k=(length)-len(includeWord))) 

        #check length of password to generate a random index
        randomIndex = random.randint(0, len(password)) 

        # add word wanted in a random index
        if includeWord : 
            password = password[:randomIndex] + includeWord + password[randomIndex:] 

        return templates.TemplateResponse( # add result to html
            "index.html",
            {"request": request, "password": password, "length": len(password), "error": None}
        )
    
    except HTTPException as e:  # and any HTTP exceptions
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "password": None, "error": e.detail}
        )
    except Exception as e: # any other exceptions
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "password": None, "error": "An unexpected error occurred: " + str(e)}
        )

#-----------------------------PASSWORD SECURITY CHECK---------------------------------------
@app.get("/check-password",response_class=HTMLResponse) 
async def home(request: Request):# return index page for GET
    return templates.TemplateResponse("checkPassword.html", {"request": request, "password": None}) 

@app.post("/check-password", response_class=HTMLResponse) #define path and return type for POST
async def check_password( request: Request, # define function to generate password
    password: str = Form(...)) :
    try:
        if len(password) < 5 : # check length
            raise HTTPException(
                status_code=400, 
                detail="You should provide a password.Must be longer than 5 digits"
        ) #check if shorten than 5 digits
        if len(password) < 12:
            isSecure =  False
         # Check for at least one lowercase letter
        elif not re.search(r'[a-z]', password):
            isSecure = False

        # Check for at least one uppercase letter
        elif not re.search(r'[A-Z]', password):
            isSecure = False

        # Check for minimum one digit
        elif not re.search(r'[0-9]', password):
            isSecure = False

        # Check for minimum one special character
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            isSecure = False

        # Check if the password do not have a guessable patterns
        elif password in ["password", "123456", "qwerty", "abcdef"]:
            isSecure = False

        # If all checks pass, the password is secure
        else :  
            isSecure = True
        result = ''
        if not isSecure : 
            result = "Not Secure"
        else:
            result = "Secure"
                
        return templates.TemplateResponse( # add result to html
            "checkPassword.html",
            {"request": request, "result": result , "error": None}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "checkPassword.html",
            {"request": request, "result": result, "password" : password, "error": f"An unexpected error occurred: {str(e)}"}
        )

#-----------------------------CURRENCY CONVERSION---------------------------------------

config = dotenv_values(".env") 
APIKey = os.getenv("CONVERSION_API")
currencyApp = freecurrencyapi.Client('fca_live_qXZpyqRjfl6Ya0hKcpOH6cPxviWkUzDIsIaNw72e')
currencyList = currencyApp.currencies()



@app.get("/get-conversion",response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("currency.html", {"request": request, "currencyList":currencyList}) # return index page for GET

@app.post("/get-conversion", response_class=HTMLResponse)
async def convert_currency(
    request: Request,
    amount: float = Form(...),
    baseCurrency: str = Form(...),
    currency: str = Form(...)):
    try:
        data = currencyApp.latest(baseCurrency)
        exchangeRate = data['data'][f'{currency}']

        # get result 
        result = {
            "baseCurrency": baseCurrency,
            "targetCurrency": currency,
            "amount": amount,
            "exchangeRate": exchangeRate,
            "convertedAmount": round(amount * exchangeRate, 2),
        }

        # send result to the template
        return templates.TemplateResponse(
            "currency.html",
            {"request": request, "result": result, "error": None ,"currencyList": currencyList}
        )

    except HTTPException as e:
        return templates.TemplateResponse(
            "currency.html",
            {"request": request, "result": None, "error": e.detail}
        )

    except KeyError as e:
        return templates.TemplateResponse(
            "currency.html",
            {"request": request, "result": None, "error": f"Missing key in data: {str(e)}"}
        )

    except Exception as e:
        return templates.TemplateResponse(
            "currency.html",
            {"request": request, "result": None, "error": f"An unexpected error occurred: {str(e)}"}
        )
