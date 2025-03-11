PUG SOAP Web Service Reference
Methods
Name	Description
AssayDownload	Given an assay key, prepare for download a file containing an assay data table in the selected format. See the assay query section of the PUG service documentation for more detail on the supported formats. Compression is optional and defaults to gzip (.gz). Returns a download key. Asynchronous.
Download	Given a list key, prepare for download a file containing those records in the selected format. See the web download service documentation for more detail on the supported formats and file types. Returns a download key. Asynchronous. Note that if SynchronousSingleRecord is set to true, and the ListKey contains only a single ID, then a Base64 string of data is returned synchronously in the response, instead of going through the download file.
GetAssayColumnDescription	Get the description of column (readout) in a BioAssay, which may be the outcome, score, or a TID from the given AID. Synchronous.
GetAssayColumnDescriptions	Get the description of all columns (readouts) in a BioAssay. Synchronous.
GetAssayDescription	Get the descriptive information for a BioAssay, including the number of user-specified readouts (TIDs) and whether a score readout is present. Optionally get version and SID/CID count information. If GetFullDataBlob is set to true, then a Base64 string of data is returned in the response instead, containing the full PubChem Assay description in the requested format (ASN or XML only). Synchronous.
GetDownloadUrl	Given a download key, return an FTP URL that may be used to download the requested file. Synchronous.
GetEntrezKey	Given a list key, return an Entrez history key (db, query key, and WebEnv) corresponding to that list. Synchronous.
GetEntrezUrl	Given an Entrez history key (db, query key, and WebEnv), return an HTTP URL that may be used to view the list in Entrez. Synchronous.
GetIDList	Given a list key, return the identifiers as an array of integers. Note that this method expects there to be at least one identifier in the list, and will fault if the list is empty; see GetListItemsCount, which can be used to check for an empty list prior to calling GetIDList. The optional Start (zero-based) and Count parameters can be used to return smaller portions of the list, useful especially for large lists. Synchronous.
GetListItemsCount	Return the number of IDs in the set represented by the given list key. Synchronous.
GetOperationStatus	Given a key for any asynchronous operation, return the status of that operation. Possible return values are: Success, the operation completed normally; HitLimit, TimeLimit: the operation finished normally, but one of the limits was reached (e.g. before the entire database was searched); ServerError, InputError, DataError, Stopped: there was a problem with the input or on the server, and the job has died; Queued: the operation is waiting its turn in the public queue; Running: the operation is in progress. Synchronous.
GetStandardizedCID	Given a structure key that has been processed by Standardize, return the corresponding PubChem Compound database CID, or an empty value if the structure is not present in PubChem. Synchronous.
GetStandardizedStructure	Given a structure key that has been processed by Standardize, return the chemical structure in as SMILES or InChI strings. Synchronous.
GetStandardizedStructureBase64	Given a structure key that has been processed by Standardize, return the chemical structure as ASN, XML, or SDF, returned as a Base64-encoded string. Synchronous.
GetStatusMessage	Given a key for any asynchronous operation, return any system messages (error messages, job info, etc.) associated with the operation, if any. Synchronous.
IdentitySearch	Search PubChem Compound for structures identical to the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.
IDExchange	Convert IDs from one type to another, using any one of a variety of CID matching algorithms. Output can be a list or a downloaded file; download file compression is optional and defaults to gzip (.gz). Returns a list or download key. Asynchronous.
InputAssay	Specify an assay table from a BioAssay AID. The table may be complete, concise, or include a ListKey-specified set of readouts (TIDs). By default, all tested substances are included, but can be restricted to a ListKey-specified set of SIDs or CIDs. Returns an assay key. Synchronous.
InputEntrez	Input an Entrez history key (db, query key, and WebEnv). Returns a list key. Synchronous.
InputList	Input a set of identifiers for a PubChem database, as an array of integers. Returns a list key. Synchronous.
InputListString	Input a set of identifiers for a PubChem database, as an array of strings. Returns a list key. Synchronous.
InputListText	Input a set of identifiers for a PubChem database, as a simple string of integer values separated by commas and/or whitespace. Returns a list key. Synchronous.
InputStructure	Input a chemical structure as a simple (one-line) string, either SMILES or InChI. Returns a structure key. Synchronous.
InputStructureBase64	Input a chemical structure in ASN.1 (text or binary), XML, or SDF format. The structure must be encoded as a Base64 string. Currently only single structures are supported. Returns a structure key. Synchronous.
MFSearch	Search PubChem Compound for structures of a given molecular formula, optionally allowing elements not specified to be present. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.
ScoreMatrix	Compute a matrix of scores from one or two lists of IDs (if one, the IDs will be self-scored), of the selected type and in the selected format. Compression is optional and defaults to gzip (.gz). Returns a download key. Asynchronous.
SimilaritySearch2D	Search PubChem Compound for structures similar to the one given by the structure key input, based on the given Tanimoto-based similarity score. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.
Standardize	Standardize the structure given by the structure key input, using the same algorithm PubChem uses to construct the Compound database. Returns a structure key. Asynchronous.
SubstructureSearch	Search PubChem Compound for structures containing the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.
SuperstructureSearch	Search PubChem Compound for structures contained within the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.
AssayDownload
Description

Given an assay key, prepare for download a file containing an assay data table in the selected format. See the assay query section of the PUG service documentation for more detail on the supported formats. Compression is optional and defaults to gzip (.gz). Returns a download key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/AssayDownload

Input (Literal)

The input of this method is the argument AssayDownload having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AssayKey	s:string	1..1
tns:AssayFormat	tns:AssayFormatType	1..1
tns:eCompress	tns:CompressType	0..1
Output (Literal)

The output of this method is the argument AssayDownloadResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:DownloadKey	s:string	1..1
Download
Description

Given a list key, prepare for download a file containing those records in the selected format. See the web download service documentation for more detail on the supported formats and file types. Returns a download key. Asynchronous. Note that if SynchronousSingleRecord is set to true, and the ListKey contains only a single ID, then a Base64 string of data is returned synchronously in the response, instead of going through the download file.

Action

http://pubchem.ncbi.nlm.nih.gov/Download

Input (Literal)

The input of this method is the argument Download having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
tns:eFormat	tns:FormatType	1..1
tns:eCompress	tns:CompressType	0..1
tns:Use3D	s:boolean	0..1
tns:N3DConformers	s:int	0..1
tns:SynchronousSingleRecord	s:boolean	0..1
Output (Literal)

The output of this method is the argument DownloadResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:DownloadKey	s:string	0..1
tns:DataBlob	tns:DataBlobType	0..1
GetAssayColumnDescription
Description

Get the description of column (readout) in a BioAssay, which may be the outcome, score, or a TID from the given AID. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetAssayColumnDescription

Input (Literal)

The input of this method is the argument GetAssayColumnDescription having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AID	s:int	1..1
tns:Heading	tns:HeadingType	1..1
tns:TID	s:int	0..1
Output (Literal)

The output of this method is the argument GetAssayColumnDescriptionResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ColumnDescription	tns:ColumnDescriptionType	1..1
GetAssayColumnDescriptions
Description

Get the description of all columns (readouts) in a BioAssay. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetAssayColumnDescriptions

Input (Literal)

The input of this method is the argument GetAssayColumnDescriptions having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AID	s:int	1..1
Output (Literal)

The output of this method is the argument GetAssayColumnDescriptionsResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ColumnDescription	tns:ColumnDescriptionType	1..*
GetAssayDescription
Description

Get the descriptive information for a BioAssay, including the number of user-specified readouts (TIDs) and whether a score readout is present. Optionally get version and SID/CID count information. If GetFullDataBlob is set to true, then a Base64 string of data is returned in the response instead, containing the full PubChem Assay description in the requested format (ASN or XML only). Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetAssayDescription

Input (Literal)

The input of this method is the argument GetAssayDescription having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AID	s:int	1..1
tns:GetVersion	s:boolean	0..1
tns:GetCounts	s:boolean	0..1
tns:GetFullDataBlob	s:boolean	0..1
tns:eFormat	tns:FormatType	0..1
Output (Literal)

The output of this method is the argument GetAssayDescriptionResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AssayDescription	tns:AssayDescriptionType	0..1
tns:DataBlob	tns:DataBlobType	0..1
GetDownloadUrl
Description

Given a download key, return an FTP URL that may be used to download the requested file. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetDownloadUrl

Input (Literal)

The input of this method is the argument GetDownloadUrl having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:DownloadKey	s:string	1..1
Output (Literal)

The output of this method is the argument GetDownloadUrlResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:url	s:string	1..1
GetEntrezKey
Description

Given a list key, return an Entrez history key (db, query key, and WebEnv) corresponding to that list. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetEntrezKey

Input (Literal)

The input of this method is the argument GetEntrezKey having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
Output (Literal)

The output of this method is the argument GetEntrezKeyResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:EntrezKey	tns:EntrezKey	1..1
GetEntrezUrl
Description

Given an Entrez history key (db, query key, and WebEnv), return an HTTP URL that may be used to view the list in Entrez. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetEntrezUrl

Input (Literal)

The input of this method is the argument GetEntrezUrl having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:EntrezKey	tns:EntrezKey	1..1
Output (Literal)

