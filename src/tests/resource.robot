*** Settings ***
Library  Browser

*** Variables ***
${BROWSER}   chromium
${HEADLESS}  false

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}  headless=True
    ELSE
        New Browser  browser=${BROWSER}  headless=False  slowMo=500ms
    END
    New Context

Homepage
    New Page  about:blank
    Go To  http://localhost:5001
