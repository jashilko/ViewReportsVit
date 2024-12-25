from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class CDR(Base):
    calldate = Column(DateTime, primary_key=True)
    src = Column(String)
    dst = Column(String)
    duration = Column(Integer)
    billsec = Column(Integer)
    disposition = Column(String)
    recordingfile = Column(String)


    def to_dict(self):
        return {
            "calldate": self.calldate.strftime("%d.%m.%Y %H:%M:%S"),
            "src": self.src,
            "dst": self.dst,
            "duration": self.duration,
            "billsec": self.billsec,
            "disposition": self.disposition,
            "recordingfile": self.recordingfile,
        }