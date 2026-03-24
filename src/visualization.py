import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.express as px

def visualize_Structure(input):
    print(input.head())

def visualize_Normal(input):
    df = pd.DataFrame(input)

    plotBar1(df)
    plotBarStacked(df)
    plotBox(df) 
    plotPie(df)

def plotBar1(df):
    #2
    #Bar Plot
    SELECTED_REALMS = ["Alpha", "Cerberus","Lich","Louisoix","Moogle","Odin","Omega"]  # <-- european realms
 
    df = df[df["Dim_Realms"].isin(SELECTED_REALMS)]
    pivot = df.pivot_table(
    index="Dim_Realms",
    columns="Dim_isEndgame",
    values="V_PlayerCount",
    aggfunc="sum",
    )

    ax = pivot.plot.bar(figsize=(24, 10))
    ax.set_xlabel("Realm", fontsize=12)
    ax.set_ylabel("Player Count", fontsize=12)
    ax.set_title("Player Count by Realm and Endgame status", fontsize=14)
    ax.legend(title="Endgame status", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=45)
    ax.set_yscale("log")
    plt.suptitle("")
    plt.tight_layout()

    plt.savefig("./docs/media/visualizations/ffxiv_Bar_PlayerEndgameRealm.png", dpi=150)

def plotBox(df):
    #2
    #Box Plot

    SELECTED_REALMS = ["Alpha", "Cerberus","Lich","Louisoix","Moogle","Odin","Omega"]  # <-- european realms
 
    df = df[df["Dim_Realms"].isin(SELECTED_REALMS)]
    realms = df["Dim_Realms"].unique()
    COLS_PER_ROW = 22
    n_cols = min(COLS_PER_ROW, len(realms))
    n_rows = math.ceil(len(realms) / n_cols)
 
    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(5 * n_cols, 5 * n_rows),
        sharey=True,
    )
 
    axes_flat = np.array(axes).flatten()
 
    for i, realm in enumerate(realms):
        ax = axes_flat[i]
        subset = df[df["Dim_Realms"] == realm]
        subset.boxplot(
        column="V_PlayerCount",
        by="Dim_isEndgame",
        ax=ax,
        grid=False,
        )
        ax.set_title(realm, fontsize=11)
        ax.set_xlabel("isEndgame", fontsize=10)
        ax.set_ylabel("Player Count (log scale)" if i % n_cols == 0 else "", fontsize=10)
        ax.set_yscale("log")
        ax.tick_params(axis="x", rotation=0)
 
    for j in range(len(realms), len(axes_flat)):
        axes_flat[j].set_visible(False)
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig("./docs/media/visualizations/ffxiv_Box_PlayerEndgameRealm.png", dpi=150)

def plotBarStacked(df):
    #1
    #Box plot stacked
    SELECTED_REALMS = ["Lich"] 
 
    df_filtered = df[df["Dim_Realms"].isin(SELECTED_REALMS)]
 
    # --- Grid layout ---
    COLS_PER_ROW = 3
    n_cols = min(COLS_PER_ROW, len(SELECTED_REALMS))
    n_rows = math.ceil(len(SELECTED_REALMS) / n_cols)
 
    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(6 * n_cols, 5 * n_rows),
        sharey=True,
    )   
    axes_flat = np.array(axes).flatten()
    
    for i, realm in enumerate(SELECTED_REALMS):
        ax = axes_flat[i]
        subset = df_filtered[df_filtered["Dim_Realms"] == realm]
 
        # Pivot: rows = GrandCompany, columns = isEndgame
        pivot = subset.pivot_table(
        index="Dim_GrandCompany",
        columns="Dim_isEndgame",
        values="V_PlayerCount",
        aggfunc="sum",
        )
        pivot.columns = [f"Endgame: {c}" for c in pivot.columns]
 
        pivot.plot.bar(stacked=True,ax=ax, legend=(i == 0))
 
        ax.set_title(realm, fontsize=11)
        ax.set_xlabel("Grand Company", fontsize=10)
        ax.set_ylabel("Player Count" if i % n_cols == 0 else "", fontsize=10)
        ax.set_yscale("log")
        ax.tick_params(axis="x", rotation=30)
 
    if i == 0:
        ax.legend(title="isEndgame", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
 
    # Hide unused slots
    for j in range(len(SELECTED_REALMS), len(axes_flat)):
        axes_flat[j].set_visible(False)
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig("./docs/media/visualizations/ffxiv_Bar_PlayerEndgameCompany.png", dpi=150)
    
def plotPie(df):
    summary = df.groupby("Dim_isEndgame")["V_PlayerCount"].sum()
    summary.index = ["Non-Endgame" if not x else "Endgame" for x in summary.index]
 
    # --- Plot ---
    fig, ax = plt.subplots(figsize=(6, 6))
 
    summary.plot.pie(
    ax=ax,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#4C72B0", "#DD8452"],
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        )
 
    ax.set_ylabel("")
    ax.set_title("Player Split: Endgame vs Non-Endgame", fontsize=13)
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig("./docs/media/visualizations/ffxiv_Pie_PlayerEndgame.png", dpi=150)

def visualize_Ridiculous(input):
    df = pd.DataFrame(input)
    plot_pie_ridi(df)
    plot_bar_ridi(df)

    
def plot_pie_ridi(df):
    summary = df.groupby("V_Category")["V_Interactions"].sum()
 
    # --- Plot ---
    fig, ax = plt.subplots(figsize=(6, 6))
 
    summary.plot.pie(
    ax=ax,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#4C72B0", "#DD8452","#00FF6B","#5100FF","#D400FF","#C3FF00","#FF0000"],
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        )
 
    ax.set_ylabel("")
    ax.set_title("Player Split: Favorite Category", fontsize=13)
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig("./docs/media/visualizations/ffxiv_Pie_PlyerFavCategorie.png", dpi=150)

def plot_bar_ridi(df):
    #Bar Plot
    pivot = df.pivot_table(
    index="V_Category",
    values="V_Interactions",
    aggfunc="sum",
    )

    ax = pivot.plot.bar(figsize=(24, 10))
    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Player Count", fontsize=12)
    ax.set_title("Favorite Category ", fontsize=14)
    ax.tick_params(axis="x", rotation=45)
    ax.set_yscale("log")
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig("./docs/media/visualizations/ffxiv_Bar_PlayerFavCat.png", dpi=150)
    

def visualize_Geo(input):
    df = pd.DataFrame(input)
    df['label'] = df['V_Region'] + '<br>' + df['V_PlayerCount'].astype(str)
    fig = px.scatter_geo(
        df,
        lat='lat', lon='lon',
        size='V_PlayerCount',
        text='label',
        title='Player Count by Region',
        projection='natural earth'
    )

    fig.update_traces(
        textposition='top center',
        textfont=dict(size=25, color='black')
    )

    fig.show()



    