import pandas as pd
import matplotlib.pyplot as plt

def visualize_Structure(input):
    print(input.head())

def visualize_Normal(input):
    df = pd.DataFrame(input,columns=[])
    pivot = df.pivot_table(
    index="Dim_Realms",
    columns="Dim_GrandCompany",
    values="Fact_PlayerCount",
    aggfunc="sum",
    )
    ax = pivot.plot.bar(figsize=(12, 6))
 
    ax.set_xlabel("Realm", fontsize=12)
    ax.set_ylabel("Player Count", fontsize=12)
    ax.set_title("Player Count by Realm and Grand Company", fontsize=14)
    ax.legend(title="Grand Company", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=45)
    
    plt.tight_layout()
    plt.show()
    