import plotly.express as px
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"
)

def survival_demographics():
    df_local = df.copy()

    df_local["AgeBracket"] = pd.cut(
        df_local["Age"],
        bins=[0, 12, 19, 59, 120],
        labels=["Child", "Teen", "Adult", "Senior"]
    )

    g = (
        df_local.groupby(
            ["Pclass", "Sex", "AgeBracket"],
            dropna=False,
            observed=False
        )
        .agg(
            n_passengers=("Survived", "size"),
            n_survivors=("Survived", "sum")
        )
        .assign(survival_rate=lambda x: x["n_survivors"] / x["n_passengers"])
        .reset_index()
        .sort_values(by=["Pclass", "Sex", "AgeBracket"])
        .reset_index(drop=True)
    )

    return g


g = survival_demographics()
print(g.head(30))

def visualize_demographic(g):
    groups = g[g["AgeBracket"].isin(["Child", "Adult"])].copy()

    v = px.bar(
        groups,
        x="AgeBracket",
        y="survival_rate",
        color="Sex",
        barmode="group",
        facet_col="Pclass",
        category_orders={
            "AgeBracket": ["Child", "Adult"],
            "Pclass": sorted(groups["Pclass"].unique())
        }
    )
    return v


fig1 = visualize_demographic(g)
fig1.show()

#e2

def family_group(df, sibsp, parch, family_size):
    df[family_size] = df[sibsp] + df[parch] + 1

    df2 = (
        df.groupby([family_size, "Pclass"])
        .agg(
            n_passengers=("PassengerId", "size"),
            avg_fare=("Fare", "mean"),
            min_fare=("Fare", "min"),
            max_fare=("Fare", "max"),
        )
    )
    return df2

df2 = family_group(df, "SibSp", "Parch", "family_size")
df2.head(30)

def last_names(df):
    last_name = df["Name"].str.split(",").str[0]
    return  last_name.value_counts()

last_name_counts = last_names(df)
last_name_counts.head(30)

avg_fare = (
    df.groupby("Pclass")
    .agg(avg_fare=("Fare", "mean"))
    .reset_index()
)
def visualize_families(avg_fare):
    vi = px.bar(
        avg_fare,
        x="Pclass",
        y="avg_fare",
    )
    vi.update_layout(
    title="Average Fare by Passenger Class",
    xaxis_title="Passenger Class",
    yaxis_title="Average Fare"
)
    return vi
fig2 = visualize_families(avg_fare)
fig2.show()

