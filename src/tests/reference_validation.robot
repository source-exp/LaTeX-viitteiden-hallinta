*** Settings ***
Resource  resource.robot
Library  Collections
Library  DateTime
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Add Form Shows Character Limits
    Homepage
    Click  text="Lisää viite"

    Get Attribute  id=author  maxlength  ==  200
    Get Attribute  id=title  maxlength  ==  300
    ${current_year}=  Get Current Date  result_format=%Y
    Get Attribute  id=year  max  ==  ${current_year}

    Select Options By  id=reference_type  value  article
    Get Attribute  id=title  maxlength  ==  300

    Select Options By  id=reference_type  value  conference_article
    Get Attribute  id=title  maxlength  ==  300
    Get Attribute  id=booktitle  maxlength  ==  300

Reject Over-limit Book Title
    [Template]  Reject Over-limit Reference Field
    book  title  301  Nimi saa olla enintään 300 merkkiä.

Reject Over-limit Article Title
    [Template]  Reject Over-limit Reference Field
    article  title  301  Nimi saa olla enintään 300 merkkiä.

Reject Over-limit Conference Article Title
    [Template]  Reject Over-limit Reference Field
    conference_article  title  301  Nimi saa olla enintään 300 merkkiä.

Reject Over-limit Author Name
    [Template]  Reject Over-limit Reference Field
    book  author  201  Tekijä saa olla enintään 200 merkkiä.

Reject Over-limit Citation Key
    [Template]  Reject Over-limit Reference Field
    book  cite_key  101  Viiteavain saa olla enintään 100 merkkiä.

Reject Over-limit Publisher
    [Template]  Reject Over-limit Reference Field
    book  publisher  501  Kustantaja saa olla enintään 500 merkkiä.

Reject Over-limit Journal
    [Template]  Reject Over-limit Reference Field
    article  journal  501  Julkaisu saa olla enintään 500 merkkiä.

Reject Over-limit Volume
    [Template]  Reject Over-limit Reference Field
    article  volume  101  Volyymi saa olla enintään 100 merkkiä.

Reject Over-limit Issue Number
    [Template]  Reject Over-limit Reference Field
    article  number  101  Numero saa olla enintään 100 merkkiä.

Reject Over-limit Pages
    [Template]  Reject Over-limit Reference Field
    article  pages  101  Sivut saa olla enintään 100 merkkiä.

Reject Over-limit Conference Book Title
    [Template]  Reject Over-limit Reference Field
    conference_article  booktitle  301  Kirja tai konferenssinimi saa olla enintään 300 merkkiä.

Reject Future Publication Year For Books
    [Template]  Reject Future Publication Year
    book

Reject Future Publication Year For Articles
    [Template]  Reject Future Publication Year
    article

Reject Future Publication Year For Conference Articles
    [Template]  Reject Future Publication Year
    conference_article

*** Keywords ***
Reject Over-limit Reference Field
    [Arguments]  ${reference_type}  ${field}  ${length}  ${expected_error}
    Homepage
    ${current_year}=  Get Current Date  result_format=%Y
    ${data}=  Create Dictionary
    ...  reference_type=${reference_type}
    ...  cite_key=robot-limit-test
    ...  author=Test author
    ...  title=Test title
    ...  year=${current_year}
    IF  $reference_type == 'book'
        Set To Dictionary  ${data}  publisher  Test publisher
    ELSE IF  $reference_type == 'article'
        Set To Dictionary  ${data}  journal  Test journal
    ELSE
        Set To Dictionary  ${data}  booktitle  Test proceedings
    END
    ${over_limit_value}=  Evaluate  'x' * int(${length})
    Set To Dictionary  ${data}  ${field}  ${over_limit_value}
    ${response}=  Submit Reference Form  ${data}
    Should Be Equal As Integers  ${response}[status]  400
    Should Contain  ${response}[body]  ${expected_error}

Reject Future Publication Year
    [Arguments]  ${reference_type}
    Homepage
    ${current_year}=  Get Current Date  result_format=%Y
    ${future_year}=  Evaluate  int(${current_year}) + 1
    ${data}=  Create Dictionary
    ...  reference_type=${reference_type}
    ...  cite_key=robot-future-year-test
    ...  author=Test author
    ...  title=Test title
    ...  year=${future_year}
    IF  $reference_type == 'book'
        Set To Dictionary  ${data}  publisher  Test publisher
    ELSE IF  $reference_type == 'article'
        Set To Dictionary  ${data}  journal  Test journal
    ELSE
        Set To Dictionary  ${data}  booktitle  Test proceedings
    END
    ${response}=  Submit Reference Form  ${data}
    Should Be Equal As Integers  ${response}[status]  400
    Should Contain  ${response}[body]  Julkaisuvuosi ei voi olla vuotta ${current_year} myöhempi.

Submit Reference Form
    [Arguments]  ${form_data}
    ${response}=  Evaluate JavaScript  ${None}
    ...  async (formData) => {
    ...      const response = await fetch("/books", {
    ...          method: "POST",
    ...          headers: {"Content-Type": "application/x-www-form-urlencoded"},
    ...          body: new URLSearchParams(formData),
    ...      });
    ...      return {status: response.status, body: await response.text()};
    ...  }
    ...  arg=${form_data}
    RETURN  ${response}