The output of this method is the argument GetEntrezUrlResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:url	s:string	1..1
GetIDList
Description

Given a list key, return the identifiers as an array of integers. Note that this method expects there to be at least one identifier in the list, and will fault if the list is empty; see GetListItemsCount, which can be used to check for an empty list prior to calling GetIDList. The optional Start (zero-based) and Count parameters can be used to return smaller portions of the list, useful especially for large lists. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetIDList

Input (Literal)

The input of this method is the argument GetIDList having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
tns:Start	s:int	0..1
tns:Count	s:int	0..1
Output (Literal)

The output of this method is the argument GetIDListResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:IDList	tns:ArrayOfInt	1..1
GetListItemsCount
Description

Return the number of IDs in the set represented by the given list key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetListItemsCount

Input (Literal)

The input of this method is the argument GetListItemsCount having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
Output (Literal)

The output of this method is the argument GetListItemsCountResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:count	s:int	1..1
GetOperationStatus
Description

Given a key for any asynchronous operation, return the status of that operation. Possible return values are: Success, the operation completed normally; HitLimit, TimeLimit: the operation finished normally, but one of the limits was reached (e.g. before the entire database was searched); ServerError, InputError, DataError, Stopped: there was a problem with the input or on the server, and the job has died; Queued: the operation is waiting its turn in the public queue; Running: the operation is in progress. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetOperationStatus

Input (Literal)

The input of this method is the argument GetOperationStatus of type tns:AnyKeyType having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AnyKey	s:string	1..1
Output (Literal)

The output of this method is the argument GetOperationStatusResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:status	tns:StatusType	1..1
GetStandardizedCID
Description

Given a structure key that has been processed by Standardize, return the corresponding PubChem Compound database CID, or an empty value if the structure is not present in PubChem. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetStandardizedCID

Input (Literal)

The input of this method is the argument GetStandardizedCID having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
Output (Literal)

The output of this method is the argument GetStandardizedCIDResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:CID	s:int	1..1
GetStandardizedStructure
Description

Given a structure key that has been processed by Standardize, return the chemical structure in as SMILES or InChI strings. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetStandardizedStructure

Input (Literal)

The input of this method is the argument GetStandardizedStructure having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
tns:format	tns:FormatType	1..1
Output (Literal)

The output of this method is the argument GetStandardizedStructureResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:structure	s:string	1..1
GetStandardizedStructureBase64
Description

Given a structure key that has been processed by Standardize, return the chemical structure as ASN, XML, or SDF, returned as a Base64-encoded string. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetStandardizedStructureBase64

Input (Literal)

The input of this method is the argument GetStandardizedStructureBase64 having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
tns:format	tns:FormatType	1..1
Output (Literal)

The output of this method is the argument GetStandardizedStructureBase64Response having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:structure	s:base64Binary	1..1
GetStatusMessage
Description

Given a key for any asynchronous operation, return any system messages (error messages, job info, etc.) associated with the operation, if any. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/GetStatusMessage

Input (Literal)

The input of this method is the argument GetStatusMessage of type tns:AnyKeyType having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AnyKey	s:string	1..1
Output (Literal)

The output of this method is the argument GetStatusMessageResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:message	s:string	1..1
IdentitySearch
Description

Search PubChem Compound for structures identical to the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/IdentitySearch

Input (Literal)

The input of this method is the argument IdentitySearch having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
tns:idOptions	tns:IdentitySearchOptions	1..1
tns:limits	tns:LimitsType	0..1
Output (Literal)

The output of this method is the argument IdentitySearchResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
IDExchange
Description

Convert IDs from one type to another, using any one of a variety of CID matching algorithms. Output can be a list or a downloaded file; download file compression is optional and defaults to gzip (.gz). Returns a list or download key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/IDExchange

Input (Literal)

The input of this method is the argument IDExchange having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:InputListKey	s:string	1..1
tns:Operation	tns:IDOperationType	1..1
tns:OutputType	tns:PCIDType	1..1
tns:OutputSourceName	s:string	0..1
tns:OutputFormat	tns:IDOutputFormatType	1..1
tns:ToWebEnv	s:string	0..1
tns:eCompress	tns:CompressType	0..1
Output (Literal)

The output of this method is the argument IDExchangeResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	0..1
tns:DownloadKey	s:string	0..1
InputAssay
Description

Specify an assay table from a BioAssay AID. The table may be complete, concise, or include a ListKey-specified set of readouts (TIDs). By default, all tested substances are included, but can be restricted to a ListKey-specified set of SIDs or CIDs. Returns an assay key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/InputAssay

Input (Literal)

The input of this method is the argument InputAssay having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AID	s:int	1..1
tns:Columns	tns:AssayColumnsType	1..1
tns:ListKeyTIDs	s:string	0..1
tns:ListKeySCIDs	s:string	0..1
tns:OutcomeFilter	tns:AssayOutcomeFilterType	0..1
Output (Literal)

The output of this method is the argument InputAssayResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:AssayKey	s:string	1..1
InputEntrez
Description

Input an Entrez history key (db, query key, and WebEnv). Returns a list key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/InputEntrez

Input (Literal)

The input of this method is the argument InputEntrez having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:EntrezKey	tns:EntrezKey	1..1
Output (Literal)

The output of this method is the argument InputEntrezResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
InputList
Description

Input a set of identifiers for a PubChem database, as an array of integers. Returns a list key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/InputList

Input (Literal)

The input of this method is the argument InputList having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ids	tns:ArrayOfInt	1..1
tns:idType	tns:PCIDType	1..1
Output (Literal)

The output of this method is the argument InputListResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
InputListString
Description

Input a set of identifiers for a PubChem database, as an array of strings. Returns a list key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/InputListString

Input (Literal)

The input of this method is the argument InputListString having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:strids	tns:ArrayOfString	1..1
tns:idType	tns:PCIDType	1..1
tns:SourceName	s:string	0..1
Output (Literal)

The output of this method is the argument InputListStringResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
InputListText
Description

Input a set of identifiers for a PubChem database, as a simple string of integer values separated by commas and/or whitespace. Returns a list key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/InputListText

Input (Literal)

The input of this method is the argument InputListText having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ids	s:string	1..1
tns:idType	tns:PCIDType	1..1
Output (Literal)

The output of this method is the argument InputListTextResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
InputStructure
Description

Input a chemical structure as a simple (one-line) string, either SMILES or InChI. Returns a structure key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/InputStructure

Input (Literal)

The input of this method is the argument InputStructure having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:structure	s:string	1..1
tns:format	tns:FormatType	1..1
Output (Literal)

The output of this method is the argument InputStructureResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
InputStructureBase64
Description

Input a chemical structure in ASN.1 (text or binary), XML, or SDF format. The structure must be encoded as a Base64 string. Currently only single structures are supported. Returns a structure key. Synchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/InputStructureBase64

Input (Literal)

The input of this method is the argument InputStructureBase64 having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:structure	s:base64Binary	1..1
tns:format	tns:FormatType	1..1
Output (Literal)

The output of this method is the argument InputStructureBase64Response having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
MFSearch
Description

Search PubChem Compound for structures of a given molecular formula, optionally allowing elements not specified to be present. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/MFSearch

Input (Literal)

The input of this method is the argument MFSearch having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:MF	s:string	1..1
tns:mfOptions	tns:MFSearchOptions	0..1
tns:limits	tns:LimitsType	0..1
Output (Literal)

The output of this method is the argument MFSearchResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
ScoreMatrix
Description

Compute a matrix of scores from one or two lists of IDs (if one, the IDs will be self-scored), of the selected type and in the selected format. Compression is optional and defaults to gzip (.gz). Returns a download key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/ScoreMatrix

Input (Literal)

The input of this method is the argument ScoreMatrix having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
tns:SecondaryListKey	s:string	0..1
tns:ScoreType	tns:ScoreTypeType	1..1
tns:MatrixFormat	tns:MatrixFormatType	1..1
tns:eCompress	tns:CompressType	0..1
tns:N3DConformers	s:int	0..1
tns:No3DParent	s:boolean	0..1
Output (Literal)

The output of this method is the argument ScoreMatrixResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:DownloadKey	s:string	1..1
SimilaritySearch2D
Description

Search PubChem Compound for structures similar to the one given by the structure key input, based on the given Tanimoto-based similarity score. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/SimilaritySearch2D

Input (Literal)

The input of this method is the argument SimilaritySearch2D having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
tns:simOptions	tns:SimilaritySearchOptions	1..1
tns:limits	tns:LimitsType	0..1
Output (Literal)

The output of this method is the argument SimilaritySearch2DResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
Standardize
Description

Standardize the structure given by the structure key input, using the same algorithm PubChem uses to construct the Compound database. Returns a structure key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/Standardize

Input (Literal)

The input of this method is the argument Standardize having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
Output (Literal)

The output of this method is the argument StandardizeResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
SubstructureSearch
Description

Search PubChem Compound for structures containing the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/SubstructureSearch

Input (Literal)

The input of this method is the argument SubstructureSearch having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
tns:ssOptions	tns:StructureSearchOptions	0..1
tns:limits	tns:LimitsType	0..1
Output (Literal)

The output of this method is the argument SubstructureSearchResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
SuperstructureSearch
Description

