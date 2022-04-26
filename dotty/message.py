class Message:
    def __init__(self, body: str, sent_by: str, sent_in: str):
        self.sent_by: str = sent_by
        self.sent_in: str = sent_in
        self.body: str = body

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.body == other.body and self.sent_by == other.sent_by and self.sent_in == other.sent_in
        return False
