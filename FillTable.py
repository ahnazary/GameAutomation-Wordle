import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

charsXpath = {
    "q": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[1]',
    "w": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[2]',
    "e": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[3]',
    "r": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[4]',
    "t": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[5]',
    "y": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[6]',
    "u": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[7]',
    "i": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[8]',
    "o": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[9]',
    "p": '//*[@id="root"]/div/div[1]/div[11]/div[1]/div[10]',
    "a": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[1]',
    "s": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[2]',
    "d": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[3]',
    "f": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[4]',
    "g": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[5]',
    "h": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[6]',
    "j": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[7]',
    "k": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[8]',
    "l": '//*[@id="root"]/div/div[1]/div[11]/div[2]/div[9]',
    "z": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[2]',
    "x": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[3]',
    "c": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[4]',
    "v": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[5]',
    "b": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[6]',
    "n": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[7]',
    "m": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[8]',
    "enter": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[9]',
    "backspace": '//*[@id="root"]/div/div[1]/div[11]/div[3]/div[1]'

}

absentChars = []
elsewhereChars = {}
correctChars = {}
filters = []


class FillTable:
    def __init__(self, driver):
        self.driver = driver
        wordsFilePath = os.path.abspath(os.path.dirname(__file__)) + '/words_wiki.txt'
        with open(wordsFilePath) as f:
            self.words = f.readlines()

        self.words = [x for x in self.words if len(x) > 4]
        for i in range(len(self.words)):
            self.words[i] = self.words[i].lower()
        filters.append(re.compile(r"^.{5}$"))

        filters.append(re.compile(r"\s*[a-z]\w*\s*"))
        for item in filters:
            self.words = list(filter(item.match, self.words))
        filters.clear()
        self.originalWords = self.words

    @staticmethod
    def fillTableWithWord(chars, driver):
        for char in chars:
            if char != '\n':
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, charsXpath.get(char)))
                )
                element.click()
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, charsXpath.get('enter')))
        )
        element.click()

    @staticmethod
    def evaluateGuess(driver, guessRound, lastGuessedWord):
        for i in range(1, 6):
            xPath = '//*[@id="root"]/div/div[1]/div[{}]/div[{}]'.format(guessRound + 1, i)
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, xPath))
            )
            if element.get_attribute("class") == 'RowL-letter letter-absent':
                if element.text.lower() != '' or element.text.lower() is not None:
                    absentChars.append(element.text.lower())
                else:
                    xPath = '//*[@id="root"]/div/div[1]/div[{}]/div[{}]'.format(guessRound, i)
                    element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, xPath))
                    )
                    absentChars.append(element.text.lower())

            elif element.get_attribute("class") == 'RowL-letter letter-correct':
                if element.text.lower() != '' or element.text.lower() is not None:
                    correctChars[element.text.lower()] = i
                else:
                    xPath = '//*[@id="root"]/div/div[1]/div[{}]/div[{}]'.format(guessRound, i)
                    element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, xPath))
                    )
                    correctChars[element.text.lower()] = i

            elif element.get_attribute("class") == 'RowL-letter letter-elsewhere':
                if element.text.lower() != '' or element.text.lower() is not None:
                    elsewhereChars[element.text.lower()] = i
                else:
                    xPath = '//*[@id="root"]/div/div[1]/div[{}]/div[{}]'.format(guessRound, i)
                    element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, xPath))
                    )
                    elsewhereChars[element.text.lower()] = i

        for char in absentChars:
            if char in elsewhereChars or char in correctChars:
                absentChars.remove(char)

    def gotAllCorrect(self, guessRound):
        result = 0
        for i in range(1, 6):
            xPath = '//*[@id="root"]/div/div[1]/div[{}]/div[{}]'.format(guessRound + 1, i)
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, xPath))
            )
            if element.get_attribute("class") == 'RowL-letter letter-correct':
                result += 1
        if result == 5:
            return True
        else:
            return False

    def filterWords(self):
        self.words = [ele for ele in self.words if all(ch not in ele for ch in absentChars)]
        print('absent chars are', absentChars)
        absentChars.clear()
        self.words = [ele for ele in self.words if all(ch in ele for ch in elsewhereChars)]

        for key in correctChars:
            filterStr = "^"
            for i in range(1, 6):
                if i != int(correctChars[key]):
                    filterStr += '.'
                elif i == int(correctChars[key]):
                    filterStr += key
                if i == 5:
                    filterStr += '$'
            filters.append(filterStr)
            for item in filters:
                self.words = list(filter(re.compile(item).match, self.words))
        print('correct chars are ', correctChars)
        correctChars.clear()
        filters.clear()
        # print(self.words)

        for key in elsewhereChars:
            filterStr = "^"
            for i in range(1, 6):
                if i != int(elsewhereChars[key]):
                    filterStr += '.'
                elif i == int(elsewhereChars[key]):
                    filterStr += key
                if i == 5:
                    filterStr += '$'
            filters.append(filterStr)
            for item in filters:
                self.words = [re.sub(re.compile(item), "", i) for i in self.words]

        print('elsewhere chars are', elsewhereChars)
        elsewhereChars.clear()
        filters.clear()
        self.words = [x for x in self.words if len(x) > 4]

    def invalidWordAlert(self, guessedWord):
        xPath = '//*[@id="root"]/div/div[1]/div[9]'
        element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xPath))
        )
        if element.text is not None:
            for i in range(1, 6):
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, charsXpath.get('backspace')))
                )
                element.click()
            if guessedWord in self.words:
                self.words.remove(guessedWord)
            return True
        return False

    def resetWords(self):
        self.words = self.originalWords

    def exitWinningMenu(self):
        xPath = '//*[@id="root"]/div/div[1]/div[9]/div/button'
        element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xPath))
        )
        element.click()
        element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, charsXpath.get('enter')))
        )
        element.click()

    def getNextGuessWords(self):
        for word in self.words:
            if word != '' and "'" not in word:
                return word

    def getAllWords(self):
        return self.words
