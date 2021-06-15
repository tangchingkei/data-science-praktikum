# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 17:03:40 2021

@author: JonathanW
"""

import seaborn as sns

#filter spain from df
only_pain = g20_data[g20_data["location"]=="Spain"]

#make sure date is in datetime format
only_pain["date"] = pd.to_datetime(only_pain["date"], yearfirst=True)

#group by week -> each group gets mean cases of it's days assigned
grouped_pain = only_pain.groupby([pd.Grouper(key="date", freq= "W")]).mean()

#turn negative values positive
grouped_pain["new_cases"] = grouped_pain["new_cases"].apply(lambda x: abs(x))
#plot
f = sns.relplot(data = grouped_pain, x = "date", y= "new_cases", kind="line")
f.fig.autofmt_xdate()
f.set_ylabels("mean_new_cases")
