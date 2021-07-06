from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import OrderedDict
from datetime import timedelta


g20_vacc = vaccination[vaccination["Entity"].isin(g20_members)].reset_index(drop=True)

phases = []

for country in g20_members:

    #this does not work if the European Union is included in g20_members, since it doesn't have data on vaccines -> makes array out of bounds
    
    #changed the phases df to be of the format [ "country", "start date of policy", "end date of policy", "level of policy" ]

    df = g20_vacc[g20_vacc["Entity"] == country].reset_index(drop=True)
    
    #level and start are now initialized to contain the first date in the data and the policy level on the first date
    level = df.iloc[0]["vaccination_policy"]
    start = df.iloc[0]["Day"]
    for index, row in df.iterrows():
        if row["vaccination_policy"] != level:
            phases.append([country, start, row["Day"], level])
            level = row["vaccination_policy"]
            start = row["Day"]

    #append the time between last change and the end of data. without this the most recent level change might be lost
    phases.append([country, start, df.iloc[-1]["Day"], df.iloc[-1]["vaccination_policy"]])

#used the name "date" instead of "start" so the merge in "final_vacc" doesn't get fucked up
vaccination_phases = DataFrame(phases, columns=["country","date", "end", "level"]).dropna(how="all").reset_index(drop=True)
vaccination_phases["date"] = pd.to_datetime(vaccination_phases["date"], yearfirst=True)
vaccination_phases["end"] = pd.to_datetime(vaccination_phases["end"], yearfirst=True)


for loc in g20_members:
    loc_data = g20_data[g20_data["location"]==loc]
    phases = vaccination_phases[vaccination_phases["country"] == loc]

    #datetime
    loc_data["date"] = pd.to_datetime(loc_data["date"], yearfirst=True)
    loc_data["month"] = loc_data.date.dt.month_name()
    loc_data["year"] = loc_data.date.dt.year
    loc_data["day"] = loc_data.date.dt.day

    #negative to nan
    loc_data["new_cases"] = loc_data["new_cases"].map(lambda x: float("nan") if (x<0 or x==0) else x, na_action="ignore")

    final_vacc = phases.merge(loc_data, on="date")
    final_vacc = final_vacc.drop(["location"],axis=1)


    fig, ax = plt.subplots(figsize=(20,7))
    ax.scatter("date", "new_cases", data = loc_data, color="silver")
    fmt_every_month = mdates.MonthLocator(interval=3)
    ax.xaxis.set_major_locator(fmt_every_month)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.autofmt_xdate()
    plt.title(loc)


    vacc_colors = ["peachpuff", "salmon", "tomato", "orangered", "firebrick"]

    #needed to adjust columns since there is now one more column in final_vacc
    for ind, data in final_vacc.iterrows():
        plt.hlines(data[4], xmin=data[1], xmax =data[2], colors = vacc_colors[int(data[3])-1],
                   label = f"Level {int(data[3])}", linestyles="dashdot", linewidth=3)

    

    #plot everything
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(),loc="upper left")
    plt.show()