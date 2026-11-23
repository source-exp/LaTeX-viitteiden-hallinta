*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Homepage
Test Template  Edit Reference And Verify The Saved Changes

*** Variables ***
&{BOOK_BEFORE}          publisher=Vanha kustantaja
&{BOOK_AFTER}           publisher=Uusi kustantaja
&{ARTICLE_BEFORE}       journal=Vanha julkaisu  volume=12  number=3  pages=45-58
&{ARTICLE_AFTER}        journal=Uusi julkaisu  volume=14  number=2  pages=21-34
&{CONFERENCE_BEFORE}    booktitle=Vanha konferenssi
&{CONFERENCE_AFTER}     booktitle=Uusi konferenssi

*** Test Cases ***
Edit a book
    book  Kirja  muokkaa-kirja  ${BOOK_BEFORE}  ${BOOK_AFTER}  Uusi kustantaja

Edit a journal article
    article  Artikkeli  muokkaa-artikkeli  ${ARTICLE_BEFORE}  ${ARTICLE_AFTER}
    ...  Uusi julkaisu, 14(2), 21-34

Edit a conference article
    conference_article  Konferenssiartikkeli  muokkaa-konferenssi
    ...  ${CONFERENCE_BEFORE}  ${CONFERENCE_AFTER}  Uusi konferenssi

*** Keywords ***
Edit Reference And Verify The Saved Changes
    [Arguments]  ${type}  ${type_label}  ${cite_key}  ${old_details}  ${new_details}  ${expected_details}
    Add Reference  ${type}  ${cite_key}  Eeva Esimerkki  Alkuperäinen nimi  2019
    ...  &{old_details}
    ${old_row}=  Set Variable  css=tbody tr:has(td:text-is("${cite_key}"))
    Click  ${old_row} >> text="Muokkaa"
    Get Property  id=cite_key  value  ==  ${cite_key}
    Get Property  id=author  value  ==  Eeva Esimerkki
    Get Property  id=title  value  ==  Alkuperäinen nimi
    Get Property  id=year  value  ==  2019
    FOR  ${field}  ${value}  IN  &{old_details}
        Get Property  id=${field}  value  ==  ${value}
    END

    ${new_cite_key}=  Set Variable  ${cite_key}-paivitetty
    Fill Reference Fields  ${new_cite_key}  Aino Mallikas  Päivitetty nimi  2024
    ...  &{new_details}
    Click  text="Tallenna muutokset"
    Get Text  role=status  ==  Viitteen tiedot päivitettiin onnistuneesti.

    Reload
    Reference Row Should Show  ${new_cite_key}  ${type_label}  Aino Mallikas
    ...  Päivitetty nimi  2024  ${expected_details}
    Get Element Count  ${old_row}  ==  0
