from enum import Enum

class ResponseSignal(Enum):
    fileTypeNotSupportedOrFileSizeExceeded="file type is not supported or file size exceeded"
    FileUploadedSuccess = "file upload success"
    FileUploadedFailed= "file upload failed"
    PROCESSING_FAILED ="processing failed"
    PROCESSING_SUCCESS ="processing success"