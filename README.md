# Python API for Piwik
This is a Python wrapper around the HTTP API for Piwik. While only a few methods are currently implemented the basic structure is there and should be easy to extend.

# Contributing
If you want to add a missing API please add a corresponding test in `test_api.py`.

## Tests
To run the tests set the environment variables then run `py.test`.

```sh
export PYWIK_API_URL=https://company.piwik.pro PYWIK_TOKEN_AUTH=$api_key
py.test
```
