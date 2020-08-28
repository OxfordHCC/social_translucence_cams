from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    ForeignKeyField,
    BooleanField
)
from arlo_st.env import DATABASE

# create a peewee database instance -- our models will use this database to
# persist information
database = SqliteDatabase(DATABASE)

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database

class Issue(BaseModel):
    #id = CharField(primary_key=True, column_name="IssueID")
    message = CharField(column_name="IssueMessage")
    resolved = BooleanField(default=False, column_name="IssueResolved")

class Message(BaseModel):
    #id = CharField(primary_key=True, column_name="MessageID")
    content = CharField(column_name="MessageContent")
    
class IssueMessage(BaseModel):
    issue = ForeignKeyField(Issue, backref='+', column_name="_FK_IssueID")
    message = ForeignKeyField(Message, backref='+', column_name="FK_MessageID")
    class Meta:
        indexes = (
            (('issue', 'message'), True),
        )

#capture adapters
#Examples: arlo, motionsense
class CaptureAdapter(BaseModel):
    name = CharField(default="Unnamed Adapter", column_name="CaptureAdapterName")
    adapter_type = CharField(column_name="CaptureAdapterType")
    options = CharField(null=True, column_name="CaptureAdapterOptions")

#each library entry corresponds to a remote entry from adapter_id
#remote_id is the adapter-specific identifier
#name is usually the remote name unless no such thing, in which case the name is up to the adapter
# to choose

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
    removed_remote = BooleanField(default=False, column_name="RemovedRemote")
    location_remote = CharField(null = True, column_name="LocationRemote")
    location_local = CharField(null = True, column_name="LocationLocal")
    def __hash__(self):
        return hash(self.id)
    
#TODO: move to ops scripts
def create_tables():
    with database:
        database.create_tables([
            Issue,
            Message,
            IssueMessage,
            Library,
            Camera,
            CaptureAdapter
        ])
