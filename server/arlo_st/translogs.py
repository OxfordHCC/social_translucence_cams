from arlo_st.db import TransLog

def get():
    return list(TransLog.select().dicts())

def create(user_id, event_type):
    return TransLog.create(user=user_id, event_type=event_type)
