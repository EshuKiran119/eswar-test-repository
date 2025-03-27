*** Settings ***
Library    SeleniumLibrary
Resource    ../../utils/custom_keywords.py

*** Test Cases ***
Valid Login
    Open Browser    https://parabank.parasoft.com    chrome
    Input Text    id=username    admin
    Input Text    id=password    admin
    Click Button    id=loginBtn
    Location Should Contain    overview.htm
    Close Browser
