from arlo_st.db import Issue

def get():
    return list(Issue.select().dicts())
