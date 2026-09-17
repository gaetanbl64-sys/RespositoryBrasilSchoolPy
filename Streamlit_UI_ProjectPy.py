import json
import pandas as pd
import plotly.express as px
import streamlit as st
from Loading_ProjectPy import import_json
from ProjetPy import ControlFin


# _______________________________________________________________________
def _render_comparaison_tab(expenses_archive):
    # 1. Extraction de toutes les données par année
    all_data = []
    years = []
    for p, archive in enumerate(expenses_archive):
        year = str(2026 - p)
        years.append(year)

        V0 = ControlFin(archive)
        dicCat = V0.add_expenses()

        for cat_name, cat_obj in dicCat.items():
            all_data.append(
                {
                    "Archive": year,
                    "Categorie": cat_name,
                    "Valeur": cat_obj.get_amount(),
                }
            )

    # 2. Tableau de sélection basé uniquement sur les années uniques
    st.subheader(f"Sélection des années ({len(years)})")
    df_years = pd.DataFrame([{
        "Select": True, 
        "Archive": y
        } for y in years])

    edited_df = st.data_editor(
        df_years,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=True)
        },
        hide_index=True,
        use_container_width=True,
    )

    # 3. Récupération des années cochées
    selected_years = edited_df[edited_df["Select"]]["Archive"].tolist()

    # 4. Filtrage du DataFrame global avec les années sélectionnées
    df_all = pd.DataFrame(all_data)
    df_chart = df_all[df_all["Archive"].isin(selected_years)]

    # 5. Affichage du graphique
    fig = px.bar(
        df_chart,
        x="Archive",
        y="Valeur",
        color="Categorie",
        barmode="stack",
        title="Expenses by Category across years",
    )
    st.plotly_chart(fig, use_container_width=True)


# _______________________________________________________________________
def _render_visualisation_tab(expenses_archive):
    # --- Plot camembert chart ---
    V0 = ControlFin(expenses_archive[0])
    diCat = V0.add_expenses()
    amounts = [cat.get_amount() for cat in diCat.values()]
    data = {"Categorie": list(diCat.keys()), "Valeur": amounts}
    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        values="Valeur",
        names="Categorie",
        title="Expenses during this last year",
    )
    st.plotly_chart(fig, use_container_width=True)


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