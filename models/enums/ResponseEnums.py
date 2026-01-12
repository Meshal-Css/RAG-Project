from enum import Enum

class ResponseSignal(Enum):

 FILE_VALIDATED_SUCCESS = "file_validate_successfully"
 FILE_TYPE_NOT_SUPPORTED = "File_type_not_supported"
 FILE_SIZE_EXCEEDED = "File_size_exceeded"
 FILE_UPLOAD_SUCCESS = "FILE_UPLOAD_SUCCESS"
 FILE_UPLOAD_FAILED = "FILE_UPLOAD_FAILED"