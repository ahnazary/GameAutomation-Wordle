import os

from selenium import webdriver
from FillTable import charsXpath, FillTable, absentChars, correctChars, elsewhereChars


driverPath = os.path.abspath(os.path.dirname(__file__)) + '/chromedriver_linux64/chromedriver'
driver = webdriver.Chrome(driverPath)
driver.get('https://www.wordleunlimited.com/')

initialGuess = 'beast'
guessRound = 1

fillTable = FillTable()

FillTable.fillTableWithWord(initialGuess, driver)
FillTable.evaluateGuess(driver, guessRound, initialGuess)
print(FillTable.gotAllCorrect(driver, guessRound, fillTable.getNextGuessWords()))
fillTable.filterWords()
guessRound += 1

print(fillTable.getAllWords())
FillTable.fillTableWithWord(fillTable.getNextGuessWords(), driver)
FillTable.evaluateGuess(driver, guessRound, fillTable.getNextGuessWords())
print(FillTable.gotAllCorrect(driver, guessRound, fillTable.getNextGuessWords()))
fillTable.filterWords()
guessRound += 1


print(fillTable.getAllWords())
FillTable.fillTableWithWord(fillTable.getNextGuessWords(), driver)
FillTable.evaluateGuess(driver, guessRound, fillTable.getNextGuessWords())
print(FillTable.gotAllCorrect(driver, guessRound, fillTable.getNextGuessWords()))
fillTable.filterWords()
guessRound += 1

print(fillTable.getAllWords())
FillTable.fillTableWithWord(fillTable.getNextGuessWords(), driver)
FillTable.evaluateGuess(driver, guessRound, fillTable.getNextGuessWords())
print(FillTable.gotAllCorrect(driver, guessRound, fillTable.getNextGuessWords()))
fillTable.filterWords()
guessRound += 1