Search PubChem Compound for structures contained within the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

Action

http://pubchem.ncbi.nlm.nih.gov/SuperstructureSearch

Input (Literal)

The input of this method is the argument SuperstructureSearch having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:StrKey	s:string	1..1
tns:ssOptions	tns:StructureSearchOptions	0..1
tns:limits	tns:LimitsType	0..1
Output (Literal)

The output of this method is the argument SuperstructureSearchResponse having the structure defined by the following table.

Element	Type	Occurs

1..1
tns:ListKey	s:string	1..1
Complex Types
Name
tns:AnyKeyType
tns:ArrayOfInt
tns:ArrayOfString
tns:ArrayOfTargets
tns:AssayDescriptionType
tns:AssayTargetType
tns:ColumnDescriptionType
tns:DataBlobType
tns:EntrezKey
tns:IdentitySearchOptions
tns:LimitsType
tns:MFSearchOptions
tns:SimilaritySearchOptions
tns:StructureSearchOptions
tns:TestedConcentrationType
tns:AnyKeyType
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:AnyKey	s:string	1..1
tns:ArrayOfInt
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:int	s:int	1..*
tns:ArrayOfString
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:string	s:string	1..*
tns:ArrayOfTargets
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:Target	tns:AssayTargetType	1..*
tns:AssayDescriptionType
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:Name	s:string	0..1
tns:Description	tns:ArrayOfString	0..1
tns:Protocol	tns:ArrayOfString	0..1
tns:Comment	tns:ArrayOfString	0..1
tns:NumberOfTIDs	s:int	1..1
tns:HasScore	s:boolean	1..1
tns:Method	s:string	0..1
tns:Targets	tns:ArrayOfTargets	0..1
tns:Version	s:int	0..1
tns:Revision	s:int	0..1
tns:LastDataChange	s:int	0..1
tns:SIDCountAll	s:int	0..1
tns:SIDCountActive	s:int	0..1
tns:SIDCountInactive	s:int	0..1
tns:SIDCountInconclusive	s:int	0..1
tns:SIDCountUnspecified	s:int	0..1
tns:SIDCountProbe	s:int	0..1
tns:CIDCountAll	s:int	0..1
tns:CIDCountActive	s:int	0..1
tns:CIDCountInactive	s:int	0..1
tns:CIDCountInconclusive	s:int	0..1
tns:CIDCountUnspecified	s:int	0..1
tns:CIDCountProbe	s:int	0..1
tns:AssayTargetType
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:gi	s:int	1..1
tns:Name	s:string	0..1
tns:ColumnDescriptionType
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:Heading	tns:HeadingType	1..1
tns:TID	s:int	0..1
tns:Name	s:string	1..1
tns:Description	tns:ArrayOfString	0..1
tns:Type	s:string	1..1
tns:Unit	s:string	0..1
tns:TestedConcentration	tns:TestedConcentrationType	0..1
tns:ActiveConcentration	s:boolean	0..1
tns:DataBlobType
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:Data	s:base64Binary	1..1
tns:BlobFormat	tns:BlobFormatType	0..1
tns:eCompress	tns:CompressType	0..1
tns:EntrezKey
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:db	s:string	1..1
tns:key	s:string	1..1
tns:webenv	s:string	1..1
tns:IdentitySearchOptions
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:eIdentity	tns:IdentityType	1..1
tns:ToWebEnv	s:string	0..1
tns:LimitsType
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:seconds	s:int	0..1
tns:maxRecords	s:int	0..1
tns:ListKey	s:string	0..1
tns:MFSearchOptions
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:AllowOtherElements	s:boolean	1..1
tns:ToWebEnv	s:string	0..1
tns:SimilaritySearchOptions
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:threshold	s:int	1..1
tns:ToWebEnv	s:string	0..1
tns:StructureSearchOptions
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:MatchIsotopes	s:boolean	0..1
tns:MatchCharges	s:boolean	0..1
tns:MatchTautomers	s:boolean	0..1
tns:RingsNotEmbedded	s:boolean	0..1
tns:SingeDoubleBondsMatch	s:boolean	0..1
tns:ChainsMatchRings	s:boolean	0..1
tns:StripHydrogen	s:boolean	0..1
tns:eStereo	tns:StereoType	0..1
tns:ToWebEnv	s:string	0..1
tns:TestedConcentrationType
Derived By

Restricting s:anyType

Content Model

Contains elements as defined in the following table.

Component	Type	Occurs

1..1
tns:Concentration	s:double	1..1
tns:Unit	s:string	1..1
Simple Types
Name
tns:AssayColumnsType
tns:AssayFormatType
tns:AssayOutcomeFilterType
tns:BlobFormatType
tns:CompressType
tns:FormatType
tns:HeadingType
tns:IdentityType
tns:IDOperationType
tns:IDOutputFormatType
tns:MatrixFormatType
tns:PCIDType
tns:ScoreTypeType
tns:StatusType
tns:StereoType
tns:AssayColumnsType
Derived By

Restricting s:string

Enumeration

Value
eAssayColumns_Complete
eAssayColumns_Concise
eAssayColumns_TIDs
tns:AssayFormatType
Derived By

Restricting s:string

Enumeration

Value
eAssayFormat_XML
eAssayFormat_ASN_Text
eAssayFormat_ASN_Binary
eAssayFormat_CSV
tns:AssayOutcomeFilterType
Derived By

Restricting s:string

Enumeration

Value
eAssayOutcome_All
eAssayOutcome_Inactive
eAssayOutcome_Active
eAssayOutcome_Inconclusive
eAssayOutcome_Unspecified
tns:BlobFormatType
Derived By

Restricting s:string

Enumeration

Value
eBlobFormat_Unspecified
eBlobFormat_ASNB
eBlobFormat_ASNT
eBlobFormat_XML
eBlobFormat_SDF
eBlobFormat_CSV
eBlobFormat_Text
eBlobFormat_HTML
eBlobFormat_PNG
eBlobFormat_Other
tns:CompressType
Derived By

Restricting s:string

Enumeration

Value
eCompress_None
eCompress_GZip
eCompress_BZip2
tns:FormatType
Derived By

Restricting s:string

Enumeration

Value
eFormat_ASNB
eFormat_ASNT
eFormat_XML
eFormat_SDF
eFormat_SMILES
eFormat_InChI
eFormat_Image
eFormat_Thumbnail
tns:HeadingType
Derived By

Restricting s:string

Enumeration

Value
TID
outcome
score
tns:IdentityType
Derived By

Restricting s:string

Enumeration

Value
eIdentity_SameConnectivity
eIdentity_AnyTautomer
eIdentity_SameStereo
eIdentity_SameIsotope
eIdentity_SameStereoIsotope
eIdentity_SameNonconflictStereo
eIdentity_SameIsotopeNonconflictStereo
tns:IDOperationType
Derived By

Restricting s:string

Enumeration

Value
eIDOperation_Same
eIDOperation_SameStereo
eIDOperation_SameIsotope
eIDOperation_SameConnectivity
eIDOperation_SameParent
eIDOperation_SameParentStereo
eIDOperation_SameParentIsotope
eIDOperation_SameParentConnectivity
eIDOperation_Similar2D
eIDOperation_Similar3D
tns:IDOutputFormatType
Derived By

Restricting s:string

Enumeration

Value
eIDOutputFormat_Entrez
eIDOutputFormat_FileList
eIDOutputFormat_FilePair
tns:MatrixFormatType
Derived By

Restricting s:string

Enumeration

Value
eMatrixFormat_CSV
eMatrixFormat_IdIdScore
tns:PCIDType
Derived By

Restricting s:string

Enumeration

Value
eID_CID
eID_SID
eID_AID
eID_TID
eID_ConformerID
eID_SourceID
eID_InChI
eID_InChIKey
tns:ScoreTypeType
Derived By

Restricting s:string

Enumeration

Value
eScoreType_Sim2DSubs
eScoreType_ShapeOpt3D
eScoreType_FeatureOpt3D
tns:StatusType
Derived By

Restricting s:string

Enumeration

Value
eStatus_Unknown
eStatus_Success
eStatus_ServerError
eStatus_HitLimit
eStatus_TimeLimit
eStatus_InputError
eStatus_DataError
eStatus_Stopped
eStatus_Running
eStatus_Queued
tns:StereoType
Derived By

Restricting s:string

Enumeration

Value
eStereo_Ignore
eStereo_Exact
eStereo_Relative
eStereo_NonConflicting



