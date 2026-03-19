import streamlit as st


def init_session():
    """Initialise all global session-state keys once."""
    defaults = {
        "df":             None,   # active DataFrame
        "df_name":        None,   # filename
        "dataset_count":  0,
        "rows_processed": 0,
        "chart_count":    0,
        "report_count":   0,
        "theme_accent":   "#00e5ff",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def set_df(df, name: str):
    st.session_state.df             = df
    st.session_state.df_name        = name
    st.session_state.dataset_count  = st.session_state.dataset_count + 1
    st.session_state.rows_processed = len(df)


def get_df():
    return st.session_state.get("df", None)
