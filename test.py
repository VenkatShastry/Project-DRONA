import streamlit as st
import login as lgn  # Now import login only
import ats_tool
import plagiarism_tool
import about
from streamlit_option_menu import option_menu


# Ensure session state is properly initialized
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "show_login" not in st.session_state:
    st.session_state["show_login"] = True
if "show_register" not in st.session_state:
    st.session_state["show_register"] = False

# Main logic for deciding whether to show login, register, or main content
def show():
    if not st.session_state["logged_in"]:
        # Show login or register based on session state
        if st.session_state["show_login"]:
            lgn.show_login()  # No circular import now
        elif st.session_state["show_register"]:
            lgn.show_register_page()
    else:
        # If the user is logged in, show the main app content
        with st.sidebar:
            st.markdown(f"<span style='font-size: 20px; color: Gold;'>Welcome Back, {st.session_state['username']}</span>", unsafe_allow_html=True)
            
            # Button to log out
            if st.button("Sign Out"):
                st.session_state["logged_in"] = False
                st.session_state.pop("username", None)
                st.experimental_rerun()

            selected = option_menu(
                "Main Menu",
                ["ATS_Tool", "Plagiarism Tool", "About"],
                icons=["tools", "file-text", "info-circle"],
                menu_icon="cast",
                default_index=0,
            )

        if selected == "ATS_Tool":
            ats_tool.show()
        elif selected == "Plagiarism Tool":
            plagiarism_tool.show()
        elif selected == "About":
            about.show()

if __name__ == "__main__":
    show()
