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

Add Reference
    [Arguments]  ${type}  ${cite_key}  ${author}  ${title}  ${year}  &{details}
    Click  text="Lisää viite"
    Select Options By  id=reference_type  value  ${type}
    Fill Reference Fields  ${cite_key}  ${author}  ${title}  ${year}  &{details}
    Click  button[type="submit"]
    Get Text  role=status  ==  Viite lisättiin onnistuneesti.

Fill Reference Fields
    [Arguments]  ${cite_key}  ${author}  ${title}  ${year}  &{details}
    Fill Text  id=cite_key  ${cite_key}
    Fill Text  id=author  ${author}
    Fill Text  id=title  ${title}
    Fill Text  id=year  ${year}
    FOR  ${field}  ${value}  IN  &{details}
        Fill Text  id=${field}  ${value}
    END

Reference Row Should Show
    [Arguments]  ${cite_key}  ${type_label}  ${author}  ${title}  ${year}  ${details}
    ${row}=  Set Variable  css=tbody tr:has(td:text-is("${cite_key}"))
    Get Text  ${row} > td:nth-child(1)  ==  ${type_label}
    Get Text  ${row} > td:nth-child(2)  ==  ${cite_key}
    Get Text  ${row} > td:nth-child(3)  ==  ${author}
    Get Text  ${row} > td:nth-child(4)  ==  ${title}
    Get Text  ${row} > td:nth-child(5)  ==  ${year}
    Get Text  ${row} > td:nth-child(6)  ==  ${details}
