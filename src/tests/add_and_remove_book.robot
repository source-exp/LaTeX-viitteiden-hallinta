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
    Click  text="Lisää kirja"
    Fill Text  id=cite_key   avain
    Fill Text  id=author     human being
    Fill Text  id=title      fake test book
    Fill Text  id=year       1000
    Fill Text  id=publisher  very real publisher
    Click  button[type="submit"]

    # The fake book should exist now.
    Get Text  body  contains  fake test book

Remove a book
    Homepage

    # The fake book should exist after the previous test.
    Get Text  body  contains  fake test book

    # Remove the fake book
    Handle Future Dialogs  action=accept
    Click  text=Poista

    # The fake book should not exist anymore.
    Get Text  body  not contains  fake test book
