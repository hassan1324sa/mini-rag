from enum import Enum

class ResponseSignal(Enum):
    fileTypeNotSupportedOrFileSizeExceeded="file type is not supported or file size exceeded the file must be smaller than 11MB and the extension must be 'text' or 'pdf' "
    FileUploadedSuccess = "file upload success"
    FileUploadedFailed= "file upload failed"
    processingFailed ="processing failed"
    processingSuccess ="processing success"
    noFilesError = "files not found"
    fileIdError = "no file found with this id"
    projectNotFound = "the project not found"
    insertIntoVectorDBError = "insert Into VectorDB Error"
    insertIntoVectorDBSuccess = "insert Into VectorDB success"
    vectorCollectionRetrieved = "vector Collection Retrieved"
    vectorDBSearchSuccess="vectorDBSearch Success"
    vectorDBSearchError="vectorDBSearch Error"
    errorWhileAnswering="error While Answering"
    successAnswering="success Answering"