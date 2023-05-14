import datetime
from time import sleep

import pandas as pd

while True:
    df = pd.DataFrame(
        data={"col1": [datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=7)], "col2": [1, 2]}
    )
    print(df)
    sleep(2)
