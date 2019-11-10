class LineStatus:

    def __init__(self, affected_lines=[], duration_ms=None, file_handle=None, file_path=None, phrase=None, raw_status=None,
                 status_code=None):
        self.affected_lines = affected_lines
        self.duration_ms = duration_ms
        self.file_handle = file_handle
        self.file_path = file_path
        self.phrase = phrase
        self.raw_status = raw_status
        self.status_code = status_code

    def __repr__(self):
        return '<LineStatus affected_lines=%r, status_code=%r, file_path=%r, phrase=%r>' % (
            self.affected_lines, self.status_code, self.file_path, self.phrase
        )

    def __eq__(self, other):
        return (self.affected_lines == other.affected_lines and
                self.duration_ms == other.duration_ms and
                self.file_handle == other.file_handle and
                self.file_path == other.file_path and
                self.phrase == other.phrase and
                self.raw_status == other.raw_status and
                self.status_code == other.status_code)
