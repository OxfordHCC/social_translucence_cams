import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["P_ROOT"] = MAIN_DIR

#this import needs to be after the environement modification above

from arlo_st.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()