Power User Gateway (PUG)
Introduction
The PubChem Power User Gateway (PUG) provides access to PubChem services via a programmatic interface. The basic design principle is straightforward. There is a single CGI (pug.cgi, referred to hereafter as simply PUG) that is the central gateway to multiple PubChem functions. PUG takes no URL arguments; all communication with PUG is through XML. To perform any request, one formulates input in XML and then HTTP POST it to PUG. The CGI interprets your incoming request, initiates the appropriate action, then returns results (also) in XML format. (This document assumes a basic familiarity with XML tags and data structures. To learn more about XML, visit the URL: https://en.wikipedia.org/wiki/XML)

PubChem services are queued. As such, a submitted task will (usually) complete sometime after PUG responds to the initial request. The initial PUG response contains the request ID of your task.  This request ID must be used for further communication with PUG concerning your submitted task. When PUG is interrogated about an outstanding request using the request ID, PUG will return either the results of your task, if completed, or the status of your task.

Each PubChem service enabled for use with PUG is documented separately. This service by service documentation will detail the input, output, and options. All XML used by PUG is specified in the data type definition (DTD), which may be found at: https://pubchem.ncbi.nlm.nih.gov/pug/pug.dtd or in the equivalent XML Schema definition at: https://pubchem.ncbi.nlm.nih.gov/pug/pug.xsd.

We strongly recommend using an XML parser/generator tool to read and write the XML data, rather than composing XML manually. 

PubChem PUG enabled services have the ability to save and open valid PUG requests designed for that service. You can use this feature to learn how to compose valid PUG XML requests and to verify that your PUG XML request does what is intended. Examples of such services provided in this document.

Additional documentation on PubChem and its services may be found at https://pubchem.ncbi.nlm.nih.gov and via help links throughout PubChem's web site. If you cannnot find what you need there, further requests for information or help may be sent to the highly knowledgeable and responsive NCBI help desk at info@ncbi.nlm.nih.gov.

503 HTTP STATUS CODE: Please note that this status code may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

Interacting with PUG
All communication to PUG is via XML sent to the CGI at the URL: https://pubchem.ncbi.nlm.nih.gov/pug/pug.cgi

The primary data container used in all transactions is <PCT-Data>, the top-level container for any PUG input or output.  ("PCT" stands for PubChem Tools, a data specification that is shared by both PUG and internal PubChem applications.  See the introduction in this document for more information.)  This <PCT-Data> object may contain either a <PCT-InputData> or a <PCT-OutputData> object.  Users of  PUG will always send <PCT-Data> containing <PCT-InputData>, and always receive <PCT-Data> containing <PCT-OutputData>.

After a new task is submitted to PUG, your request is queued, rather than executing immediately.  As such, PUG  will return an XML message containing a request ID to be used for further actions on your request.  In the example PUG XML reply below, the message says that the request was successfully submitted and that the request ID is "402936103567975582".  It will then be up to you to (periodically) poll PUG, using the request ID, until your task is complete.  When your task is completed, PUG will return the result; otherwise it will simply return a status message.  See examples in other sections of this document on how to properly poll PUG.

Example of a PUG reply to a newly submitted request:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_waiting>  
          <PCT-Waiting>  
            <PCT-Waiting_reqid>402936103567975582</PCT-Waiting_reqid>  
          </PCT-Waiting>  
        </PCT-OutputData_output_waiting>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
The <PCT-InputData> object is a choice between request types.  Tasks specific to various PubChem services are contained by <PCT-InputData> and are described in different sections of this document.  Primary to the use of PUG is the <PCT-InputData> input type used to perform request management, <PCT-Request>.  Request management enables you to enquire about the status of or to cancel a previous PUG request.  For example, to cancel a PUG request with request ID "402936103567975582", the PUG XML input message will look like this:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_request>  
        <PCT-Request>  
          <PCT-Request_reqid>402936103567975582</PCT-Request_reqid>  
          <PCT-Request_type value="cancel"/>  
        </PCT-Request>  
      </PCT-InputData_request>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
The <PCT-OutputData> object contained in the output from PUG will always include a status message in a <PCT-Status-Message>, which consists of an enumerated status in <PCT-Status> and an optional message string.  When a new task is queued by PUG, the <PCT-OutputData> returned to you will (likely) contain a <PCT-Waiting> which contains your request ID.  If the request finishes quickly, the initially returned <PCT-OutputData> object will actually contain the appropriate result of your task specific to the requested service.  Similarly, when polling PUG using your request ID, the <PCT-OutputData> object will contain either your task result or a status message.

PUG Tasks
PubChem services currently enabled for use by PUG include:

PubChem Record downloads (see also the help page for bulk downloads)
PubChem Compound Structure Search (https://pubchem.ncbi.nlm.nih.gov/search/search.cgi)
PubChem Structure Standardization (https://pubchem.ncbi.nlm.nih.gov/standardize/standardize.cgi)
Each PUG service has its own expected input and provided output. The sections below detail how to use each service with PUG.

Download Tasks
This service allows you to download sets of PubChem records - substances or compounds - using PUG's <PCT-Download> sub-object. You will need to specify which records to download, using a <PCT-QueryUids> object, the desired output format (ASN.1, XML, or SDF), and, optionally, the desired compression method (gzip or bzip2). The options available through PUG are equivalent to those for the interactive PubChem Download service.

The <PCT-QueryUids> object enables you to specify an explicit list of record IDs, or to provide an existing Entrez history key (see eUtils documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/) from either the PubChem Compound ("pccompound") or the PubChem Substance ("pcsubstance") Entrez databases.  Currently there is an upper limit of 250,000 structures per download request; if you find this limit too restrictive for your purposes, please consider using the PubChem FTP site which contains all available PubChem contents: https://ftp.ncbi.nlm.nih.gov/pubchem/

When your download request is successfully completed, the returned <PCT-OutputData> object will hold a <PCT-Download-URL> containing the URL you may use to download your results.  Again, please note that the result of a download task is an URL, not the record data itself (which may be quite large).  To obtain the data requested, you must use the provided URL.

Example: You want to download CID 1 and CID 99, being uids 1 and 99 in the "pccompound" Entrez database, in SDF format with gzip compression.

The typical flow of information is as follows.  First, the initial input XML is sent to PUG via HTTP POST.  Note the input data container with the download request and uid and format options:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_download>  
        <PCT-Download>  
          <PCT-Download_uids>  
            <PCT-QueryUids>  
              <PCT-QueryUids_ids>  
                <PCT-ID-List>  
                  <PCT-ID-List_db>pccompound</PCT-ID-List_db>  
                  <PCT-ID-List_uids>  
                    <PCT-ID-List_uids_E>1</PCT-ID-List_uids_E>  
                    <PCT-ID-List_uids_E>99</PCT-ID-List_uids_E>  
                  </PCT-ID-List_uids>  
                </PCT-ID-List>  
              </PCT-QueryUids_ids>  
            </PCT-QueryUids>  
          </PCT-Download_uids>  
          <PCT-Download_format value="sdf"/>  
          <PCT-Download_compression value="gzip"/>  
        </PCT-Download>  
      </PCT-InputData_download>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
If the request is small and finishes very quickly, you may get a final URL right away (see further below). But usually PUG will respond initially with a waiting message and a request ID (<PCT-Waitingreqid>) such as:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_waiting>  
          <PCT-Waiting>  
            <PCT-Waiting_reqid>402936103567975582</PCT-Waiting_reqid>  
          </PCT-Waiting>  
        </PCT-OutputData_output_waiting>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
You would then parse out this request id, being "402936103567975582", in this case, and use this id to "poll" PUG on the status of the request, composing an XML message like:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_request>  
        <PCT-Request>  
          <PCT-Request_reqid>402936103567975582</PCT-Request_reqid>  
          <PCT-Request_type value="status"/>  
        </PCT-Request>  
      </PCT-InputData_request>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
Note that here the request type "status" is used; there is also the request type "cancel" that you may use to cancel a running job.

If the request is still running, you well get back another waiting message as above, and then you would poll again after some reasonable interval. If the request is finished, you will get a final result message like:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_download-url>  
          <PCT-Download-URL>  
            <PCT-Download-URL_url>  
              ftp://ftp-private.ncbi.nlm.nih.gov/pubchem/.fetch/1064385222466625960.sdf.gz  
            </PCT-Download-URL_url>  
          </PCT-Download-URL>  
        </PCT-OutputData_output_download-url>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
You would parse out the URL from the <PCT-Download-URL_url> tag, and then use a tool of your choice to connect to that URL to retrieve the actual requested data.

Query Tasks
The <PCT-Query> object may be used to perform queries against PubChem data that are not possible using Entrez. The <PCT-Query> object consists of a series of queries and a database to query against. One must be careful when formulating queries to select compatible database and query types, as outlined in the documentation of each query task type. For example, you will not want to perform a chemical similarity search on a list of bioassay identifiers (AIDs), since chemical searches may only be performed on compound identifiers (CIDs).

The <PCT-Query> object can perform multiple queries in a single request. The semantic of multiple queries in a single task is to "AND" the result between queries, which is to say that the resulting list of identifiers will satisfy all queries requested. Sometimes it is best to perform multiple search tasks individually rather than in a single task, unless otherwise noted in the task documentation.

Chemical Structure Query
To perform PubChem Compound structure searches using PUG, you will need to make a request using a <PCT-Query> object. Chemical structure search tasks use the query objects <PCT-QueryCompoundCS> and <PCT-QueryCompoundEL>. You may submit a structure search by mixing and matching more than one of these two query types in a series. Furthermore, only the PubChem Compound ("pccompound") Entrez database may be specified in <PCT-QueryUids>, when performing chemical structure queries.

The  and  objects can encode many different types of chemical structure searches.  To help you understand how to encode a structure search, please consider using the PubChem Structure Search web site. It has the ability to translate your structure search query into the XML necessary for use with PUG, and can be very helpful to demonstrate how to encode complex queries. The PubChem Structure Search system is located at the URL: https://pubchem.ncbi.nlm.nih.gov/search/.

Please note that the output result of a chemical structure search is an Entrez history key (see eUtils documentation). To obtain the list of compounds matching your query, you must use eUtils; more information on eUtils is below.There is currently a limit of two million compound identifiers returned by the structure search (through either PUG or the interactive web site).

Example:  You wish to perform a chemical similarity search of CID 2244 at a Tanimoto similarity value of 80% with at most 300 results returned.

The initial HTTP POST to PUG to initiate the search would contain XML like:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_query>  
        <PCT-Query>  
          <PCT-Query_type>  
            <PCT-QueryType>  
              <PCT-QueryType_css>  
                <PCT-QueryCompoundCS>  
                  <PCT-QueryCompoundCS_query>  
                    <PCT-QueryCompoundCS_query_data>2244</PCT-QueryCompoundCS_query_data>  
                  </PCT-QueryCompoundCS_query>  
                  <PCT-QueryCompoundCS_type>  
                    <PCT-QueryCompoundCS_type_similar>  
                      <PCT-CSSimilarity>  
                        <PCT-CSSimilarity_threshold>80</PCT-CSSimilarity_threshold>  
                      </PCT-CSSimilarity>  
                    </PCT-QueryCompoundCS_type_similar>  
                  </PCT-QueryCompoundCS_type>  
                  <PCT-QueryCompoundCS_results>300</PCT-QueryCompoundCS_results>  
                </PCT-QueryCompoundCS>  
              </PCT-QueryType_css>  
            </PCT-QueryType>  
          </PCT-Query_type>  
        </PCT-Query>  
      </PCT-InputData_query>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
If the request is processed and started successfully, PUG would respond with a waiting message and request id, for example:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_waiting>  
          <PCT-Waiting>  
            <PCT-Waiting_reqid>271473836860076709</PCT-Waiting_reqid>  
            <PCT-Waiting_message>Structure search job was submitted</PCT-Waiting_message>  
          </PCT-Waiting>  
        </PCT-OutputData_output_waiting>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
You would then use this request ID, "271473836860076709" in this case, to "poll" PUG for the status of the request:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_request>  
        <PCT-Request>  
          <PCT-Request_reqid>271473836860076709</PCT-Request_reqid>  
          <PCT-Request_type value="status"/>  
        </PCT-Request>  
      </PCT-InputData_request>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
If the search is still running, you would get another waiting message as above, and you would then need to poll again after a reasonable interval.  If the search task is completed, PUG would give an Entrez history key for the resulting CID (compound identifier) list:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
          <PCT-Status-Message_message>Your  
     search has already been completed.</PCT-Status-Message_message>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_entrez>  
          <PCT-Entrez>  
            <PCT-Entrez_db>pccompound</PCT-Entrez_db>  
            <PCT-Entrez_query-key>1</PCT-Entrez_query-key>  
            <PCT-Entrez_webenv>  
          0Hm9YDD1X4wor4nONvSWx9vkKmEqFXTiq84JO47pgxmSw_  
          cIuDBVcG46Yr@2B5C47D162BBD720_0008SID  
     </PCT-Entrez_webenv>  
          </PCT-Entrez>  
        </PCT-OutputData_output_entrez>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
More information on using Entrez history (and eUtils) to retrieve hit lists is below.

If for some reason your initial query cannot be properly interpreted, PUG would respond with an error message with some indication of the problem encountered:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="data-error"/>  
          </PCT-Status-Message_status>  
          <PCT-Status-Message_message>Programatic  
            Error:Non-decodeable query specified.  
     Input a valid SMILE/SMARTS or a CID.</PCT-Status-Message_message>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
If you wish to cancel a queued or running request, you would send to PUG:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_request>  
        <PCT-Request>  
          <PCT-Request_reqid>271473836860076709</PCT-Request_reqid>  
          <PCT-Request_type value="cancel"/>  
        </PCT-Request>  
      </PCT-InputData_request>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
And when PUG cancels your task, you would get back:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="running"/>  
          </PCT-Status-Message_status>  
          <PCT-Status-Message_message>Your search will be stopped, please wait...  
   </PCT-Status-Message_message>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_waiting>  
          <PCT-Waiting>  
            <PCT-Waiting_reqid>271473836860076709</PCT-Waiting_reqid>  
            <PCT-Waiting_message>Your search will be stopped, please wait...  
     </PCT-Waiting_message>  
          </PCT-Waiting>  
        </PCT-OutputData_output_waiting>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
PubChem BioAssay Description
PubChem has discontinued several bioactivity analysis tools since November 1, 2018. This includes the BioActivity Summary, BioActivity DataTable, SAR, Structure Clustering, and Plot Service. A help document page is available outlining alternatives with the same or similar functionality, see https://pubchem.ncbi.nlm.nih.gov/docs/legacy-bioassay-tools

The only BioAssay service still accessible through PUG is the assay description.

Example: You wish to determine the TID number of "IC-50" for AID 523.

The HTTP POST to PUG to get the full description, including columns, would contain XML like:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_query>  
        <PCT-Query>  
          <PCT-Query_type>  
            <PCT-QueryType>  
              <PCT-QueryType_asd>  
                <PCT-QueryAssayDescription>  
                  <PCT-QueryAssayDescription_aid>523</PCT-QueryAssayDescription_aid>  
                  <PCT-QueryAssayDescription_get-columns value="true"/>  
                </PCT-QueryAssayDescription>  
              </PCT-QueryType_asd>  
            </PCT-QueryType>  
          </PCT-Query_type>  
        </PCT-Query>  
      </PCT-InputData_query>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
Standardization
The PubChem Standardization service allows you to standardize the representation of a chemical structure using a <PCT-Standardize> sub-object. PubChem uses a normalization procedure on all PubChem substance records to remove variation due to different representations of functional groups, tautomeric or resonance forms, etc., to create the PubChem Compound database, which contains the unique chemical structures in the PubChem Substance database. This procedure verifies and validates that a chemical structure is reasonable (to a certain degree) through examination of the atoms and their valence and involves a valence bond canonicalization processing for tautomer invariance. The input to structure standardization is a chemical structure and the output is either a failure message or a chemical structure. To use this service, you will need to specify an input structure and its format. You also need to specify the output format you desire. This service operates on only a single structure at a time.

Example:  You would like to standardize the representation of guanine input in SMILES format and output in SDF format.

The typical flow of information is as follows. First, the initial input XML is sent to PUG via HTTP POST. Note the input data container with the download request and uid and format options:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_standardize>  
        <PCT-Standardize>  
          <PCT-Standardize_structure>  
            <PCT-Structure>  
              <PCT-Structure_structure>  
                <PCT-Structure_structure_string>C1=NC2=C(N1)C(=O)N=C(N2)N  
                </PCT-Structure_structure_string>  
              </PCT-Structure_structure>  
              <PCT-Structure_format>  
                <PCT-StructureFormat value="smiles"/>  
              </PCT-Structure_format>  
            </PCT-Structure>  
          </PCT-Standardize_structure>  
          <PCT-Standardize_oformat>  
            <PCT-StructureFormat value="smiles"/>  
          </PCT-Standardize_oformat>  
        </PCT-Standardize>  
      </PCT-InputData_standardize>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
If the request is small and finishes very quickly, you may get a final URL right away (see further below). But usually PUG will respond initially with a waiting message and a request ID () such as:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_waiting>  
          <PCT-Waiting>  
            <PCT-Waiting_reqid>402936103567975582</PCT-Waiting_reqid>  
          </PCT-Waiting>  
        </PCT-OutputData_output_waiting>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
You would then parse out this request id, being "402936103567975582", in this case, and use this id to "poll" PUG on the status of the request, composing an XML message like:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_request>  
        <PCT-Request>  
          <PCT-Request_reqid>402936103567975582</PCT-Request_reqid>  
          <PCT-Request_type value="status"/>  
        </PCT-Request>  
      </PCT-InputData_request>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
Note that here the request type "status" is used; there is also the request type "cancel" that you may use to cancel a running job.

If the request is still running, you well get back another waiting message as above, and then you would poll again after some reasonable interval. If the request is finished, you will get a final result message like:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_structure>  
          <PCT-Structure>  
            <PCT-Structure_structure>  
              <PCT-Structure_structure_string>C1=NC2=C(N1)C(=O)N=C(N2)N  
              </PCT-Structure_structure_string>  
            </PCT-Structure_structure>  
            <PCT-Structure_format>  
              <PCT-StructureFormat value="smiles"/>  
            </PCT-Structure_format>  
          </PCT-Structure>  
        </PCT-OutputData_output_structure>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
You would parse out the output from the <PCT-Download-URL_url> tag to retrieve the standardized structure.

PUG, NCBI eUtils, and Entrez History
NCBI's Entrez integrates the scientific literature, DNA and protein sequence databases, 3D protein structure and protein domain data, population study datasets, expression data, assemblies of complete genomes, taxonomic information, and PubChem Compound, Substance, and BioAssay databases (among others) into a tightly interlinked system. It is a retrieval system designed for searching its linked databases. Entrez history provides a record of the searches performed during a search session. PubChem communicates with Entrez history through Entrez Programming Utilities (eUtils) to enhance data analysis.

NCBI's eUtils are used extensively by PubChem services. Results from queries are often provided in the form of an Entrez history, which represents a list of database specific identifiers within the Entrez search system. These identifiers are, for example, your PubChem CIDs (compound identifiers). This allows you, the user, to interact with other Entrez databases and to perform hit list management tasks using eUtils, e.g., to logically combine the results of different queries using AND, OR, or NOT operations. PubChem services typically accept an Entrez history as a means to provide a subset of identifiers as input, so that your query operates only on a subset of a PubChem database contents. Use of Entrez history can help you avoid sending and receiving (potentially) very large lists of identifiers.

To learn more about eUtils, please visit the URL: https://www.ncbi.nlm.nih.gov/books/NBK25501/

Histories in Entrez are database specific. Each time an Entrez search is executed, the search terms, the time the search was executed, and the search results are numbered consecutively and saved automatically in Entrez history for that database. The history can be recalled at any time during a search session, but histories are lost after 8 hours of inactivity. There is also a running limit of 100 searches (across all databases) saved in any given session.

PUG is integrated with Entrez in that it may use Entrez history keys (also know as "webenv" keys) as both input and output, depending on the task. For example, structure search via PUG may return an Entrez history, and the resulting hit list can be retrieved as a list of CIDs using Entrez's eFetch utility. PUG can also take a history key as input, if you wanted to download the records resulting from either a prior structure search or a programmatic Entrez search via the eSearch utility. (See the eUtils documentation for more details.)

Entrez histories are referred to programmatically by the trio of a database name, a WebEnv string, and a query key number. You can see this in the example structure search above. The part of PUG's response that contains this information is the <PCT-Entrez> tag:

<PCT-Entrez>  
  <PCT-Entrez_db>pccompound</PCT-Entrez_db>  
  <PCT-Entrez_query-key>1</PCT-Entrez_query-key>  
  <PCT-Entrez_webenv>  
      0Hm9YDD1X4wor4nONvSWx9vkKmEqFXTiq84JO47pgxmSw_cIuDBVcG46Yr@2B5C47D162BBD720_0008SID  
  </PCT-Entrez_webenv>  
</PCT-Entrez>
This Entrez history information may be used in a variety of ways. If you want to view these hits on a regular web page, you can direct a browser to an URL as follows, which shows the results in HTML in the usual Entrez docsum format:

https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Select+from+History&WebEnvRq=1&db=pccompound&query_key=1&WebEnv=0Hm9YDD1X4wor4nONvSWx9vkKmEqFXTiq84JO47pgxmSw_cIuDBVcG46Yr@2B5C47D162BBD720_0008SID

On the other hand, if you are writing an application and want to retrieve the hit list directly via HTTP, you can use eFetch with the same information, which can return the list in XML (with its own DTD/XSD that is not related to PUG's), for example:

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?retmode=xml&rettype=uilist&WebEnvRq=1&db=pccompound&query_key=1&WebEnv=0Hm9YDD1X4wor4nONvSWx9vkKmEqFXTiq84JO47pgxmSw_cIuDBVcG46Yr@2B5C47D162BBD720_0008SID

Finally, if you want to download the compounds from this search in, e.g., SDF format with gzip compression, you would send PUG a request with the  information instead of an explicit CID list. From here, the download process would continue as in the example above.

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_download>  
        <PCT-Download>  
          <PCT-Download_uids>  
            <PCT-QueryUids>  
              <PCT-QueryUids_entrez>  
                <PCT-Entrez>  
                  <PCT-Entrez_db>pccompound</PCT-Entrez_db>  
                  <PCT-Entrez_query-key>1</PCT-Entrez_query-key>  
                  <PCT-Entrez_webenv>  
                   0Hm9YDD1X4wor4nONvSWx9vkKmEqFXTiq84JO47pgxmSw_cIuDBVcG46Yr@2B5C47D162BBD720_0008SID  
                  </PCT-Entrez_webenv>  
                </PCT-Entrez>  
              </PCT-QueryUids_entrez>  
            </PCT-QueryUids>  
          </PCT-Download_uids>  
          <PCT-Download_format value="sdf"/>  
          <PCT-Download_compression value="gzip"/>  
        </PCT-Download>  
      </PCT-InputData_download>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
PUG and eUtils together make possible a wide variety of powerful programmatic data analysis tools for PubChem and other Entrez databases.

PUG and SOAP
There is a SOAP wrapper for PUG, see: https://pubchem.ncbi.nlm.nih.gov/docs/pug-soap

The interface includes much of PUG's functionality, but with simplified functions that are accessible from GUI workflow applications and SOAP-aware programming languages.

FAQs
Some simple workflows help to illustrate the use of PUG. All PUG messages must be sent via a HTTP POST to the URL: https://pubchem.ncbi.nlm.nih.gov/pug/pug.cgi

Scenario 1. I would like to retrieve the SMILES (in gzip compressed format) for a list of PubChem Compound CIDs: 1, 2, and 3.

Compose your PUG message:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_download>  
        <PCT-Download>  
          <PCT-Download_uids>  
            <PCT-QueryUids>  
              <PCT-QueryUids_ids>  
                <PCT-ID-List>  
                  <PCT-ID-List_db>pccompound</PCT-ID-List_db>  
                  <PCT-ID-List_uids>  
                    <PCT-ID-List_uids_E>1</PCT-ID-List_uids_E>  
                    <PCT-ID-List_uids_E>2</PCT-ID-List_uids_E>  
                    <PCT-ID-List_uids_E>3</PCT-ID-List_uids_E>  
                  </PCT-ID-List_uids>  
                </PCT-ID-List>  
              </PCT-QueryUids_ids>  
            </PCT-QueryUids>  
          </PCT-Download_uids>  
          <PCT-Download_format value="smiles"/>  
          <PCT-Download_compression value="gzip"/>  
        </PCT-Download>  
      </PCT-InputData_download>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
PUG will send you back a response, for example:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_waiting>  
          <PCT-Waiting>  
            <PCT-Waiting_reqid>402936103567975582</PCT-Waiting_reqid>  
          </PCT-Waiting>  
        </PCT-OutputData_output_waiting>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
This response contains a request ID, being "402936103567975582". You will use this request ID to query PUG on the status of your request by composing and sending another PUG message, as such:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_request>  
        <PCT-Request>  
          <PCT-Request_reqid>402936103567975582</PCT-Request_reqid>  
          <PCT-Request_type value="status"/>  
        </PCT-Request>  
      </PCT-InputData_request>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
If your request is still being processed, you will receive a response message as before. When your request completes, PUG will return an XML message like:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_download-url>  
          <PCT-Download-URL>  
            <PCT-Download-URL_url>  
              ftp://ftp-private.ncbi.nlm.nih.gov/pubchem/.fetch/656213441898678492.txt.gz  
            </PCT-Download-URL_url>  
          </PCT-Download-URL>  
        </PCT-OutputData_output_download-url>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
The PUG response gives you an URL where you may retrieve your results: 
ftp://ftp-private.ncbi.nlm.nih.gov/pubchem/.fetch/656213441898678492.txt.gz

Scenario 2a. I have a SMILES of L-tyrosine and I would like to get back an SDF file containing the PubChem Compound record(s) exactly matching this structure (with the same stereo and isotopes).

The workflow for this scenario is very similar to Scenario 1, where you .

Borrowing the workflow from the first scenario, the PUG message you HTTP POST would be:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_query>  
        <PCT-Query>  
          <PCT-Query_type>  
            <PCT-QueryType>  
              <PCT-QueryType_css>  
                <PCT-QueryCompoundCS>  
                  <PCT-QueryCompoundCS_query>  
                    <PCT-QueryCompoundCS_query_data>C1=CC(=CC=C1C\[C@@H\](C(=O)O)N)O  
                    </PCT-QueryCompoundCS_query_data>  
                  </PCT-QueryCompoundCS_query>  
                  <PCT-QueryCompoundCS_type>  
                    <PCT-QueryCompoundCS_type_identical>  
                      <PCT-CSIdentity value="same-stereo-isotope">5</PCT-CSIdentity>  
                    </PCT-QueryCompoundCS_type_identical>  
                  </PCT-QueryCompoundCS_type>  
                  <PCT-QueryCompoundCS_results>2000000</PCT-QueryCompoundCS_results>  
                </PCT-QueryCompoundCS>  
              </PCT-QueryType_css>  
            </PCT-QueryType>  
          </PCT-Query_type>  
        </PCT-Query>  
      </PCT-InputData_query>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
The eventual result of the search will look something like:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
          <PCT-Status-Message_message>Your search has completed successfully!  
          </PCT-Status-Message_message>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_entrez>  
          <PCT-Entrez>  
            <PCT-Entrez_db>pccompound</PCT-Entrez_db>  
            <PCT-Entrez_query-key>3</PCT-Entrez_query-key>  
            <PCT-Entrez_webenv>  
            0hJ--NzxiSKFxJzc4SnMb5PvxBP8HKJvZ-2s-XE19WBZSHG0xIO_k_xPrU@1FBE6DE17A397ED0_0011SID  
            </PCT-Entrez_webenv>  
          </PCT-Entrez>  
        </PCT-OutputData_output_entrez>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
When the query is complete, the result is an Entrez query key and webenv. The query key identifies the query result and the webenv provides your session identifier. You use this Entrez query key and webenv as your source of CIDs to compose another PUG message to download the gzipped compressed SDF file of the query hits:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_download>  
        <PCT-Download>  
          <PCT-Download_uids>  
            <PCT-QueryUids>  
              <PCT-QueryUids_entrez>  
                <PCT-Entrez>  
                  <PCT-Entrez_db>pccompound</PCT-Entrez_db>  
                  <PCT-Entrez_query-key>3</PCT-Entrez_query-key>  
                  <PCT-Entrez_webenv>  
                  0hJ--NzxiSKFxJzc4SnMb5PvxBP8HKJvZ-2s-XE19WBZSHG0xIO_k_xPrU@1FBE6DE17A397ED0_0011SID  
                  </PCT-Entrez_webenv>  
                </PCT-Entrez>  
              </PCT-QueryUids_entrez>  
            </PCT-QueryUids>  
          </PCT-Download_uids>  
          <PCT-Download_format value="sdf"/>  
          <PCT-Download_compression value="gzip"/>  
        </PCT-Download>  
      </PCT-InputData_download>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
The final result, as in the first scenario, will contain an URL to the results containing CID 6057:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_download-url>  
          <PCT-Download-URL>  
            <PCT-Download-URL_url>  
            ftp://ftp-private.ncbi.nlm.nih.gov/pubchem/.fetch/693081357064045880.sdf.gz  
            </PCT-Download-URL_url>  
          </PCT-Download-URL>  
        </PCT-OutputData_output_download-url>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
Scenario 2b. I have a SMILES of L-tyrosine and I would like to get back an SDF file containing the PubChem Compound records containing the same isotopes (but stereo can be different).

This scenario is identical to Scenario 2a, except that the initial PUG message would look like:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_query>  
        <PCT-Query>  
          <PCT-Query_type>  
            <PCT-QueryType>  
              <PCT-QueryType_css>  
                <PCT-QueryCompoundCS>  
                  <PCT-QueryCompoundCS_query>  
                    <PCT-QueryCompoundCS_query_data>  
                    C1=CC(=CC=C1C\[C@@H\](C(=O)O)N)O</PCT-QueryCompoundCS_query_data>  
                  </PCT-QueryCompoundCS_query>  
                  <PCT-QueryCompoundCS_type>  
                    <PCT-QueryCompoundCS_type_identical>  
                      <PCT-CSIdentity value="same-isotope">4</PCT-CSIdentity>  
                    </PCT-QueryCompoundCS_type_identical>  
                  </PCT-QueryCompoundCS_type>  
                  <PCT-QueryCompoundCS_results>2000000</PCT-QueryCompoundCS_results>  
                </PCT-QueryCompoundCS>  
              </PCT-QueryType_css>  
            </PCT-QueryType>  
          </PCT-Query_type>  
        </PCT-Query>  
      </PCT-InputData_query>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
The final result would contain three records, being CIDs 6057, 1153, and 71098.

Scenario 2c. I have a SMILES of L-tyrosine and I would like to get back an SDF file containing the PubChem Compound records that have a similarity of 95%.

This scenario is identical to Scenario 2a, except that the initial PUG message would look like:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_query>  
        <PCT-Query>  
          <PCT-Query_type>  
            <PCT-QueryType>  
              <PCT-QueryType_css>  
                <PCT-QueryCompoundCS>  
                  <PCT-QueryCompoundCS_query>  
                    <PCT-QueryCompoundCS_query_data>  
                    C1=CC(=CC=C1C\[C@@H\](C(=O)O)N)O</PCT-QueryCompoundCS_query_data>  
                  </PCT-QueryCompoundCS_query>  
                  <PCT-QueryCompoundCS_type>  
                    <PCT-QueryCompoundCS_type_similar>  
                      <PCT-CSSimilarity>  
                        <PCT-CSSimilarity_threshold>95</PCT-CSSimilarity_threshold>  
                      </PCT-CSSimilarity>  
                    </PCT-QueryCompoundCS_type_similar>  
                  </PCT-QueryCompoundCS_type>  
                  <PCT-QueryCompoundCS_results>2000000</PCT-QueryCompoundCS_results>  
                </PCT-QueryCompoundCS>  
              </PCT-QueryType_css>  
            </PCT-QueryType>  
          </PCT-Query_type>  
        </PCT-Query>  
      </PCT-InputData_query>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
The final result would contain (currently) the SDF records for 191 CIDs.

Scenario 2d. How do I query using a molecular formula C2H7O and get back an SDF file containing the PubChem Compound records matching exactly?

This scenario is identical to Scenario 2a, except that the initial PUG message would look like:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_query>  
        <PCT-Query>  
          <PCT-Query_type>  
            <PCT-QueryType>  
              <PCT-QueryType_css>  
                <PCT-QueryCompoundCS>  
                  <PCT-QueryCompoundCS_query>  
                    <PCT-QueryCompoundCS_query_data>C2H7NO</PCT-QueryCompoundCS_query_data>  
                  </PCT-QueryCompoundCS_query>  
                  <PCT-QueryCompoundCS_type>  
                    <PCT-QueryCompoundCS_type_formula>  
                      <PCT-CSMolFormula></PCT-CSMolFormula>  
                    </PCT-QueryCompoundCS_type_formula>  
                  </PCT-QueryCompoundCS_type>  
                  <PCT-QueryCompoundCS_results>2000000</PCT-QueryCompoundCS_results>  
                </PCT-QueryCompoundCS>  
              </PCT-QueryType_css>  
            </PCT-QueryType>  
          </PCT-Query_type>  
        </PCT-Query>  
      </PCT-InputData_query>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
The final result would contain (currently) the SDF records for 20 CIDs.

Scenario 3. How do I retrieve the SDF file of all PubChem Compound records within the mass range 100.00 to 100.01 atomic mass units?

Unlike the first two scenarios, you will query Entrez (not PUG) initially to generate the list of CIDs. To perform the Entrez query, using "eSearch", use the URL:

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pccompound&usehistory=y&retmax=0&term=100:100.01[exactmass]

Please note that the "retmax=0" argument in the URL above prevents the actual result list of PubChem Compound CIDs from being returned. The "usehistory=y" creates an Entrez history item, required for the next step in this scenario. If a CID list is desired, simply omit both, e.g.:

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pccompound&term=100:100.01[exactmass]

The XML return message from eSearch, using the former URL above (rather than the latter), will look like:

<eSearchResult>  
        <Count>81</Count>  
        <RetMax>0</RetMax>  
        <RetStart>0</RetStart>  
        <QueryKey>26</QueryKey>  
        <WebEnv>  
0BPLhFE_YfmLOCUMsO7FDRuhXLxgPqzfs-aB_O2nILEnCpSEb-AIRQzeQ0LTaQNNlpK8XkxiDcX71it@46C3203C79E0BE30_0000SID  
        </WebEnv>  
        <IdList>  
        </IdList>  
        <TranslationSet>  
        </TranslationSet>  
        <TranslationStack>  
                <TermSet>  
                        <Term>0000100.000000[ExactMass]</Term>  
                        <Field>ExactMass</Field>  
                        <Count>-1</Count>  
                        <Explode>Y</Explode>  
                </TermSet>  
                <TermSet>  
                        <Term>0000100.010000[ExactMass]</Term>  
                        <Field>ExactMass</Field>  
                        <Count>-1</Count>  
                        <Explode>Y</Explode>  
                </TermSet>  
                <OP>RANGE</OP>  
        </TranslationStack>  
        <QueryTranslation>0000100.000000[ExactMass] : 0000100.010000[ExactMass]</QueryTranslation>  
</eSearchResult>
When the query is complete, the result is an Entrez query key and webenv. The query key identifies the query result and the webenv provides your session identifier. You use this Entrez query key and webenv as your source of CIDs to compose another PUG message to download the gzipped compressed SDF file of the query hits:

<PCT-Data>  
  <PCT-Data_input>  
    <PCT-InputData>  
      <PCT-InputData_download>  
        <PCT-Download>  
          <PCT-Download_uids>  
            <PCT-QueryUids>  
              <PCT-QueryUids_entrez>  
                <PCT-Entrez>  
                  <PCT-Entrez_db>pccompound</PCT-Entrez_db>  
                  <PCT-Entrez_query-key>26</PCT-Entrez_query-key>  
                  <PCT-Entrez_webenv>  
0BPLhFE_YfmLOCUMsO7FDRuhXLxgPqzfs-aB_O2nILEnCpSEb-AIRQzeQ0LTaQNNlpK8XkxiDcX71it@46C3203C79E0BE30_0000SID  
                  </PCT-Entrez_webenv>  
                </PCT-Entrez>  
              </PCT-QueryUids_entrez>  
            </PCT-QueryUids>  
          </PCT-Download_uids>  
          <PCT-Download_format value="sdf"/>  
          <PCT-Download_compression value="gzip"/>  
        </PCT-Download>  
      </PCT-InputData_download>  
    </PCT-InputData>  
  </PCT-Data_input>  
</PCT-Data>
The final result, as in the first scenario, is an URL to the results:

<PCT-Data>  
  <PCT-Data_output>  
    <PCT-OutputData>  
      <PCT-OutputData_status>  
        <PCT-Status-Message>  
          <PCT-Status-Message_status>  
            <PCT-Status value="success"/>  
          </PCT-Status-Message_status>  
        </PCT-Status-Message>  
      </PCT-OutputData_status>  
      <PCT-OutputData_output>  
        <PCT-OutputData_output_download-url>  
          <PCT-Download-URL>  
            <PCT-Download-URL_url>  
            ftp://ftp-private.ncbi.nlm.nih.gov/pubchem/.fetch/816930703564580480.sdf.gz  
            </PCT-Download-URL_url>  
          </PCT-Download-URL>  
        </PCT-OutputData_output_download-url>  
      </PCT-OutputData_output>  
    </PCT-OutputData>  
  </PCT-Data_output>  
</PCT-Data>
In this example, 81 hits are (currently) returned.

Scenario 4. How do I get back the PubMed abstracts for PubChem Compound CID 2244 (aspirin)?

Similar to Scenario 3, you will query Entrez (not PUG) to get a list of PubMed abstracts linked to a PubChem Compound. To perform the Entrez query, using "eLink", for use the URL:

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pccompound&id=2244&db=pubmed

Given that a list of abstracts may be long, it is a good idea to create an Entrez history item, e.g., using the URL:

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pccompound&id=2244&db=pubmed&cmd=neighbor_history

The XML return message from eLink, using the latter URL above (rather than the former), will look like:

<eLinkResult>  
<LinkSet>  
   <DbFrom>pccompound</DbFrom>  
   <IdList>  
    <Id>2244</Id>  
   </IdList>  
   <LinkSetDbHistory>  
    <DbTo>pubmed</DbTo>  
    <LinkName>pccompound_pubmed</LinkName>  
    <QueryKey>5</QueryKey>  
   </LinkSetDbHistory>  
   <LinkSetDbHistory>  
    <DbTo>pubmed</DbTo>  
    <LinkName>pccompound_pubmed_mesh</LinkName>  
    <QueryKey>6</QueryKey>  
   </LinkSetDbHistory>  
    <WebEnv>  
0FFDpPFhSw2nzieR6fvaLMqXLnx9GKbcev9IJqI3EXp8pEzTEj38McL0EHmseTEpHXZkgacEGym2qtB@264F60B37ADDEBF0_0143SID  
    </WebEnv>  
   </LinkSet>  
  </eLinkResult>
In the message above, two Entrez history items were created, one corresponding to the depositor provided links (pccompound_pubmed) and those derived through linkage of MeSH ontology with depositor provided synonyms (pccompound_pubmed_mesh). To retrieve the abstracts, one may provide PubMed ids, one at a time or all at once, using "eFetch".

To retrieve a single abstract, e.g., for PubMed id 12767473, one would formulate an URL like:

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=12767473&retmode=xml&rettype=abstract

To retrieve abstracts for a list of PubMed ids contained in an Entrez history, e.g., for the eLink query above:
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&webenv=0FFDpPFhSw2nzieR6fvaLMqXLnx9GKbcev9IJqI3EXp8pEzTEj38McL0EHmseTEpHXZkgacEGym2qtB@264F60B37ADDEBF0_0143SID&query_key=5&retmode=xml&rettype=abstract

The output of the above URLs is omitted for brevity.

ON THIS PAGE
Introduction
Interacting with PUG
PUG Tasks
Download Tasks
Query Tasks
Chemical Structure Query
PubChem BioAssay Description
Standardization
PUG, NCBI eUtils, and Entrez History
PUG and SOAP
FAQs
PubChem on X
PubChem on Facebook


Auto-Complete Search Service
The PubChem REST auto-complete API service supports fuzzy matching of input strings against a number of query dictionaries.

503 HTTP STATUS CODE: Please note that this status code may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

Query URL Format
https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/<dictionary>/<search_term>/<output_format>?<options>

Available Dictionaries
Compound
Assay
Gene
Taxonomy
Output Format
jsonp
json
Options
limit (default: 10)
Maximum number of returned results

Example Queries
https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/compound/aspirin/jsonp?limit=6

callback({
    "status": {
        "code": 0
    },
    "total": 6,
    "dictionary_terms": {
        "compound": [
            "aspirin",
            "Aspirine",
            "Aspirin sodium",
            "Aspirin anhydride",
            "Aspirin methyl ester",
            "Aspirin calcium"
        ]
    }
})
https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/assay/p68/json?limit=8

{
    "status": {
        "code": 0
    },
    "total": 8,
    "dictionary_terms": {
        "assay": [
            "p68 - Protein Target",
            "p68-PAK - Protein Target",
            "p68 kinase - Protein Target",
            "Inhibition of HIV2 reverse transcriptase p68/p54 expressed in Escherichia coli - Assay Name",
            "Inhibition of HIV2 reverse transcriptase p68/p54 expressed in Escherichia coli at 495 uM - Assay Name",
            "RPL21P68 - Gene Target",
            "gp68 - Protein Target",
            "CEP68 - Gene Target"
        ]
    }
}
https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/gene/egfr/jsonp?limit=5

callback({
    "status": {
        "code": 0
    },
    "total": 5,
    "dictionary_terms": {
        "gene": [
            "EGFR",
            "NGFR",
            "OGFR",
            "DHFR",
            "EGR1"
        ]
    }
})
https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/taxonomy/mouse/json?limit=5

{
    "status": {
        "code": 0
    },
    "total": 5,
    "dictionary_terms": {
        "taxonomy": [
            "mouse",
            "mousepox",
            "mousepox virus",
            "mouse-ear cress",
            "Mouse adenovirus"
        ]
    }
}
How It Works
We keep dictionaries of terms for compounds, genes, taxons (organisms), and assays. The auto-complete search service searches through these dictionary terms to find the best matches. When the user submits an auto-complete search request with a query (which should be at least three-character long), it launches two search threads in parallel:

Auto-complete, which finds the terms containing the query string.
Spell-suggest, which finds close matches (e.g., the terms similar to the query string).
The spell-suggest thread performs trigram searches to find the closest matches. For example, when “motrn” (a misspelling of “motrin”) is given as a query, this thread looks up terms matching as many trigram pieces as possible (i.e., --m, -mo, mot, otr, trn, rn-, n-- ), which finds "motrin" as the closest match.

To speed up the process, the searches are not exhaustive (that is, not thorough) and only a portion of the dictionary is searched for most queries. Each of the auto-complete and spell-suggest threads searches for up to 1,000 hits. When the search finds 1,000 hits, it stops even if not all part of the dictionary is searched.

The hits from each thread are rank-ordered according to internal scoring schemes. The limit parameter (L), which is set to 10 by default, controls the number of hits returned to the user. Note that the difference between L and the number of hits (AC) from the auto-complete thread determines the context of the returned hit list.

If the auto-complete thread finds the same number of terms or more, compared to the limit parameter (that is, AC >= L), the returned term list contains the L highest-ranked hits from the auto-complete threads.
If the auto-complete thread finds fewer terms than the limit parameter (that is, AC < L), the returned term list has all hits from the auto-complete thread and the (L - AC) highest-ranked hits from the spell-suggest thread. For example, when the user requests 10 terms (L = 10) and the auto-complete thread finds only 4 terms (AC = 4), then the top 6 (= 10 - 4) hits from the spell-suggest thread are appended to make up the requested total 10 hits.



Dynamic Request Throttling
To help maximize uptime and request handling speed, PubChem web servers employ a dynamic, web-request throttling approach that enforces Usage Policies.  Importantly, during periods of excessive demand, these policies may be dynamically changed to maintain accessibility to all users.  Requests exceeding limits are rejected (HTTP 503 error).  If the user continuously exceeds the limit, they will be blocked for a period of time. An HTTP 503 STATUS CODE may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

Therefore, the user should moderate the speed at which requests are sent to PubChem, according to the traffic status of PubChem and the extent to which the user is approaching limits.  This information is provided in specialized HTTP response headers accompanying all PUG-REST web requests.  For example, the HTTP response header contains a line similar to the following:

X-Throttling-Control: Request Count status: Green (0%), Request Time status: Green (0%), Service status: Green (20%)

The first two status indicators (Request Count and Time statuses) give information on your usage of the service in one of four states:

Green - less than 50% of the permitted request limit has been used
Yellow - between 50% and 75% of the request limit has been used
Red - more than 75% of the request limit has been reached
Black - the limit has been exceeded and requests are being blocked
The third indicator (Service status) shows the concurrent usage of the service in one of four states:

Idle (Green) - Low concurrent usage being applied to the service at present
Moderate (Yellow) - a moderate number of concurrent requests are being handled
Busy (Red) - a significant number of concurrent requests are being handled
Overloaded (Black) - an excessively high number of concurrent requests are being handled
It is important to note that there are many instances of PubChem services running in parallel. Each instance receives traffic from a load balancer, which distributes the requests across the system. Thus, when a stream of requests is sent to PubChem, the responses will be relative to the PubChem server instance handling the request. Because of the load balancing, one server instance can become overloaded while others may not, depending on the overall nature of requests sent to that server. When providing many requests, one should moderate the speed requests are sent to according to the worst-case usage feedback received.  This will prevent uneven rejection of requests by PubChem services.

NOTE: PubChem has many ways to download large volumes of information that are more efficient than multiple requests e.g. to PUG REST. There are various download services, and datafiles on the FTP site. See the download help page for more information.

