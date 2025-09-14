from enum import Enum

class ResponseSignal(Enum):
    fileTypeNotSupportedOrFileSizeExceeded="file type is not supported or file size exceeded the file must be smaller than 11MB and the extension must be 'text' or 'pdf' "
    FileUploadedSuccess = "file upload success"
    FileUploadedFailed= "file upload failed"
    processingFailed ="processing failed"
    processingSuccess ="processing success"
    noFilesError = "files not found"
    fileIdError = "no file found with this id"
