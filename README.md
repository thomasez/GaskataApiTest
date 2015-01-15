# GaskataApiTest
The [zato-apitest][1] based test regime for [Gaskata][2].

There are three environment variables you can use to change the output from this.

 * BEHAVE_DEBUG_ON_ERROR prints as much debug info as possible when a test fails.
 * PRINT_VERBOSE_OUTPUT prints as much as possible anyway after each scenario.
 * PRINT_DOC_ON_PASSED prints a Trac-wiki formatted doc with request and response.

[1]: https://github.com/zatosource/zato-apitest
[2]: https://github.com/thomasez/Gaskata
