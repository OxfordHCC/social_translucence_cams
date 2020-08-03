import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["P_ROOT"]= MAIN_DIR

from arlo_st.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()
    
