from pydantic import BaseModel

class JsonModel(BaseModel):
    class config:
        arbitrary_types_allowed = True
        extra = "allow"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_profile_store()
    
    def init_profile_store(self):
        raise NotImplementedError("Subclasses must implement this method")