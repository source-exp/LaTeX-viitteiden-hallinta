*** Settings ***
Documentation  Uses the references saved earlier by the Edit References suite.
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Homepage

*** Test Cases ***
Find a book by part of its title regardless of letter case
    Search Should Return Only The Edited Book  NIMI

Find a book by part of its author name
    Search Should Return Only The Edited Book  Mallikas

Find a book by publication year
    Search Should Return Only The Edited Book  2024

Find a journal article by its title
    Search Books  Päivitetty nimi
    Get Element Count  css=tbody tr  ==  3
    Get Text  css=tbody tr:has(td:text-is("muokkaa-artikkeli-paivitetty")) > td:nth-child(1)  ==  Artikkeli

Find a conference article by its author
    Search Books  Aino Mallikas
    Get Element Count  css=tbody tr  ==  3
    Get Text  css=tbody tr:has(td:text-is("muokkaa-konferenssi-paivitetty")) > td:nth-child(1)  ==  Konferenssiartikkeli

Show a message when no books match
    Search Books  ei-osumia-876
    Get Text  role=status  ==  Hakutuloksia ei löydy.
    Get Element Count  css=tbody tr  ==  0

Clearing a search restores the reference list
    Search Books  Päivitetty nimi
    Get Element Count  css=tbody tr  ==  1
    Click  text="Tyhjennä haku"
    Get Property  id=search  value  ==  ${EMPTY}
    Get Text  css=tbody  contains  muokkaa-kirja-paivitetty
    Get Text  css=tbody  contains  muokkaa-artikkeli-paivitetty
    Get Text  css=tbody  contains  muokkaa-konferenssi-paivitetty

*** Keywords ***
Search Books
    [Arguments]  ${query}
    Fill Text  id=search  ${query}
    Click  css=form[role="search"] button

Search Should Return Only The Edited Book
    [Arguments]  ${query}
    Search Books  ${query}
    Get Element Count  css=tbody tr  ==  1
    Get Text  css=tbody tr > td:nth-child(2)  ==  muokkaa-kirja-paivitetty
