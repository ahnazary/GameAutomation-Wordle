import os

from selenium import webdriver
from FillTable import charsXpath, FillTable, absentChars, correctChars, elsewhereChars


driverPath = os.path.abspath(os.path.dirname(__file__)) + '/chromedriver_linux64/chromedriver'
driver = webdriver.Chrome(driverPath)
driver.get('https://www.wordleunlimited.com/')

initialGuess = 'crane'
guessRound = 1

fillTable = FillTable(driver)

while True:
    if guessRound == 1:
        fillTable.resetWords()
        FillTable.fillTableWithWord(initialGuess, driver)
        FillTable.evaluateGuess(driver, guessRound, initialGuess)
        fillTable.invalidWordAlert(initialGuess)
        fillTable.filterWords()
        guessRound += 1

    else:
        print(fillTable.getAllWords())
        FillTable.fillTableWithWord(fillTable.getNextGuessWords(), driver)
        FillTable.evaluateGuess(driver, guessRound, fillTable.getNextGuessWords())
        fillTable.invalidWordAlert(fillTable.getNextGuessWords())
        fillTable.filterWords()
        if fillTable.gotAllCorrect(guessRound):
            guessRound = 0
            fillTable.exitWinningMenu()
        guessRound += 1

