Feature: Gaskata Basic features

Scenario: *** Ping Gaskata ***
    Given address "@gaskata_base_url"
    Given URL path "/ping"
    Given HTTP method "GET"
    Given request format "RAW"
    Given response format "RAW"

    When the URL is invoked

    Then status is "200"
    And The text "ACK" is in the response data.
    And The text "login_check" isn't in the response data.

