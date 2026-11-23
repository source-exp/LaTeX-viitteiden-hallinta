*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Add a book
    Homepage

    # The fake book should not exist yet.
    Get Text  body  not contains  fake test book

    # Add the fake book.
    Add Reference  book  avain  human being  fake test book  1000
    ...  publisher=very real publisher

    Reload
    Reference Row Should Show  avain  Kirja  human being  fake test book  1000
    ...  very real publisher

Remove a book
    Homepage

    # The fake book should exist after the previous test.
    Get Text  body  contains  fake test book

    # Remove the fake book
    Handle Future Dialogs  action=accept
    Click  css=tbody tr:has(td:text-is("avain")) >> text="Poista"

    # The fake book should not exist anymore.
    Get Text  body  not contains  fake test book
