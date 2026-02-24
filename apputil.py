import plotly.express as px
import pandas as pd
#e1
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
df["AgeBracket"] = pd.cut(
    df["Age"],
    bins=[0, 12, 19, 59, 120],
    labels=["Child", "Teen", "Adult", "Senior"]
)
g = (
    df.groupby(["Pclass", "Sex", "AgeBracket"], dropna=False, observed=False)
    .agg(
        n_passengers=("Survived", "size"),
        n_survivors=("Survived", "sum")
    )
    .assign(survival_rate=lambda x: x["n_survivors"] / x["n_passengers"])
    .reset_index()
)

g
st.write("Was the term 'save the children' accurate for the Titanic? Or just for the higher classes?")
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
viz = visualize_demographic(g)
viz.show()

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

st.write("These findings from the last name counts seem odd to me because if there are 25 passengers with a family size of 7+ then how come only 2 last names have 7+ unique people?")

st.write("How much was first class really on average and how does that compare to the other tickets?")
