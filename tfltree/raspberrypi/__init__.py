class LineStatus:

    def __init__(self, affected_lines=set(), duration_ms=None, file_handle=None, file_path=None, phrase=None, reason=None,
                 status_codes=set()):
        self.affected_lines = affected_lines
        self.duration_ms = duration_ms
        self.file_handle = file_handle
        self.file_path = file_path
        self.phrase = phrase
        self.reason = reason
        self.status_codes = status_codes

    def __repr__(self):
        return '<LineStatus affected_lines=%r, status_codes=%r, file_path=%r, phrase=%r>' % (
            self.affected_lines, self.status_codes, self.file_path, self.phrase
        )

    def __eq__(self, other):
        return (self.affected_lines == other.affected_lines and
                self.duration_ms == other.duration_ms and
                self.file_handle == other.file_handle and
                self.file_path == other.file_path and
                self.phrase == other.phrase and
                self.reason == other.reason and
                self.status_codes == other.status_codes)
