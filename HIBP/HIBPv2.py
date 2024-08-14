import requests

def checkIfEmailIsPawned(f_emailID):
    url2 = "https://haveibeenpwned.com/api/breachedaccount/" + f_emailID
    print("Trying the request to the URL: ", url2)

    #Send get request and save response
    response = requests.get(url2, params)

    #Change response from string to List
    response_JSON = response.json()
    for item in response_JSON:
        #print(item)
        #print(typeof(item))
        print(item['Name'])
        print (item['DataClasses'])
    return

if __name__== "__main__":
    emailID = "shahrukhvp@gmail.com"
    url1 = "GET https://haveibeenpwned.com/api/v2/breaches"
    params = {'User-Agent': 'Mozilla'}
    checkIfEmailIsPawned(emailID)