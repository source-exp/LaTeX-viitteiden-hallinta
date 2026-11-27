*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Homepage
Test Teardown  Remove BibTeX Test References

*** Test Cases ***
BibTeX Export Includes Every Reference Type
    Add Reference  book  bibtex-export-book  Test Author  Book title  2024
    ...  publisher=Test Publisher
    Add Reference  article  bibtex-export-article  Test Author  Article title  2023
    ...  journal=Test Journal  volume=5  number=2  pages=10-20
    Add Reference  conference_article  bibtex-export-conference  Test Author
    ...  Conference title  2022  booktitle=Test Proceedings

    ${export}=  Evaluate JavaScript  ${None}
    ...  async () => {
    ...      const response = await fetch("/bibtex");
    ...      return {
    ...          disposition: response.headers.get("Content-Disposition"),
    ...          body: await response.text(),
    ...      };
    ...  }

    Should Contain  ${export}[disposition]  attachment
    Should Contain  ${export}[disposition]  viitteet.bib
    Should Contain  ${export}[body]  @book{bibtex-export-book
    Should Contain  ${export}[body]  publisher = "Test Publisher"
    Should Contain  ${export}[body]  @article{bibtex-export-article
    Should Contain  ${export}[body]  journal   = "Test Journal"
    Should Contain  ${export}[body]  volume    = "5"
    Should Contain  ${export}[body]  number    = "2"
    Should Contain  ${export}[body]  pages     = "10-20"
    Should Contain  ${export}[body]  @inproceedings{bibtex-export-conference
    Should Contain  ${export}[body]  booktitle = "Test Proceedings"

*** Keywords ***
Remove BibTeX Test References
    Homepage
    FOR  ${cite_key}  IN
    ...  bibtex-export-book
    ...  bibtex-export-article
    ...  bibtex-export-conference
        ${row}=  Set Variable  css=tbody tr:has(td:text-is("${cite_key}"))
        ${count}=  Get Element Count  ${row}
        IF  ${count} > 0
            Handle Future Dialogs  action=accept
            Click  ${row} >> text="Poista"
        END
    END
