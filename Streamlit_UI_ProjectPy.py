import streamlit as st
import pandas as pd
import plotly.express as px
from Loading_ProjectPy import import_json
from ProjetPy import ControlFin

import plotly.express as px
import pandas as pd
import streamlit as st

def _render_comparaison_tab(expenses_archive):
    # --- Run selection table ---
    # --- Plot chart ---
    data = []
    for p, i in enumerate(expenses_archive):
        V0 = ControlFin(i) 
        dicCat = V0.add_expenses()  
        year = 2026 - p
        for cat_name, cat_obj in dicCat.items():
            data.append({
                "Archive": str(year),
                "Categorie": cat_name,
                "Valeur": cat_obj.get_amount()
            })

    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Archive",
        y="Valeur",
        color="Categorie",
        barmode="stack",  # 'stack' pour empiler (par défaut), ou 'group' pour côte à côte
        title="Expenses by Category across years"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def _render_visualisation_tab(expenses_archive):
    # --- Plot camenbert chart ---
    V0 = ControlFin(expenses_archive[0]) 
    diCat = V0.add_expenses()  
    amounts = [cat.get_amount() for cat in diCat.values()]  #l'année en question on recupere l'objet categorie et on veut
    data = {"Categorie": list(diCat.keys()), "Valeur": amounts}
    df = pd.DataFrame(data)

    fig = px.pie(df, values="Valeur", names="Categorie", title="Expenses during this last year")
    st.plotly_chart(fig, width='stretch')


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
def main():
    st.title("Expenses report")

    # --- Top-level tabs ---
    tab_visualisation, tab_comparaison, tab_expenses_details, tab_user = st.tabs(["Expenses categories visualisation", "Comparaison with archive",  "Expenses list", "User"])
    # tab_expenses_details, tab_user have not been implemented maybe in the futur

    path = 'Data_expenses.JSON'
    expenses_archive = import_json(path)

    with tab_visualisation:
        _render_visualisation_tab(expenses_archive)

    with tab_comparaison:
        _render_comparaison_tab(expenses_archive)
    
if __name__ == "__main__":
    main()