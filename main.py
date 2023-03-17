from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random


programRunning = True
recipeListNotDone = True
fiveRandomRecipesList = []
usedIndexList = []
ingredientList = []
finalIngredientList = []


def fetchRecipes():
    driver = webdriver.Chrome(service=Service('C:/git/Weekly_Food_Shoplist/weekly-food-shoplist/chromedriver.exe'))
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)


    foods = ['liha', 'kala', 'jauheliha']
    finalFoodList = []

    for i in range(len(foods)):
        driver.get("https://www.valio.fi/reseptit/haku/?ruokalaji=paaruoat&raaka-aineet=" + str(
            foods[i]) + "&jarjestys=suosituimmat")
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        previous_height = driver.execute_script('return document.body.scrollHeight')

        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(0.5)
            new_height = driver.execute_script('return document.body.scrollHeight')

            if new_height == previous_height:
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                lists = soup.find_all('a', class_="StyledCardWrapper-sc-83brm2 dYMhnT recipe-card search-result-card")
                i = 0
                for list in lists:  # Take the 50 highest ranked recipes per food category
                    i += 1
                    foodName = list.find("div",
                                         class_="CardTitle-sc-q66kkn RecipeCardTitle-sc-agd8pc iBoraM fwfgnt recipe-card-title").text.replace(
                        '\n', '')
                    timeToMake = list.find("div",
                                         class_="StyledCookingTime-sc-8fvacb iLRGmH").text.replace(
                        '\n', '')
                    recipeUrlEnding = list['href']

                    foodNameList = [foodName.lower(), timeToMake, recipeUrlEnding]

                    finalFoodList.insert(i, foodNameList)
                    if i == 50:
                        break
                break
            previous_height = new_height
    print(finalFoodList)
    return finalFoodList


def swapChoice(changeRecipeNr, fiveRandomRecipesList, acquiredFoodList):
    pickNewRandomRecipe = random.choice(acquiredFoodList)
    acquiredFoodList.remove(pickNewRandomRecipe)
    fiveRandomRecipesList[int(changeRecipeNr)-1] = pickNewRandomRecipe
    return fiveRandomRecipesList


def inputEmail():  # Run this later in the program
    emailAddress = input("Anna sähköposti: ")
    return emailAddress


def fetchRecipeWebsites(chosenRecipes): #This should return list of ingredients for each recipe
    #drive = webdriver.Chrome(service=Service('C:/git/Weekly_Food_Shoplist/weekly-food-shoplist/chromedriver.exe'))
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #drive = webdriver.Chrome(options=chrome_options)
    url = "https://www.valio.fi/reseptit/jauheliha-nachos-1/"
    df = pd.read_html(url)-
    print(df[0])



    #for recipe in range(len(chosenRecipes)):

        #url = "https://www.valio.fi" + str(chosenRecipes[recipe][2])
        #df = pd.read_html(url)
        #df[0].rename(columns={"0": "Määrä", "1": "Ainesosa"})



        #If valuecolumn1 = valuecolumn2 -> delete








        #print(chosenRecipes[recipe][2])
        #drive.get("https://www.valio.fi" + str(chosenRecipes[recipe][2]))
        #html = drive.page_source
        #soup = BeautifulSoup(html, 'html.parser')
        #lists = soup.find_all('tr')

        #i = 0
        #for list in lists:

            #trythis = list.find("span").text.replace('\n', '')
            #ingredientAmount = list.find("td", class_="IngredientRowLeft-sc-25fwcz cXfQpc").text.replace('\n', '')
            #ingredientName = list.find("div", class_="IngredientRowRightContainer-sc-egmiky dSBYXk")
            #ingredientList = [ingredientName]
            #finalIngredientList.insert(i, ingredientList)
            #i += 1
            #print(finalIngredientList)
    #print(finalIngredientList)



    #return finalIngredientList"""""


def computeIngredients():
    pass


def sendEmail():
    pass


while programRunning:
    acquiredFoodList = fetchRecipes()
    print("----------------------------------------------------------------------------")

    for i in range(5):
        pickRandomRecipe = random.choice(acquiredFoodList)
        acquiredFoodList.remove(pickRandomRecipe)
        fiveRandomRecipesList.append(pickRandomRecipe)
        print(str(i + 1) + ". " + pickRandomRecipe[0].capitalize().ljust(45) + 'Valmistusaika: ' + pickRandomRecipe[1])
        #firstListChoices.append(pickRandomRecipe)
    print("----------------------------------------------------------------------------")

    while recipeListNotDone:
        changeRecipeNr = input("Anna vaihdettavan reseptin numero tai jätä tyhjäksi (Enter): ")
        print("----------------------------------------------------------------------------")
        if changeRecipeNr == "":
            fetchedRecipes = fetchRecipeWebsites(fiveRandomRecipesList)
            #print(fetchedRecipes)
            recipeListNotDone = False
        elif int(changeRecipeNr) not in range(1,6) or isinstance(changeRecipeNr, (int, float)) == False:
            print("Arvo ei ole 1 ja 5 välillä. Anna uusi arvo.")
            print("----------------------------------------------------------------------------")
        elif len(acquiredFoodList) == 0:
            print("Reseptit loppuivat listasta.")
            time.sleep(5)
            break
        else:
            newList = swapChoice(changeRecipeNr, fiveRandomRecipesList, acquiredFoodList)
            for elements in range(len(newList)):
                print(str(elements + 1) + ". " + str(newList[elements][0]).capitalize().ljust(45) + 'Valmistusaika: ' + newList[elements][1])
            print("----------------------------------------------------------------------------")








    # acquiredEmail = inputEmail()
    break

    # Program should:
    # Find website with recipes in Finnish (DONE)
    # Generate first the 5 recipes, then if accepted, send to email. You should also be able to choose only 1
    # Have keywords like Maksalaatikko, Lihamakaronilaatikko, Lasagne, Lihamureke and put in list
    # Feed keywords and based on this fetch recipe from e.g. Valios page
    # Fetch e.g. 5 recipes for one week of food -> Check if one recipe requires 2 eggs, other 3 eggs, sum these to 5 eggs.
    # List also the recipes as URL, but make purchase list simple, no duplicates
    # Send the buy list as email to inputted email

    # Should look like this output:
    # Lihamakaranoilaatikko, http://www.valio....makaronilaatikko
    # -//-
    # -//-
    # ...
    # OSTOSLISTA
    # 2 kananmunaa
    # 1 litra maitoa (no duplicates)