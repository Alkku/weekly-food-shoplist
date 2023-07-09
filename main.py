from bs4 import BeautifulSoup
from tqdm import tqdm
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


    foods = ['liha', 'kala', 'jauheliha', 'broileri']
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

                lists = soup.find_all('a', class_="StyledCardWrapper-sc-1x87nsj dJJHhy recipe-card search-result-card")
                i = 0
                for list in lists:  # Take the 50 highest ranked recipes per food category
                    i += 1
                    foodName = list.find("div",
                                         class_="CardTitle-sc-i9wkow RecipeCardTitle-sc-7be5j4 eNyUcv xmKgT recipe-card-title").text.replace(
                        '\n', '')
                    timeToMake = list.find("div",
                                         class_="StyledCookingTime-sc-1wzbg24 cBCVbc").text.replace(
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
    for recipe in tqdm(range(len(chosenRecipes))):
        url = "https://www.valio.fi" + str(chosenRecipes[recipe][2])
        dataframe = pd.read_html(url)

        if recipe == 0:
            df1 = pd.DataFrame(dataframe[0])
            df1.columns = ['MÄÄRÄ', 'AINESOSA']
        elif recipe == 1:
            df2 = pd.DataFrame(dataframe[0])
            df2.columns = ['MÄÄRÄ', 'AINESOSA']
        elif recipe == 2:
            df3 = pd.DataFrame(dataframe[0])
            df3.columns = ['MÄÄRÄ', 'AINESOSA']
        elif recipe == 3:
            df4 = pd.DataFrame(dataframe[0])
            df4.columns = ['MÄÄRÄ', 'AINESOSA']
        else:
            df5 = pd.DataFrame(dataframe[0])
            df5.columns = ['MÄÄRÄ', 'AINESOSA']

    all_frames = [df1, df2, df3, df4, df5]
    result = pd.concat(all_frames)
    drop_rows = result[(result['MÄÄRÄ'] == result['AINESOSA'])].index
    result.drop(drop_rows, inplace=True)
    return result.sort_values(by=['AINESOSA'])


def computeIngredients(ingredient_df):
    # Let's find all the duplicates
    duplicate_ingredients = ingredient_df.duplicated(keep=False, subset=["AINESOSA"])
    duplicate_ingredients.name = 'DUPLICATES'
    concat_duplicates = pd.concat([ingredient_df, duplicate_ingredients], axis=1)
    save_concat_duplicates = concat_duplicates
    new_df = concat_duplicates[(concat_duplicates['DUPLICATES'] == True)]
    duplicates_list = new_df.values.tolist()

    # We create new list to eliminate duplicates.
    cleansed_list = []
    for i in range(len(duplicates_list)):
        if i == 0:
            new_amount = ""
        elif i > 0 and "+" not in new_amount and duplicates_list[i-1][1] == duplicates_list[i][1]:
            new_amount = str(duplicates_list[i-1][0]).replace(" ","") + ' + ' + str(duplicates_list[i][0]).replace(" ","")
        elif i > 0 and "+" in new_amount and duplicates_list[i-1][1] == duplicates_list[i][1]:
            new_amount = new_amount + ' + ' + str(duplicates_list[i][0]).replace(" ","")
            if i == len(duplicates_list)-1:
                cleansed_list.append([new_amount, duplicates_list[i][1]])
        elif i > 0 and duplicates_list[i-1][1] != duplicates_list[i][1]:
            cleansed_list.append([new_amount, duplicates_list[i-1][1]])
            new_amount = ""

    df_cleansed_list = pd.DataFrame(cleansed_list)
    df_cleansed_list.columns = ['MÄÄRÄ', 'AINESOSA']
    dup_cleansed_list = save_concat_duplicates.drop_duplicates(subset=['AINESOSA'], keep=False)
    new_dup_cleansed = dup_cleansed_list.drop('DUPLICATES', axis=1)
    final_dataframe = pd.concat([new_dup_cleansed, df_cleansed_list])
    return final_dataframe




def sendEmail(final_dataframe, recipe_and_urls):
    pass
    # We create the final print




















while programRunning:
    acquiredFoodList = fetchRecipes()
    print(acquiredFoodList)
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
            recipeListNotDone = False
        elif int(changeRecipeNr) not in range(1,6):
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


    readyForMail = computeIngredients(fetchedRecipes)




    print(fiveRandomRecipesList)
    print(readyForMail)
    #acquiredEmail = inputEmail(readyForMail, fiveRandomRecipesList)
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