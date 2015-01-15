
Feature: Gaskata Authenticate user

Scenario: *** REST JSON Auth User with missing password. ***

    Given Autheticate user with user ident "@auth_user_ident" and no password nor token
    Given address "@gaskata_base_url"
    Given Basic Auth "@gaskata_user" "@gaskata_password"
    Given HTTP method "POST"
    Given request format "RAW"
    Given response format "RAW"

    When the URL is invoked

    Then status is "404"
    And header "Server" isn't empty

Scenario: *** REST JSON Auth User with missing idents. ***

    Given Autheticate user without user but with password "@auth_user_password"
    Given address "@gaskata_base_url"
    Given Basic Auth "@gaskata_user" "@gaskata_password"
    Given HTTP method "POST"
    Given request format "RAW"
    Given response format "RAW"

    When the URL is invoked

    Then status is "404"
    And header "Server" isn't empty

Scenario: *** REST JSON Auth User with password. ***

    Given Autheticate user with user ident "@auth_user_ident" and password "@auth_user_password"
    Given address "@gaskata_base_url"
    Given Basic Auth "@gaskata_user" "@gaskata_password"
    Given HTTP method "POST"
    Given request format "RAW"
    Given response format "JSON"

    When the URL is invoked

    Then status is "200"
    And header "Server" isn't empty
    And JSON Pointer "/auth_token" isn't empty

Scenario: *** REST JSON Auth User with email and password. ***

    Given Autheticate user with email "@auth_user_email" and password "@auth_user_password"
    Given address "@gaskata_base_url"
    Given Basic Auth "@gaskata_user" "@gaskata_password"
    Given HTTP method "POST"
    Given request format "RAW"
    Given response format "JSON"

    When the URL is invoked

    Then status is "200"
    And header "Server" isn't empty
    And JSON Pointer "/auth_token" isn't empty

