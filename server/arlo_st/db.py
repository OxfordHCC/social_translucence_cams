from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    ForeignKeyField,
    BooleanField,
    DateTimeField
)
from arlo_st.env import DATABASE
from datetime import datetime

database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

# TODO: decide on whether to explicitly specify id field on models or
# not beacause currently they're mixed.

class User(BaseModel):
    username = CharField(unique=True, column_name="UserUsername")
    password = CharField(column_name="UserPassword")
    
class TransLog(BaseModel):
    user = ForeignKeyField(User, backref="+", column_name="FK_User") # translucer
    event_type = CharField(column_name="TransLogTranslucedType")
    timestamp = DateTimeField(default=datetime.now, column_name="TransLogTimestamp")

class Issue(BaseModel):
    id = CharField(primary_key=True, column_name="IssueID")
    message = CharField(column_name="IssueMessage")
    resolved = BooleanField(default=False, column_name="IssueResolved")

class Message(BaseModel):
    id = CharField(primary_key=True, column_name="MessageID")
    content = CharField(column_name="MessageContent")
    
class IssueMessage(BaseModel):
    issue = ForeignKeyField(Issue, backref='+', column_name="_FK_IssueID")
    message = ForeignKeyField(Message, backref='+', column_name="FK_MessageID")
    class Meta:
        indexes = (
            (('issue', 'message'), True),
        )

class CaptureAdapter(BaseModel):
    name = CharField(default="Unnamed Adapter", column_name="CaptureAdapterName")
    adapter_type = CharField(column_name="CaptureAdapterType")
    options = CharField(null=True, column_name="CaptureAdapterOptions")

class Camera(BaseModel):
    id = CharField(primary_key=True, column_name="CameraID")
    name = CharField(column_name="CameraName", default="Unnamed Camera")
    adapter = ForeignKeyField(CaptureAdapter, backref='+', column_name="FK_AdapterID")
    def __hash__(self):
        return hash(self.id)

class Library(BaseModel):
    id = CharField(primary_key=True, column_name="LibraryID")
    adapter = ForeignKeyField(CaptureAdapter, backref='+', column_name="FK_AdapterID")
    camera = ForeignKeyField(Camera, backref='+', column_name = "FK_CameraID")
    name = CharField(column_name="LibraryName")
    timestamp = CharField(column_name="LibraryTimestamp")
    removed_remote = BooleanField(default=False, column_name="RemovedRemote")
    location_remote = CharField(null = True, column_name="LocationRemote")
    location_local = CharField(null = True, column_name="LocationLocal")
    def __hash__(self):
        return hash(self.id)


    
#TODO: move to ops scripts
def create_tables():
    with database:
        database.create_tables([
            User,
            Issue,
            Message,
            IssueMessage,
            Library,
            Camera,
            CaptureAdapter,
            TransLog
        ])
