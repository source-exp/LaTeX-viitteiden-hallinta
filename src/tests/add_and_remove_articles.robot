*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Homepage

*** Test Cases ***
Add a journal article
    Add Reference  article  lisaa-artikkeli  Aino Laakso  Tietokannat tutkimuksessa  2022
    ...  journal=Tietojenkäsittely  volume=12  number=3  pages=45-58
    Reload
    Reference Row Should Show  lisaa-artikkeli  Artikkeli  Aino Laakso
    ...  Tietokannat tutkimuksessa  2022  Tietojenkäsittely, 12(3), 45-58

Remove a journal article
    [Documentation]  Removes the reference created by Add a journal article.
    Remove Reference And Verify It Is Gone  lisaa-artikkeli

Add a conference article
    Add Reference  conference_article  lisaa-konferenssi  Olli Niemi  Ohjelmistojen testaus  2023
    ...  booktitle=Ohjelmistotekniikan päivät
    Reload
    Reference Row Should Show  lisaa-konferenssi  Konferenssiartikkeli  Olli Niemi
    ...  Ohjelmistojen testaus  2023  Ohjelmistotekniikan päivät

Remove a conference article
    [Documentation]  Removes the reference created by Add a conference article.
    Remove Reference And Verify It Is Gone  lisaa-konferenssi

*** Keywords ***
Remove Reference And Verify It Is Gone
    [Arguments]  ${cite_key}
    ${row}=  Set Variable  css=tbody tr:has(td:text-is("${cite_key}"))
    Get Element Count  ${row}  ==  1
    Handle Future Dialogs  action=accept
    Click  ${row} >> text="Poista"
    Reload
    Get Element Count  ${row}  ==  0
