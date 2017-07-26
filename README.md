# rqtest
test tool based on requests

## Usage
```
import rqtest
with rqtest.get('url_for_testing', data={'t': 1}, headers={'token': ...}) as obj:
    assert obj['code'] == 0
```
