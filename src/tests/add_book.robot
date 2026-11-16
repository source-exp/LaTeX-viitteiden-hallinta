*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Add a book
    Homepage

    # The fake should not exist yet.
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
