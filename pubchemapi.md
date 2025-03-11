Programmatic Access
USAGE POLICY: Please note that PubChem web services run on servers shared by all PubChem users. We ask that any script or application not make more than 5 requests per second, in order to avoid overloading these servers. For more detail on request volume limitations, including automated rate limiting (throttling), please read this document. If you have a large data set that you need to compute with, please contact us for help on optimizing your task, as there are likely more efficient ways to approach such large queries. See also the help page for bulk data downloads.

503 HTTP STATUS CODE: Please note that this status code may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

PubChem provides many types of programmatic access to its data, including:

PUG-REST
PUG-REST, a Representational State Transfer (REST)-style web service that supplies specific bits of information on one or more PubChem records, and is a good place to start for most users. PUG-REST is a simplified access route to PubChem without the overhead of XML or SOAP envelopes that are required with PUG and PUG-SOAP. PUG-REST provides convenient access to information on PubChem records not possible with the other PUG services. It is intended to handle short requests with simple inputs and outputs, and is synchronous - meaning the result is given in a single call that may last at most 30s (the default timeout on PubChem servers), without any intermediate step to poll whether that request has completed.

PUG-View
PUG-View is a REST-style web service that provides full reports, including third-party textual annotation, for individual PubChem records. Its purpose is primarily to drive the PubChem summary web pages, but can also be used independently as a programmatic web service. PUG View provides complex, structured data reports (compared to PUG REST which has simpler outputs).

Power User Gateway (PUG)
PUG provides programmatic access to PubChem services via a single common gateway interface (CGI), called ‘pug.cgi’, available at http://pubchem.ncbi.nlm.nih.gov/pug/pug.cgi. This CGI is a central gateway to several PubChem services. Instead of taking any Uniform Resource Locator (URL) arguments, PUG exchanges data through XML via a Hypertext Transfer Protocol (HTTP) POST.

PUG-SOAP
PUG-SOAP provides a web service access to PubChem data, using the simple object access protocol (SOAP). It provides an easier programmatic access to much of the same functionality as PUG, but it breaks down operations into simpler functions as defined via the web service definition language (WSDL), and uses SOAP-formatted message envelopes for information exchange. This WSDL/SOAP layer is most suitable for SOAP-aware GUI workflow applications (e.g. Taverna and Pipeline Pilot) and programming/scripting languages (e.g. C, C++, C#, .NET, Perl, Python and Java).

PubChemRDF REST interface
This is a REST-style interface designed to access RDF-encoded PubChem data. See PubChemRDF for more details.

Entrez Utilities (also called E-Utilities or E-Utils)
E-Utils are a set of programs used to access to information contained in the Entrez system. While suited for accessing text or numeric-fielded data, they cannot deal with more complex types of data specific to PubChem, such as chemical structures and tabular bioactivity data.

Also note that PubChem has a standard time limit of 30 seconds per web service request. If a request is not completed within the 30-second limit for any reason, a timeout error will be returned. To work around certain slower operations, some services off an ‘asynchronous’ approach, where a so-called ‘key’ is returned as a response to the initial request. This key is then used to check periodically whether the operation has finished, and, when complete, retrieve the results.


PUG REST
This document describes the REST-style version of PUG (Power User Gateway), a web interface for accessing PubChem data and services. It details both the syntax of the HTTP requests, and the available functions. This is more of a specification document; a less formal, tutorial-style PUG REST document is now available. For comments, help, or to suggest new functionality, please contact pubchem-help@ncbi.nlm.nih.gov.

Additional information of PUG REST can also be found in the following papers:

Kim S, Thiessen PA, Cheng T, Yu B, Bolton EE. An update on PUG-REST: RESTful interface for programmatic access to PubChem. Nucleic Acids Res. 2018 July 2; 46(W1):W563-570. doi:10.1093/nar/gky294.
[PubMed PMID: 29718389] [PubMed Central ID: PMC6030920] [Free Full Text]
Kim S, Thiessen PA, Bolton EE, Bryant SH. PUG-SOAP and PUG-REST: web services for programmatic access to chemical information in PubChem. Nucleic Acids Res. 2015 Jul 1; 43(W1):W605-W611. doi: 10.1093/nar/gkv396.
[PubMed PMID: 25934803] [PubMed Central PMCID: PMC4489244] [Free Full Text]
Kim S, Thiessen PA, Bolton EE. Programmatic Retrieval of Small Molecule Information from PubChem Using PUG-REST. In Kutchukian PS, ed. Chemical Biology Informatics and Modeling. Methods in Pharmacology and Toxicology. New York, NY: Humana Press, 2018, pp. 1-24. doi:10.1007/7653_2018_30.
[Full Text]
USAGE POLICY: Please note that PUG REST is not designed for very large volumes (millions) of requests. We ask that any script or application not make more than 5 requests per second, in order to avoid overloading the PubChem servers. To check additional request volume limitations, please read this document. If you have a large data set that you need to compute with, please contact us for help on optimizing your task, as there are likely more efficient ways to approach such bulk queries.

503 HTTP STATUS CODE: Please note that this status code may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

Example Perl scripts demonstrating how to access PubChem data through PUG-REST are available here.

URL-based API
The URL Path
Most – if not all – of the information the service needs to produce its results is encoded into the URL. The general form of the URL has three parts – input, operation, and output – after the common prefix, followed by operation options as URL arguments (after the ‘?’):

https://pubchem.ncbi.nlm.nih.gov/rest/pug/<input specification>/<operation specification>/[<output specification>][?<operation_options>]

Input
The input portion of the URL tells the service which records to use as the subject of the query. This is further subdivided into two or more locations in the URL “path” as follows:

<input specification> = <domain>/<namespace>/<identifiers>

<domain> = substance | compound | assay | gene | protein | pathway | taxonomy | cell | <other inputs>

compound domain <namespace> = cid | name | smiles | inchi | sdf | inchikey | formula | <structure search> | <xref> | <mass> | listkey | <fast search>

<structure search> = { substructure | superstructure | similarity | identity } / { smiles | inchi | sdf | cid}

<fast search> = { fastidentity | fastsimilarity_2d | fastsimilarity_3d | fastsubstructure | fastsuperstructure } / { smiles | smarts | inchi | sdf | cid } | fastformula

<xref> = xref / { RegistryID | RN | PubMedID | MMDBID | ProteinGI | NucleotideGI | TaxonomyID | MIMID | GeneID | ProbeID | PatentID }

<mass> = { molecular_weight | exact_mass | monoisotopic_mass } / { equals | range } / value_1 { / value 2 }

substance domain <namespace> = sid | sourceid/<source id> | sourceall/<source name> | name | <xref> | listkey

<source name> = any valid PubChem depositor name

assay domain <namespace> = aid | listkey | type/<assay type> | sourceall/<source name> | target/<assay target> | activity/<activity column name>

<assay type> = all | confirmatory | doseresponse | onhold | panel | rnai | screening | summary | cellbased | biochemical | invivo | invitro | activeconcentrationspecified

<assay target> = gi | proteinname | geneid | genesymbol | accession

gene domain <namespace> = geneid | genesymbol | synonym

protein domain <namespace> = accession | gi | synonym

pathway domain <namespace> = pwacc

taxonomy domain <namespace> = taxid | synonym

cell domain <namespace> = cellacc | synonym

<other inputs> = sources / [substance, assay] | sourcetable | conformers | annotations/[sourcename/<source name> | heading/<heading>] | classification | standardize | periodictable

<identifiers> = comma-separated list of positive integers (e.g. cid, sid, aid) or identifier strings (source, inchikey, formula); in some cases only a single identifier string (name, smiles, xref; inchi, sdf by POST only)

For example, to access CID 2244 (aspirin), one would construct the first part of the URL this way:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/<operation specification>/[<output specification>]

Some source names contain the ‘/’ (forward slash) character, which is incompatible with the URL syntax; for these, replace the ‘/’ with a ‘.’ (period) in the URL. Other special characters may need to be escaped, such as ‘&’ should be replaced by ‘%26’. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/<operation specification>/[<output specification>]

Operation
The operation part of the URL tells the service what to do with the input records – such as to retrieve whole record data blobs or specific properties of a compound, etc. The construction of this part of the “path” will depend on what the operation is. Currently, if no operation is specified at all, the default is to retrieve the entire record. What operations are available are, of course, dependent on the input domain – that is, certain operations are applicable only to compounds and not assays, for example.

compound domain <operation specification> = record | <compound property> | synonyms | sids | cids | aids | assaysummary | classification | <xrefs> | description | conformers

<compound property> = property / [comma-separated list of property tags]

substance domain <operation specification> = record | synonyms | sids | cids | aids | assaysummary | classification | <xrefs> | description

<xrefs> = xrefs / [comma-separated list of xrefs tags]

assay domain <operation specification> = record | concise | aids | sids | cids | description | targets/<target type> | <doseresponse> | summary | classification

<target_type> = {ProteinGI, ProteinName, GeneID, GeneSymbol}

<doseresponse> = doseresponse/sid

gene domain <operation specification> = summary | aids | concise | pwaccs

protein domain <operation specification> = summary | aids | concise | pwaccs

pathway domain <operation specification> = summary | cids | geneids | accessions

taxonomy domain <operation specification> = summary | aids

cell domain <operation specification> = summary | aids

For example, to access the molecular formula and InChI key for CID 2244, one would use a URL like:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularFormula,InChIKey/[<output specification>]

Output
The final portion of the URL tells the service what output format is desired. Note that this is formally optional, as output format can also be specified in the HTTP Accept field of the request header – see below for more detail.

<output specification> = XML | ASNT | ASNB | JSON | JSONP [ ?callback=<callback name> ] | SDF | CSV | PNG | TXT

ASNT is NCBI’s text (human-readable) variant of ASN.1; ASNB is standard binary ASN.1 and is currently returned as Base64-encoded ascii text. Note that not all formats are applicable to the results of all operations; one cannot, for example, retrieve a whole compound record as CSV or a property table as SDF. TXT output is only available in a restricted set of cases where all the information is the same – for example, synonyms for a single CID where there is one synonym per line.

For example, to access the molecular formula for CID 2244 in JSON format, one would use the (now complete) URL:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularFormula/JSON

JSONP takes an optional callback function name (which defaults to “callback” if not specified). For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularFormula/JSONP?callback=my_callback

HTTP Interface Details
Request Header
The HTTP request header may be used to supply some types of information to this service.

The value of “Accept” may be a MIME type that will tell the service what output format is accepted by the client, and hence what format is returned by the server. The allowed values are:

Accept value	Output Format
application/xml	XML
application/json	JSON
application/javascript	JSONP
application/ber-encoded	ASNB
chemical/x-mdl-sdfile	SDF
text/csv	CSV
image/png	PNG
text/plain	TXT
The Content-Type in the HTTP response header will also be set by the reverse of the above table, e.g. XML data will have “Content-Type: application/xml”.

For example, the URL:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244

with “Accept: chemical/x-mdl-sdfile” in the request header will return CID 2244 in SDF format.

For proper transmission of certain special characters, strings passed e.g. for SMILES input may need to be URL encoded; for example, “smiles=C1C[CH+]1” should be encoded as “smiles=C1C%5BCH%2B%5D1”. For correct parsing of any POST body, the proper content type header must be included in the request header (see below).

Request (POST) Body
Some parts of the URL may be moved to the body of a POST request, rather than being part of the URL path. For example, a list of CID integers – which may be too long to fit within the size limitations of a GET request URL – may be moved to the POST body:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/property/MolecularFormula,MolecularWeight/CSV

with “cid=1,2,3,4,5” in the POST body, would retrieve a CSV-formatted table of results for these CIDs. Note that for the service to parse such POST information correctly, the “Content-Type: application/x-www-form-urlencoded” value must be included in the request header. One may also use “Content-Type: multipart/form-data” with the POST body formatted accordingly. See here for more information on content type encoding.

Status Codes
If the operation was successful, the HTTP status code will be 200 (OK). If the server encounters an error, it will return an HTTP status code that gives some indication of what went wrong; possibly along with, depending on the output format (such as in a tag in XML), some additional more human-readable detail message(s). The codes in the 400-range are errors on the client side, and those in the 500 range indicate a problem on the server side; the codes currently in use are:

HTTP Status	Error Code	General Error Category
200	(none)	Success
202	(none)	Accepted (asynchronous operation pending)
400	PUGREST.BadRequest	Request is improperly formed (syntax error in the URL, POST body, etc.)
404	PUGREST.NotFound	The input record was not found (e.g. invalid CID)
405	PUGREST.NotAllowed	Request not allowed (such as invalid MIME type in the HTTP Accept header)
500	PUGREST.Unknown	An unknown error occurred
500	PUGREST.ServerError	Some problem on the server side (such as a database server down, etc.)
501	PUGREST.Unimplemented	The requested operation has not (yet) been implemented by the server
503	PUGREST.ServerBusy	Too many requests or server is busy, retry later
504	PUGREST.Timeout	The request timed out, from server overload or too broad a request
HTTPS
NCBI now requires HTTPS (URLs beginning with https://) for web service access.

Schemas
A schema for the XML data returned by PUG REST may be found at:

https://pubchem.ncbi.nlm.nih.gov/pug_rest/pug_rest.xsd

Some operations (such as full record retrieval) may use the standard PubChem schema at:

https://ftp.ncbi.nlm.nih.gov/pubchem/specifications/pubchem.xsd

Classification data is returned with this schema:

https://pubchem.ncbi.nlm.nih.gov/pug_rest/hierarchy_data.xsd

Operations
Full-record Retrieval
Returns full records for PubChem substances, compounds, and assays.

Valid output formats for substances and compounds are XML, JSON(P), ASNT/B, SDF, and PNG. A compound record may optionally be either 2D or 3D; substances are always given with coordinates as deposited. For PNG output, only the first SID or CID is used if the input is a list.

Option	Allowed Values (default in bold)	Meaning
record_type	2d, 3d	Type of conformer for compounds
image_size	large, small, <width>x<height>	Image size: large (300x300), small (100x100), or arbitrary (e.g. 320x240)
Valid output formats for assays are XML, JSON(P), ASNT/B, and CSV. Assay record retrieval is limited to a single AID with 10000 SIDs at a time; a subset of the SIDs of an assay may be specified as options:

Option	Allowed Values	Meaning
sid	listkey, or comma-separated integers	SID rows to retrieve for an assay
listkey	valid SID listkey	listkey containing SIDs, if using sid=listkey
Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/IBM/5F1CA2B314D35F28C7F94168627B29E3/ASNT

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/SDF

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/DTP.NCI/747285/PNG

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/SDF

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/PNG

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/SDF?record_type=3d

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/PNG?record_type=3d&image_size=small

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/SDF

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/BPGDAMSIGCZZLK-UHFFFAOYSA-N/SDF

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/ASNT?version=1.1 (for old-version)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/CSV?sid=26736081,26736082,26736083

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/concise/CSV

Compound Property Tables
Returns a table of compound properties. More than one property may be requested, in a comma-separated list of property tags in the request URL. Valid output formats for the property table are: XML, ASNT/B, JSON(P), CSV, and TXT (limited to a single property). Available properties are:

Property	Notes
MolecularFormula	Molecular formula.
MolecularWeight	The molecular weight is the sum of all atomic weights of the constituent atoms in a compound, measured in g/mol. In the absence of explicit isotope labelling, averaged natural abundance is assumed. If an atom bears an explicit isotope label, 100% isotopic purity is assumed at this location.
SMILES	A SMILES (Simplified Molecular Input Line Entry System) string, which includes both stereochemical and isotopic information. See the glossary entry on SMILES for more detail.
CanonicalSMILES (DEPRECATED)	Canonical SMILES (Simplified Molecular Input Line Entry System) string. It is a unique SMILES string of a compound, generated by a “canonicalization” algorithm.
IsomericSMILES (DEPRECATED)	Isomeric SMILES string. It is a SMILES string with stereochemical and isotopic specifications.
InChI	Standard IUPAC International Chemical Identifier (InChI). It does not allow for user selectable options in dealing with the stereochemistry and tautomer layers of the InChI string.
InChIKey	Hashed version of the full standard InChI, consisting of 27 characters.
IUPACName	Chemical name systematically determined according to the IUPAC nomenclatures.
Title	The title used for the compound summary page.
XLogP	Computationally generated octanol-water partition coefficient or distribution coefficient. XLogP is used as a measure of hydrophilicity or hydrophobicity of a molecule.
ExactMass	The mass of the most likely isotopic composition for a single molecule, corresponding to the most intense ion/molecule peak in a mass spectrum.
MonoisotopicMass	The mass of a molecule, calculated using the mass of the most abundant isotope of each element.
TPSA	Topological polar surface area, computed by the algorithm described in the paper by Ertl et al.
Complexity	The molecular complexity rating of a compound, computed using the Bertz/Hendrickson/Ihlenfeldt formula.
Charge	The total (or net) charge of a molecule.
HBondDonorCount	Number of hydrogen-bond donors in the structure.
HBondAcceptorCount	Number of hydrogen-bond acceptors in the structure.
RotatableBondCount	Number of rotatable bonds.
HeavyAtomCount	Number of non-hydrogen atoms.
IsotopeAtomCount	Number of atoms with enriched isotope(s)
AtomStereoCount	Total number of atoms with tetrahedral (sp3) stereo [e.g., (R)- or (S)-configuration]
DefinedAtomStereoCount	Number of atoms with defined tetrahedral (sp3) stereo.
UndefinedAtomStereoCount	Number of atoms with undefined tetrahedral (sp3) stereo.
BondStereoCount	Total number of bonds with planar (sp2) stereo [e.g., (E)- or (Z)-configuration].
DefinedBondStereoCount	Number of atoms with defined planar (sp2) stereo.
UndefinedBondStereoCount	Number of atoms with undefined planar (sp2) stereo.
CovalentUnitCount	Number of covalently bound units.
PatentCount	Number of patent documents linked to this compound.
PatentFamilyCount	Number of unique patent families linked to this compound (e.g. patent documents grouped by family).
LiteratureCount	Number of articles linked to this compound (by PubChem's consolidated literature analysis).
Volume3D	Analytic volume of the first diverse conformer (default conformer) for a compound.
XStericQuadrupole3D	The x component of the quadrupole moment (Qx) of the first diverse conformer (default conformer) for a compound.
YStericQuadrupole3D	The y component of the quadrupole moment (Qy) of the first diverse conformer (default conformer) for a compound.
ZStericQuadrupole3D	The z component of the quadrupole moment (Qz) of the first diverse conformer (default conformer) for a compound.
FeatureCount3D	Total number of 3D features (the sum of FeatureAcceptorCount3D, FeatureDonorCount3D, FeatureAnionCount3D, FeatureCationCount3D, FeatureRingCount3D and FeatureHydrophobeCount3D)
FeatureAcceptorCount3D	Number of hydrogen-bond acceptors of a conformer.
FeatureDonorCount3D	Number of hydrogen-bond donors of a conformer.
FeatureAnionCount3D	Number of anionic centers (at pH 7) of a conformer.
FeatureCationCount3D	Number of cationic centers (at pH 7) of a conformer.
FeatureRingCount3D	Number of rings of a conformer.
FeatureHydrophobeCount3D	Number of hydrophobes of a conformer.
ConformerModelRMSD3D	Conformer sampling RMSD in Å.
EffectiveRotorCount3D	Total number of 3D features (the sum of FeatureAcceptorCount3D, FeatureDonorCount3D, FeatureAnionCount3D, FeatureCationCount3D, FeatureRingCount3D and FeatureHydrophobeCount3D)
ConformerCount3D	The number of conformers in the conformer model for a compound.
Fingerprint2D	Base64-encoded PubChem Substructure Fingerprint of a molecule.
Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/1,2,3,4,5/property/MolecularFormula,MolecularWeight,InChIKey/CSV

Synonyms
Returns a list of substance or compound synonyms. Valid output formats for synonyms are XML, JSON(P), ASNT/B, and TXT (limited).

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/synonyms/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CCCC/synonyms/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/53789435/synonyms/TXT

Description
Returns the title and description for an S/CID, the same as used in the web summary pages for these records. Valid output formats are XML, JSON(P) , and ASNT/B.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/1983/description/XML

SIDS / CIDS / AIDS
Returns a list of SIDs, CIDs, or AIDs. Possibly interconverts record identifiers, with options in the table below; these options, if present, must be specified as standard URL arguments (e.g. after the ‘?’). The list of identifiers may be grouped by input (e.g. when converting from one type to another); flattened to a unique target set (implied for TXT output); or stored on the server (which also implies flat), in which case a list key is returned. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

Option	Allowed Values (default in bold)	Meaning
aids_type	all, active, inactive	Type of AIDs to return, given SIDs or CIDs
sids_type	all, active, inactive, doseresponse	Type of SIDs to return, given AIDs
sids_type	all, standardized, component	Type of SIDs to return, given CIDs
sids_type	original	Type of SIDs to return, given SIDs
cids_type	all, active, inactive	Type of CIDs to return, given AIDs
cids_type	all, standardized, component	Type of CIDs to return, given SIDs
cids_type	original, parent, component, preferred, same_stereo, same_isotopes, same_connectivity, same_tautomer, same_parent, same_parent_stereo, same_parent_isotopes, same_parent_connectivity, same_parent_tautomer	Type of CIDs to return, given CIDs
list_return	grouped, flat, listkey	Type of identifier list to return
sourcename	(any substance source)	For SIDs by name only, restrict to source
hold_type	live_only, live_and_on_hold, on_hold_only	For SIDs or AIDs by sourceall, whether to include on-hold
Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/glucose/sids/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/glucose/sids/XML?list_return=listkey

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/aspirin/sids/JSON?sourcename=ChemIDplus

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/aspirin/sids/JSON?sourcename=ChemIDplus&name_type=word

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/listkey/xxxxxx/sids/XML (where ‘xxxxxx’ is the listkey from the above URL)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/glucose/cids/XML?list_return=grouped

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/glucose/cids/XML?list_return=flat

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceall/MLSMR/sids/JSON?list_return=listkey

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceall/R%26D%20Chemicals/sids/XML?list_return=listkey

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/123061,123079/cids/XML?cids_type=all

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/sids/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchi/cids/JSON (where the POST body contains “inchi=InChI=1S/C3H8/c1-3-2/h3H2,1-2H3”)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/192180/cids/TXT?cids_type=component

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/aids/JSON?aids_type=active

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/sids/JSON?sids_type=component

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/cids/TXT?cids_type=same_connectivity

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/21145249/cids/XML?cids_type=parent

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/sids/XML?sids_type=inactive

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/sids/JSON?sids_type=doseresponse

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/type/doseresponse/aids/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/sourceall/DTP.NCI/aids/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/xref/PatentID/EP0711162A1/sids/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/cids/XML?name_type=word

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/cids/XML?name_type=complete

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/genesymbol/USP2/aids/TXT

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/gi/116516899/aids/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/activity/EC50/aids/TXT (where EC50 is case-sensitive)

Assay Description
Returns assay descriptions. Valid output formats are XML, JSON(P), and ASNT/B.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/450/description/XML

Assay Targets
Return assay target information. Valid output formats are XML, JSON(P), ASNT/B, and TXT. Available target types are:

Target Type	Notes
ProteinGI	NCBI GI of a protein sequence
ProteinName	protein name
GeneID	NCBI Gene database identifier
GeneSymbol	gene symbol
Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/490,1000/targets/ProteinGI,ProteinName,GeneID,GeneSymbol/XML

Assay Summary
Returns a summary of biological test results for the given SID(s) or CID(s), including assay experiment information, bioactivity, and target. Valid output formats are XML, JSON(P), ASNT/B, and CSV.

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/1000,1001/assaysummary/CSV

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/104234342/assaysummary/XML

There is also a per-AID assay summary available in a simplified format. Valid output formats are XML, JSON(P), and ASNT/B.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/summary/XML

Assay Dose-Response
Returns assay dose-response data for a single AID with up to 1000 SID(s). Valid output formats are XML, JSON(P), ASNT/B, and CSV. A subset of the SIDs of an assay may be specified as options:

Option	Allowed Values	Meaning
sid	listkey, or comma-separated integers	SID rows to retrieve for an assay
listkey	valid SID listkey	listkey containing SIDs, if using sid=listkey
Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/doseresponse/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/doseresponse/CSV?sid=104169547,109967232

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/doseresponse/XML (with “aid=504526&sid=104169547,109967232” in the POST body)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/602332/sids/XML?sids_type=doseresponse&list_return=listkey

followed by

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/602332/doseresponse/CSV?sid=listkey&listkey=xxxxxx&listkey_count=100 (where ‘xxxxxx’ is the listkey returned by the previous URL)

Gene Summary
Returns a summary of gene: GeneID, Symbol, Name, TaxonomyID, Taxonomy, Description, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B.

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/1956,13649/summary/JSON (by GeneID)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/summary/XML (by genesymbol, case-insensitive and default to human)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/10090/summary/JSON (mouse with NCBI TaxonomyID 9606)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/Rattus%20norvegicus/summary/JSON (mouse with scientific taxonomy name)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/Norway%20rat/summary/JSON (mouse with common taxonomy name)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/EGFR/summary/JSON (by synonym, note that one synonym may map to multiple GeneIDs)

Please check PUG REST Tutorial for a complete list of available data and more examples.

Protein Summary
Returns a summary of protein: ProteinAccession, Name, TaxonomyID, Taxonomy, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B.

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P00533,P01422/summary/JSON

Please check PUG REST Tutorial for a complete list of available data and more examples.

Pathway Summary
Returns a summary of pathway: PathwayAccession, SourceName, SourceID, SourceURL, Name, Type, Category, Description, TaxonomyID, and Taxonomy. Valid output formats are XML, JSON(P), and ASNT/B.

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983/summary/JSON

Please check PUG REST Tutorial for a complete list of available data and more examples.

Taxonomy Summary
Returns a summary of taxonomy: TaxonomyID, ScientificName, CommonName, Rank, RankedLineage, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B.

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/taxid/9606,10090,10116/summary/JSON

Please check PUG REST Tutorial for a complete list of available data and more examples.

Cell Line Summary
Returns a summary of taxonomy: CellAccession, Name, Sex, Category, SourceTissue, SourceTaxonomyID, SourceOrganism, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B.

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/cellacc/CVCL_0030,CVCL_0045/summary/JSON (by Cellosaurus cell line accession)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/HeLa/summary/JSON (by synonym)

Please check PUG REST Tutorial for a complete list of available data and more examples.

Classification
Returns the nodes in the classification tree for a single SID, CID, or AID. Valid output formats are XML, JSON(P), and ASNT/B.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/1917/classification/XML

Dates
Returns dates associated with PubChem identifiers; note that not all date types are relevant to all identifier types – see the table below. Multiple date types may be requested. Valid output formats are XML, JSON(P), and ASNT/B. Options are:

Option	Allowed Values (default in bold)	Meaning
dates_type	deposition	when an SID or AID first appeared
modification	when an SID or AID was last modified	
hold	when an SID or AID will be released	
creation	when a CID first appeared	
Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/dates/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/1,2,3,135653256/dates/XML?dates_type=modification,deposition,hold

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1,624113/dates/XML?dates_type=deposition,hold

XRefs
Returns cross-references associated with PubChem SIDs or CIDs. Multiple types may be requested in a comma-separated list in the URL path. Valid output formats are XML, JSON(P), ASNT/B, and TXT (limited to a single type). Available cross-references are:

Cross-reference	Meaning
RegistryID	external registry identifier
RN	registry number
PubMedID	NCBI PubMed identifier
MMDBID	NCBI MMDB identifier
DBURL	external database home page URL
SBURL	external database substance URL
ProteinGI	NCBI protein GI
NucleotideGI	NCBI nucleotide GI
TaxonomyID	NCBI taxonomy identifier
MIMID	NCBI MIM identifier
GeneID	NCBI gene identifier
ProbeID	NCBI probe identifier
PatentID	patent identifier
SourceName	external depositor name
SourceCategory	depositor category(ies)
Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/127378063/xrefs/PatentID/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/vioxx/xrefs/RegistryID,RN,PubMedID/JSONP

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceall/ChEBI/xrefs/RegistryID/JSON

Conformers
A list of diverse order conformer IDs can be obtained from CID. Valid output formats are XML, JSON(P), ASNT/B, and TXT (limited to a single CID):

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/conformers/XML

Individual conformer records – either computed 3D coordinates for compounds or deposited/experimental 3D coordinates for some substances – can be retrieved by conformer ID:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/conformers/000008C400000001/SDF

Structure Search Operations
Substructure / Superstructure
This is a special type of compound namespace input that retrieves CIDs by substructure or superstructure search. It requires a CID, or a SMILES, InChI, or SDF string in the URL path or POST body (InChI and SDF by POST only). Valid output formats are XML, JSON(P), and ASNT/B.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/smiles/C3=NC1=C(C=NC2=C1C=NC=C2)[N]3/cids/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/inchi/cids/XML (where the POST body contains “inchi=InChI=1S/C9H6N4/c1-2-10-3-6-7(1)11-4-8-9(6)13-5-12-8/h1-5H,(H,12,13)”)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsuperstructure/cid/2244/cids/XML

Structure search options are specified via URL arguments:

Option	Type	Meaning	Default
MatchIsotopes	boolean	atoms must be of the specified isotope	false
MatchCharges	boolean	atoms must match the specified charge	false
MatchTautomers	boolean	allow match to tautomers of the given structure (no longer supported)	false
RingsNotEmbedded	boolean	rings may not be embedded in a larger system	false
SingleDoubleBondsMatch	boolean	single or double bonds match aromatic bonds	true
ChainsMatchRings	boolean	chain bonds in the query may match rings in hits	true
StripHydrogen	boolean	remove any explicit hydrogens before searching	false
Stereo	enum	how to handle stereo; one of ignore, exact, relative, nonconflicting	ignore
MaxSeconds	integer	maximum search time in seconds	unlimited
MaxRecords	integer	maximum number of hits	2M
listkey	string	restrict to matches within hits from a prior search	none
Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/smiles/C1=NC2=C(N1)C(=O)N=C(N2)N/cids/XML?MatchIsotopes=true&MaxRecords=100

Similarity
This is a special type of compound namespace input that retrieves CIDs by 2D similarity search. It requires a CID, or a SMILES, InChI, or SDF string in the URL path or POST body (InChI and SDF by POST only). Valid output formats are XML, JSON(P), and ASNT/B.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/2244/cids/XML

Similarity search options are specified via URL arguments:

Option	Type	Meaning	Default
Threshold	integer	minimum Tanimoto score for a hit	90
MaxSeconds	integer	maximum search time in seconds	unlimited
MaxRecords	integer	maximum number of hits	2M
listkey	string	restrict to matches within hits from a prior search	none
Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/smiles/C1=NC2=C(N1)C(=O)N=C(N2)N/cids/XML?Threshold=95&MaxRecords=100

Identity
This is a special type of compound namespace input that retrieves CIDs by identity search. It requires a CID, or a SMILES, InChI, or SDF string in the URL path or POST body (InChI and SDF by POST only). Valid output formats are XML, JSON(P), and ASNT/B.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/smiles/CCCCC/cids/XML

Identity search options are specified via URL arguments:

Option	Type	Values / Meaning	Default
identity_type	string	same_connectivity, same_tautomer, same_stereo, same_isotope, same_stereo_isotope, nonconflicting_stereo, same_isotope_nonconflicting_stereo	same_stereo_isotope
MaxSeconds	integer	maximum search time in seconds	unlimited
MaxRecords	integer	maximum number of hits	2M
listkey	string	restrict to matches within hits from a prior search	none
Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/smiles/C1=NC2=C(N1)C(=O)N=C(N2)N/cids/XML?identity_type=same_isotope

Molecular Formula
This is a special type of compound namespace input that retrieves CIDs by molecular formula search. It requires a formula string in the URL path. Valid output formats are XML, JSON(P), and ASNT/B.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/C10H21N/cids/XML

Search options are specified via URL arguments:

Option	Type	Meaning	Default
AllowOtherElements	boolean	Allow other elements to be present in addition to those specified	false
MaxSeconds	integer	maximum search time in seconds	unlimited
MaxRecords	integer	maximum number of hits	2M
listkey	string	restrict to matches within hits from a prior search	none
Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/C10H21N/cids/JSON?AllowOtherElements=true&MaxRecords=10

Search Within a Search
The synchronous ("fast...") searches can use a prior result set to restrict results, using "cachekey" (a hit list storage system on the server side). For example, if you want to look for compounds that have the formula C6H12O and contain a six-membered carbon ring, first do the formula search with cachekey result:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/C6H12O/cids/JSON?list_return=cachekey

This will produce something like:

{
    "IdentifierList": {
    "Size": 692,
    "CacheKey": "is0tv08FKrkdkyiKqvJhpCDDO6PtouNSmXf4HoJm6h-Cf9Y"
    }
}
Use that cache key string as input to a substructure search this way:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/smiles/C1CCCCC1/cids/JSON?cachekey=is0tv08FKrkdkyiKqvJhpCDDO6PtouNSmXf4HoJm6h-Cf9Y

This will limit the substructure search to just those compounds found by the formula search. Note that it is important to do the more restrictive search first; a search that is too broad (like looking for substructure C1CCCCC1 across all compounds), and that results in many millions of hits, will take too long to process and will time out.

Asynchronous (polled) Search Inputs
While these are deprecated and use of these operations is not recommended, historically, PubChem used queued services for structure searches, which involved an initial request that returns a "listkey", which should followed by another request with that listkey that may return a waiting message, or the final result, for example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/listkey/xxxxx/cids/XML (where ‘xxxxx’ is the ListKey returned in the prior search request)

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/substructure/cid/2244/cids/XML?StripHydrogen=true

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/identity/cid/5793/cids/TXT?identity_type=same_connectivity

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/similarity_2d/cid/2244/cids/XML?Threshold=99

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/similarity_3d/cid/2244/cids/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/formula/C6H12O/cids/XML

Other Inputs
These are special input domains that do not deal with lists of PubChem record identifiers; regular operations are not possible with these inputs.

Source Names
Returns a list of all current depositors (sources) of substances or assays. Valid output formats are XML, JSON(P), and ASNT/B.

Examples:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/sources/substance/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug/sources/assay/JSONP

Source Table
A more complete table of source information, including organization names and record counts is available for both substances and assays. Valid output formats are CSV, XML, JSON(P), and ASNT/B.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/sourcetable/substance/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/sourcetable/assay/CSV

Classification Nodes
This is a simplified interface to retrieve lists of identifiers from classification nodes. It uses the general syntax:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/classification/hnid/<integer>/<id type>/<format>

The HNID integer can be obtained from the classification browser, and is the identifier for a specific classification node. The output identifier type is case-insensitive and must be one of: cid, compound; sid, substance; aid, bioassay; patent; pmid, pubmedid; doi; gene, geneid; protein; taxonomy, taxonomyid; pathway, pathwayid; disease, diseaseid; or cell, cellid. Note that the plural form is also accepted, e.g. "cid" or "cids". The list can also be retrieved as a cache key (but, note, not as a list key). Valid formats are TXT, XML, JSON(P), and ASNT/B.

For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/classification/hnid/1857282/cids/TXT

https://pubchem.ncbi.nlm.nih.gov/rest/pug/classification/hnid/1857282/cids/XML?list_return=cachekey

https://pubchem.ncbi.nlm.nih.gov/rest/pug/classification/hnid/4501233/patents/JSON

Periodic Table
A summary of the data used to populate PubChem's periodic table page can be retrieved through PUG REST:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/JSON

Standardize
This will return the standardized form of the user input, which can be SMILES, InChI, or SDF. Components and neutralized forms are included by default, unless "include_component=false" is specified. Valid output formats are SDF, XML, JSON(P), and ASNT/B.

For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/standardize/smiles/CCCC/SDF

https://pubchem.ncbi.nlm.nih.gov/rest/pug/standardize/smiles/CC(=O)[O-]/SDF

https://pubchem.ncbi.nlm.nih.gov/rest/pug/standardize/smiles/CC(=O)[O-]/SDF?include_components=false

Other Options
Pagination
When retrieving identifiers by listkey, the listkey_start and listkey_count options indicate at what index (zero-based) in the list to begin retrieval, and how many identifiers to return, respectively.

Example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/1,2,3,4,5/cids/XML?list_return=listkey

followed by:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/listkey/xxxxxx/cids/XML?listkey_start=2&listkey_count=2 where ‘xxxxxx’ is the listkey returned by the first URL, will return a list containing (only) CIDs 3 and 4.

Example Scripts
The following zip file contains example perl scripts demonstrating how to access PubChem data through PUG-REST.

pug_rest_scripts_nar_2018.zip

These scripts were prepared as a supplementary material of the following paper:

Kim S, Thiessen PA, Cheng T, Yu B, and Bolton EE. An Update on PUG-REST: RESTful Interface for programmatic access to PubChem. Nucleic Acids Res 2018; gky294. Epub 2018 Apr 30. doi: 10.1093/nar/gky294.



PUG REST Tutorial
The purpose of this document is to explain how PubChem’s PUG REST service is structured, with a variety of usage cases as illustrations, to help new users learn how the service works and how to construct the URLs that are the interface to this service. PUG stands for Power User Gateway, which encompasses several variants of methods for programmatic access to PubChem data and services. This REST-style interface is intended to be a simple access route to PubChem for things like scripts, javascript embedded in web pages, and 3rd party applications, without the overhead of XML, SOAP envelopes, etc. that are required for other versions of PUG. PUG REST also provides convenient access to information on PubChem records that is not possible with any other service.

Additional information of PUG REST can also be found in the following papers:

Kim S, Thiessen PA, Cheng T, Yu B, Bolton EE. An update on PUG-REST: RESTful interface for programmatic access to PubChem. Nucleic Acids Res. 2018 July 2; 46(W1):W563-570. doi:10.1093/nar/gky294.
[PubMed PMID: 29718389] [PubMed Central ID: PMC6030920] [Free Full Text]
Kim S, Thiessen PA, Bolton EE, Bryant SH. PUG-SOAP and PUG-REST: web services for programmatic access to chemical information in PubChem. Nucleic Acids Res. 2015 Jul 1; 43(W1):W605-W611. doi: 10.1093/nar/gkv396.
[PubMed PMID: 25934803] [PubMed Central PMCID: PMC4489244] [Free Full Text]
Kim S, Thiessen PA, Bolton EE. Programmatic Retrieval of Small Molecule Information from PubChem Using PUG-REST. In Kutchukian PS, ed. Chemical Biology Informatics and Modeling. Methods in Pharmacology and Toxicology. New York, NY: Humana Press, 2018, pp. 1-24. doi:10.1007/7653_2018_30.
[Full Text]
Some other documents that may be useful are:

A more technical and complete PUG REST specification document, but that is a little harder to read: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
The original purely XML-based PUG: https://pubchem.ncbi.nlm.nih.gov/docs/power-user-gateway
PUG SOAP, for applications that have built-in SOAP handlers, or programming languages with an API generated from a SOAP WSDL: https://pubchem.ncbi.nlm.nih.gov/docs/pug-soap
PUG REST is mainly designed to give small bits of information on one or more PubChem records. Users may also be interested in PUG View (https://pubchem.ncbi.nlm.nih.gov/docs/pug-view), which provides more complete but longer summary reports on individual PubChem records.

PUG REST is actively maintained and updated, so check this page for new features. For comments, help, or to suggest new functionality or topics for this tutorial, please contact pubchem-help@ncbi.nlm.nih.gov.

USAGE POLICY: Please note that PUG REST is not designed for very large volumes (millions) of requests. We ask that any script or application not make more than 5 requests per second, in order to avoid overloading the PubChem servers. To check additional request volume limitations, please read this document on dynamic request throttling. If you have a large data set that you need to compute with, please contact us for help on optimizing your task, as there are likely more efficient ways to approach such bulk queries.

503 HTTP STATUS CODE: Please note that this status code may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

How PUG REST Works
The fundamental unit upon which PUG REST is built is the PubChem identifier, which comes in three flavors – SID for substances, CID for compounds, and AID for assays. The conceptual framework of this service, that uses these identifiers, is the three-part request: 1) input – that is, what identifiers are we talking about; 2) operation – what to do with those identifiers; and 3) output – what information should be returned. The beauty of this design is that each of these three parts of the request is (mostly) independent, allowing a combinatorial expansion of the things you can do in a single request. Meaning that, for example, any form of input that specifies some group of CIDs can be combined with any operation that deals with CIDs, and any output format that’s relevant to the chosen operation. So instead of a list of separate narrowly defined service requests that are supported, you can combine these building blocks in many ways to create customized requests.

PUG REST Design

For example, this service supports input of chemical structure by SMILES. It supports output of chemical structure as images in PNG format. You can combine these two into a visualization request for a SMILES string – in this case, whether or not that particular chemical is even in the PubChem database at all! And it’s something you can almost type manually into a web browser:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CCCCBr/PNG

Or, combine input by chemical name with InChI property retrieval, and you have a simple name-to-InChI service in a single request:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/vioxx/property/InChI/TXT

The possibilities are nearly endless, and more importantly, the action of the service is simple to understand from the URL alone, without needing any extra programming, XML parsing, etc. And at the same time, more complex data handling is available for programmers who want rigorous schema-based XML communications, or who want to use JSON data to embed functionality in a web page via JavaScript.

Input: Design of the URL
PUG REST is entirely based on HTTP (or HTTPS) requests, and most of the details of the request are encoded directly in the URL path – which is what makes the service RESTful (informally anyway, as it does not adhere strictly to REST principles, which are beyond the scope of this discussion). Continuing with the last example above, let’s examine the structure of the URL, which is divided into the three main parts of input, operation, and output, in an ordered sequence that will sometimes be referred to in this document as the URL path:

https://pubchem.ncbi.nlm.nih.gov/rest/pug	/compound/name/vioxx	/property/InChI	/TXT
prolog	input	operation	output
Taking each section individually, first we have the prolog – the HTTP address of the service itself, which is common to all PUG REST requests. The next part is the input, which in this case says “I want to look in the PubChem Compound database for records that match the name ‘vioxx’.” Note that there some subtleties here, in that the name must already be present in the PubChem database, and that a name may refer to multiple CIDs. But the underlying principle is that we are specifying a set of CIDs based on a name; at the time of writing, there is only one CID with this name. The next section is the operation, in this case “I want to retrieve the InChI property for this CID.” And finally the output format specification, “I want to get back plain text.”

Some requests may use optional parameters, things after the ‘?’ at the end of the URL path. PUG REST can accept by URL-encoded arguments and/or HTTP POST some types of inputs that cannot be put into a URL path, such as InChI strings, or certain types of SMILES that contain special characters that conflict with URL syntax, or multi-line SDF files. There is a separate section towards the end of this document that explains this process in more detail. There are some additional complexities to the HTTP protocol details that aren’t covered here – see the specification document for more information.

Output: What You Get Back
The results of most operations can be expressed in a variety of data formats, though not all formats are relevant to all operations, meaning for example you can’t get back a list of CIDs in SDF format, or a chemical structure in CSV format. It is your choice which format to use, and will likely depend on the context of the requests; a C++ application may wish to use XML that is automatically parsed into class objects based on the schema, while a JavaScript applet in a web page would more naturally use JSON to have convenient access to the result data. Plain text (TXT) output is limited to certain cases where all output values are of the same simple type, such as a list of chemical name synonyms or SMILES strings. The available output formats are listed below.

Output Format	Description
XML	standard XML, for which a schema is available
JSON	JSON, JavaScript Object Notation
JSONP	JSONP, like JSON but wrapped in a callback function
ASNB	standard binary ASN.1, NCBI’s native format in many cases
ASNT	NCBI’s human-readable text flavor of ASN.1
SDF	chemical structure data
CSV	comma-separated values, spreadsheet compatible
PNG	standard PNG image data
TXT	plain text
Error Handling
If there is a problem with a request, PUG REST will usually return some sort of human-readable message indicating what went wrong – whether it’s an invalid input, or nothing was found for the given query, or the request was too broad and took too long to complete (more than 30 seconds, the NCBI standard time limit on web service requests), etc. See the specification document for more detail on result and HTTP status codes.

Special Characters in the URL
Most PUG REST URLs can be written as a simple URL "path" with elements separated by the '/' character. But some inputs, like SMILES (with stereochemistry) and InChI, contain '/' or other special characters that conflict with URL syntax. In these cases, PUG REST can take the input field as a URL-encoded CGI argument value (after the '?' in the URL), using the same argument name that appears in the path. For example, to use the InChI string

InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)

as input, use just /inchi/ in the path part of the URL, and the argument inchi=(URL-encoded-string) as a CGI parameter:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchi/cids/JSON?inchi=InChI%3D1S%2FC9H8O4%2Fc1-6%2810%2913-8-5-3-2-4-7%288%299%2811%2912%2Fh2-5H%2C1H3%2C%28H%2C11%2C12%29

Access to PubChem Substances and Compounds
This section covers some of the basic methods of accessing PubChem chemical structure information, with many working samples. It is not intended to be a comprehensive document covering all PUG REST features, but rather enough of the common access methods to give a reasonable overview of how the service is designed and what it can do, so that one can quickly begin to use it for custom applications.

Input Methods
The first part of any PUG REST request is the input, which tells the service which records you’re interested in. There are many ways to approach this; the most common are presented here, with examples.

By Identifier
The most straightforward way to tell PUG REST what records you’re interested in is by specifying the SIDs or CIDs directly. This example says “give me the names of substance with SID 10000 in XML format”:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/10000/synonyms/XML

IDs may also be specified in a comma-separated list, here retrieving a CSV table of compound properties:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/1,2,3,4,5/property/MolecularFormula,MolecularWeight,SMILES/CSV

Large lists of IDs that are too long to put in the URL itself may be specified in the POST body, but be aware that if a PUG REST requests takes more than 30 seconds to complete, it will time out, so it’s better to deal with moderately sized lists of identifiers.

By Name
It is often convenient to refer to a chemical by name. Be aware though that matching chemical names to structure is an inexact science at best, and a name may often refer to more than one record. For example, “glucose” gives (at the time of writing) four CIDs, the same as if you were to search for that name by full synonym match in Entrez:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glucose/cids/TXT

Some operations will use only the first identifier in the list, so if you want a picture of glucose, you can get what PubChem considers the “best” match to that name with the following URL:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glucose/PNG

By default, the given name must be an exact to match the entire name of the record; optionally, you can specify that matches may be to individual words in the record name:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/myxalamid/cids/XML?name_type=word

By Structure Identity
There are numerous ways to specify a compound by its chemical structure, using SMILES, InChI, InChI key, or SDF. InChI and SDF require the use of POST because the format is incompatible with a simple URL string, so they won’t be discussed here. But specifying with most  SMILES strings, or InChI key, is straightforward. For some operations, a SMILES can be used to get data even if the structure is not present in PubChem already, but may not work for others like retrieval of precomputed properties. The InChI key must always be present in the database, since unlike these other formats, it is not possible to determine structure from the key alone. This example will give the PubChem CID for the SMILES string “CCCC” (butane):

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CCCC/cids/TXT

By Structure Search
The previous section describes how one can specify a structure, for which PUG REST will return only an exact match. There are however more sophisticated structure search techniques available, including substructure and superstructure, similarity (2D Tanimoto), and various partial identity matches (like same atom connectivity but unspecified stereochemistry). Molecular formula search also falls into this category in PUG REST. The complication with these searches is that it takes time to search the entire PubChem database of tens of millions of compounds, and so results may not be available within the previously mentioned 30 second time period of a PUG REST request. To work around this, PUG REST uses what is called an “asynchronous” operation, where you get a request identifier that is a sort of job ticket when you start the search. Then it is the caller’s responsibility to check periodically (say, every 5-10 seconds) whether the search has finished, and if so, retrieve the results. It is a two stage process, where the search is initiated by a request like this search for all records containing a seven-membered carbon ring:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/substructure/smiles/C1CCCCCC1/XML

The result of that request will include what PUG REST calls a “ListKey” – which is currently a unique, private, randomly-assigned 64 bit integer. This key is used in a subsequent request like:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/listkey/12345678910/cids/TXT

… where the listkey number in the above URL is the actual ListKey returned in the first call. This will either give a message to the effect of “your search is still running,” or if complete, will return the list of CIDs found - in this example at this time, around 230,000 records. (See below for more on how to deal with large lists of identifiers.)

By Fast (Synchronous) Structure Search
Some re-engineering of the PubChem search methods has enabled faster searching by identity, similarity (2D and 3D), substructure, and superstructure. These methods are synchronous inputs, meaning there is no waiting/polling necessary, as in the majority of cases they will return results in a single call. (Timeouts are possible if the search is too broad or complex.) These are normal input methods and can be used with any output. Some examples are below:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/5793/cids/TXT?identity_type=same_connectivity

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/cid/2244/cids/XML?StripHydrogen=true

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/2244/property/MolecularWeight,MolecularFormula,RotatableBondCount/XML?Threshold=99

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/2244/cids/JSON

By Cross-Reference (XRef)
PubChem substances and compounds often include a variety of cross-references to records in other databases. Sometimes it’s useful to do a reverse lookup by cross-reference value, such as this request that returns all SIDs that are linked to a patent identifier:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/xref/PatentID/US20050159403A1/sids/JSON

For a full list of cross-references available, see the specification document.

By Mass
Compounds (CIDs) can be selected by mass value or range. Mass types are "molecular_weight", "exact_mass", and "monoisotopic_mass". Lookup can be by equality to a single value, or within an inclusive range of values. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/molecular_weight/range/400.0/400.05/cids/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/exact_mass/equals/484.29372238/cids/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/monoisotopic_mass/range/455.14196/455.14198/cids/JSON

Available Data
Now that you’ve learned how to tell PUG REST what records you want to access, the next stage is to indicate what to do with these records – what information about them you want to retrieve. One of the major design goals of PUG REST is to provide convenient access to small “bits” of information about each record, like individual properties, cross-references, etc., which may not be possible with any other PubChem service without having to download a large quantity of data and sort through it for the one piece you need. That is, PubChem provides many ways to retrieve bulk data covering the entire database, but if all you want is, say, the molecular weight of one compound, PUG REST is the way to get this simply and quickly. (Whereas PUG REST is not the best way to get information for the whole database – so it’s probably not a good idea to write a “crawler” that calls PUG REST individually for every SID or CID in the system – there are better ways to get data for all records.)

Full Records
PUG REST can be used to retrieve entire records, in the usual formats that PubChem supports – ASN.1 (NCBI’s native format), XML, SDF. Now you can even get full records in JSON(P) as well. In fact, full record retrieval is the default action if you don’t specify some other operation. For example, both of these will return the record for aspirin (CID 2244) in various fully equivalent formats:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/SDF

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/record/XML

You can also request multiple records at once, though be aware that there is still the timeout limit on record retrieval so large lists of records may not be practical this way – but of course PubChem provides separate bulk download facilities.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/1,2,3,4,5/SDF

Images
As far as PUG REST is concerned, images are really a flavor of full-record output, as they depict the structure as a whole. So all you have to do to retrieve an image is to specify PNG format output instead of one of the other data formats described in the previous section. Note though that an image request will only show the first SID or CID in the input identifier list, there is currently no way to get multiple images in a single request. (However, PubChem’s download service can be used to get multiple images.) Image retrieval is fully compatible with all the various input methods, so for example you can use this to get an image for a chemical name, SMILES string, InChI key, etc.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/lipitor/PNG

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/CCCCC=O/PNG

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/RZJQGNCSTQAWON-UHFFFAOYSA-N/PNG

Compound Properties
All of the pre-computed properties for PubChem compounds are available through PUG REST, individually or in tables. See the specification document for a table of all the property names. For example, to get just a single molecular weight value:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/MolecularWeight/TXT

Or a CSV table of multiple compounds and properties:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/1,2,3,4,5/property/MolecularWeight,MolecularFormula,HBondDonorCount,HBondAcceptorCount,InChIKey,InChI/CSV

Synonyms
Chemical names can be both input and output in PUG REST. For example, to see all the synonyms of Vioxx that PubChem has, a rather long list:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/vioxx/synonyms/XML

Cross-References (XRefs)
PubChem has many cross-references between databases, all of which are available through PUG REST. See the specification document for a table of all the cross-reference types. For example, to get all the MMDB identifiers for protein structures that contain aspirin:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/xrefs/MMDBID/XML

Or the inverse of an example above, retrieving all the patent identifiers associated with a given SID:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/137349406/xrefs/PatentID/TXT

And More…
This gives you some idea of the sorts of data one can access through PUG REST. It is not a comprehensive list, as we have not covered dates, classifications, BioAssay information and SID/CID/AID cross-links (detailed more below), etc.; more features may be added in the future. And we welcome feedback on new feature suggestions as well!

Access to PubChem BioAssays
In this section we describe the various types of BioAssay information available through PUG REST. A PubChem BioAssay is a fairly complex and sometimes very large entity with a great deal of data, so there are routes both to entire assay records and various component data readouts, etc., so that you can more easily get just the data that you’re interested in.

From AID
Assay Description
An assay is composed of two general parts: the description of the assay as a whole, including authorship, general description, protocol, and definitions of the data readout columns; and then the data section with all the actual test result values. To get just the description section via PUG REST, use a request like:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/description/XML

There is also a simplified summary format that does not have the full complexity of the original description as above, and includes some information on targets, active and inactive SID and CID counts, etc. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1000/summary/JSON

Assay Data
BioAssay data may be conceptualized as a large table where the columns are the readouts (enumerated in the description section), and the rows are the individual substances tested and their results for each column. So, retrieving an entire assay record involves the primary AID – the identifier for the assay itself – and a list of SIDs. If you want all the data rows of an assay, you can use a simple request like this one, which will return a CSV table of results. Note that full-data retrieval is the default operation for assays.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/CSV

However, as some assays have many thousands of SID rows, there is a limit, currently 10,000, on the number of rows that can be retrieved in a single request. If you are interested in only a subset of the total data rows, you can use an optional argument to the PUG REST request to limit the output to just those SIDs (and note that with XML/ASN output you get the description as well when doing data retrieval). There are other ways to input the SID list, such as in the HTTP POST body or via a list key; see below for more detail on lists stored on the server.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/XML?sid=104169547,109967232

If you are only interested in the concise data (i.e. active concentration readout), you can request it with additional information (i.e. AID, SID, CID, Activity Outcome, Target Accession, Target GeneID, Activity Value [uM], Activity Name, Assay Name, Assay Type, PubMed ID, RNAi):

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/concise/JSON (XML and CSV are valid output formats)

Some assay data may be recast as dose-response curves, in which case you can request a simplified output:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/504526/doseresponse/CSV?sid=104169547,109967232

Targets
When the target of a BioAssay is known, it can be retrieved either as a sequence or gene, including identifiers in NCBI’s respective databases for these:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/490,1000/targets/ProteinGI,ProteinName,GeneID,GeneSymbol/XML

Note though that not all assays have protein or gene targets defined.

It is also possible to select assays via target identifier, specified by GI, Gene ID, or gene symbol, for example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/genesymbol/USP2/aids/TXT

Activity Name
BioAssays may be selected by the name of the primary activity column, for example to get all the AIDs that are measuring an EC50:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/activity/EC50/aids/JSON

Access to PubChem Genes
Gene Input Methods
By Gene ID
This is the recommended way to access gene data in PubChem by using the NCBI Gene identifiers. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/1956,13649/summary/JSON

For the sake of performance, some operations (e.g. retrieving bioactivity data) are limited to a single gene only, e.g.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/13649/concise/JSON

By Gene Symbol
One can use the official gene symbol to access gene data in PubChem. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/summary/JSON

Note that a gene symbol (case-insensitive) often maps to multiple genes of different organisms. For simplicity, it returns data by default for human genes. One can provide further taxonomy information to indicate the specific organism using NCBI Taxonomy ID, scientific taxonomy name, common taxonomy name, or taxonomy synonym. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/10090/summary/JSON (mouse Egfr gene by NCBI Taxonomy ID 10090)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/Mus%20musculus/summary/JSON (mouse Egfr gene by scientific taxonomy name)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/house%20mouse/summary/JSON (mouse Egfr gene by common taxonomy name)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/mouse/summary/JSON (mouse Egfr gene by taxonomy synonym)

By Gene Synonym
One can also use gene synonym such as alternative or old name to access gene data in PubChem. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/ERBB1/summary/JSON

Note that one synonym often maps to multiple genes of different organisms. For simplicity, only one gene synonym is allowed as input at a time.

Identifiers from external sources are treated as synonyms. So, the following link returns data for human EGFR in PubChem.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/HGNC:3236/summary/JSON

It is recommended to prepend IDs with ID source (e.g. Ensembl:ENSG00000146648) to eliminate ambiguity, though the two links below work the same:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/Ensemble:ENSG00000146648/summary/JSON (with ID source, recommended)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/ENSG00000146648/summary/JSON (without ID source)

Available Gene Data
Gene Summary
This operation returns a summary of gene:  GeneID, Symbol, Name, TaxonomyID, Taxonomy, Description, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/1956,13649/summary/JSON (by Gene ID)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/summary/XML (by gene symbol, case insensitive and default to human)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/10090/summary/JSON (mouse with NCBI TaxonomyID 9606)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/Rattus%20norvegicus/summary/JSON (mouse with scientific taxonomy name)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/genesymbol/EGFR/Norway%20rat/summary/JSON (mouse with common taxonomy name)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/synonym/EGFR/summary/JSON (by synonym, note that one synonym may map to multiple GeneIDs)

Assays from Gene
This operation returns a list of AIDs tested against a given gene. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/13649/aids/TXT

For the sake of performance, only one gene is allowed as input.

Bioactivities from Gene
This operation returns the concise bioactivity data for a given gene. Valid output formats are XML, JSON(P), ASNT/B, and CSV.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/13649/concise/JSON (limited to one gene at a time)

For some genes with a large amount of data, the operation may be timed out. In such cases, one can first get the list of AIDs tested against the given gene, e.g.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/13649/aids/TXT

Then aggregate the concise bioactivity data from each AID, e.g.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/66438/concise/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/69721/concise/JSON

Pathways from Gene
This operation returns a list of pathways in which a given gene is involved. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/gene/geneid/13649/pwaccs/TXT

Such pathway accessions can then be used to access PubChem Pathways data.

Access to PubChem Proteins
Protein Input Methods
By Protein Accession
This is the recommended way to access protein data in PubChem by using the NCBI Protein accessions. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P00533,P01422/summary/JSON (single accession or a list of comma-separated accessions)

By Protein Synonym
One can also use protein synonym to access protein data in PubChem. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/synonym/PR:P00533/summary/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/synonym/ChEMBL:CHEMBL203/summary/JSON

Identifiers from external sources are treated as synonyms. It is recommended to prepend IDs with ID source to eliminate ambiguity.

Available Protein Data
Protein Summary
This operation returns a summary of protein:  ProteinAccession, Name, TaxonomyID, Taxonomy, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P00533,P01422/summary/JSON

Assays from Protein
This operation returns a list of AIDs tested against a given protein. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P00533/aids/TXT (limited to one protein only)

Bioactivities from Protein
This operation returns the concise bioactivity data for a given protein. Valid output formats are XML, JSON(P), ASNT/B, and CSV.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/Q01279/concise/JSON

For some proteins with a large amount of data, the operation may time out. In such cases, one can first get the list of AIDs tested against the given protein, e.g.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/Q01279/aids/TXT

Then aggregate the concise bioactivity data from each AID:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/66438/concise/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/69721/concise/JSON

Pathways from Protein
This operation returns a list of pathways in which a given protein is involved. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/protein/accession/P00533/pwaccs/TXT

Such pathway accessions can then be used to access PubChem Pathways data.

Access to PubChem Pathways
Pathway Input Methods
By Pathway Accession
This is the only way to access pathway information in PubChem. The Pathway Accession is in the form of Source:ID (see more information here). For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171/summary/JSON (single accession)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983/summary/JSON (a list of comma-separated accessions)

Available Pathway Data
Pathway Summary
This operation returns a summary of pathway:  PathwayAccession, SourceName, SourceID, SourceURL, Name, Type, Category, Description, TaxonomyID, and Taxonomy. Valid output formats are XML, JSON(P), and ASNT/B. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171,BioCyc:HUMAN_PWY-4983/summary/JSON

Compounds from Pathway
This operation returns a list of compounds involved in a given pathway. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171/cids/TXT (limited to one pathway only)

Genes from Pathway
This operation returns a list of genes involved in a given pathway. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171/geneids/TXT (limited to one pathway only)

Proteins from Pathway
This operation returns a list of proteins involved in a given pathway. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/pathway/pwacc/Reactome:R-HSA-70171/accessions/TXT  (limited to one pathway only)

Access to PubChem Taxonomies
Taxonomy Input Methods
By Taxonomy ID
This is the recommended way to access taxonomy information by using the NCBI Taxonomy identifiers. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/taxid/9606,2697049/summary/JSON (one ID or a list of comma-separated IDs)

By Taxonomy Synonym
One can also use taxonomy synonym such as scientific name and common name to access taxonomy information in PubChem. This is limited to one synonym at a time for simplicity. For example:
https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/synonym/Homo%20sapiens/summary/JSON
https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/synonym/human/summary/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/synonym/SARS-COV-2/summary/JSON

Identifiers from external sources are treated as synonyms. It is recommended to prepend IDs with ID source (e.g. ITIS:180092) to eliminate ambiguity. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/synonym/ITIS:180092/summary/JSON

Available Taxonomy Data
Taxonomy Summary
This operation returns a summary of taxonomy: TaxonomyID, ScientificName, CommonName, Rank, RankedLineage, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/taxid/9606,10090,10116/summary/JSON

Assays and Bioactivities
The following operation returns a list of compounds involved in a given taxonomy. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/taxonomy/taxid/2697049/aids/TXT

There is no operation available to directly retrieve the bioactivity data associated with a given taxonomy, as often the data volume is huge. However, one can first get the list of AIDs using the above link, and then aggregate the concise bioactivity data from each AID, e.g.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/1409578/concise/JSON

Access to PubChem Cell Lines
Cell Line Input Methods
By Cell Line Accession
PubChem is using Cellosaurus and ChEMBL cell line accessions as its identifiers. This is the recommended way to access cell line data in PubChem. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/cellacc/CHEMBL3308376,CVCL_0045/summary/JSON

By Cell Line Synonym
One can also use cell line synonym such as name to access cell line information. For example: 

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/HeLa/summary/JSON

Identifiers from external sources are treated as synonyms. It is recommended to prepend IDs with ID source (e.g. MeSH:D006367). For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/MeSH:D006367/summary/JSON

Available Cell Line Data
Cell Line Summary
This operation returns a summary of cell line: CellAccession, Name, Sex, Category, SourceTissue, SourceTaxonomyID, SourceOrganism, and a list of Synonyms. Valid output formats are XML, JSON(P), and ASNT/B. For example:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/cellacc/CVCL_0030,CVCL_0045/summary/JSON (by Cellosaurus cell line accession)

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/HeLa/summary/JSON (by synonym)

Assays and Bioactivities from Cell Line
This operation returns a list of assays tested on a given cell line. Valid output formats are XML, JSON(P), ASNT/B, and TXT.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/cell/synonym/HeLa/aids/TXT

There is no operation available to directly retrieve the bioactivity data associated with a given taxonomy, as often the data volume is huge. However, one can first get the list of AIDs using the above link, and then aggregate the concise bioactivity data from each AID, e.g.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/79900/concise/JSON

Dealing with Lists of Identifiers
Storing Lists on the Server
Some PUG REST requests may result in a very long list of identifiers, and it may not be practical to deal with all of them at once. Or you may have a set of identifiers you want to be able to use for several subsequent requests of different types. For this reason, we provide a way to store lists on the server side, and retrieve them in part or whole. The basic idea is that you request a “List Key” for your identifiers – in fact the same sort of key you get from a structure search as mentioned above. But any operation that results in a list of SIDs, CIDs, or AIDs can be stored in a ListKey this way, not just structure search.

Say for example you want to look at all the SIDs tested in a large assay. First make the request to get the SIDs and store them on the server:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/640/sids/XML?list_return=listkey

This will return a ListKey – along with the size of the list, and values needed to retrieve this same list from Entrez’s eUtils services. You can then use that listkey in subsequent request. For example, since assay data retrieval is limited in the number of rows, you could break it up into multiple requests of 1,000 SID rows at a time, like:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/640/CSV?sid=listkey&listkey=12345678910&listkey_start=0&listkey_count=1000

Here, substitute the “listkey” value with the key returned by the initial request above, then “listkey_start” is the zero-based index of the first element of the list to use, and “listkey_count” is how many. Simply repeat the request with increasing values of “listkey_start” in order to loop over the entire assay – either to get the contents of the whole assay, or (with a smaller count value perhaps) to show one page of results at a time in a custom assay data viewer, with pagination controls to move through the whole set of results.

A ListKey can be used in most places that could otherwise take an explicit list of identifiers. So, for example, the same list of SIDs can be used in the context of substance requests, such as this one to get the synonyms associated with the first 10 records on the same list:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/listkey/12345678910/synonyms/XML?&listkey_start=0&listkey_count=10

You can even create lists from identifiers specified in the URL (or in the HTTP POST body):

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/1,2,3,4,5/cids/XML?list_return=listkey

List Sharing between PUG-REST and E-Utilities
E-Utilities are a set of programs that provide programmatic access to data within the Entrez system, which integrates PubChem with other NCBI databases.  While appropriate for searching or accessing text and numeric data, E-Utilities are not suitable for handling other types of data specific to PubChem (such as chemical structure queries, and bioactivity data tables).  These data are readily accessible through PubChem-specific programmatic access routes such as PUG, PUG-SOAP, and PUG-REST.  Therefore, E-Utilities and PubChem-specific programmatic access routes complement each other.  As a result, to get desired data from PubChem programmatically, one may need to use the result from a PUG-REST request as an input to a subsequent E-Utilities request, or vice versa.

This can be done using the PubChem List Gateway, available at the URL:

https://pubchem.ncbi.nlm.nih.gov/list_gateway/list_gateway.cgi

It is a common gateway interface (CGI) that converts between the list key from a PUG-REST request and the Entrez history from an E-Utilities request.

An Entrez history is specified using three parameters: database (DB), Query Key, and WebEnv.  The list gateway takes these three parameters for an Entrez history, and returns a list key, which can be used in a subsequent PUG-REST request.  As an example, the following URL shows how to convert from a Entrez history to a PUG-REST list key:

https://pubchem.ncbi.nlm.nih.gov/list_gateway/list_gateway.cgi?action=entrez_to_pug&entrez_db=DB&entrez_query_key=QUERYKEY&entrez_webenv=WEBENV

where QUERYKEY and WEBENV are the Query Key and WebEnv values for an Entrez history, respectively, and DB is the name of the PubChem database in Entrez (“pccompound” for Compound, “pcsubstance” for Substance, and “pcassay” for BioAssay).  The returned list key can be used in a PUG-REST request, as described in the Storing Lists on the Server section above.

Conversely, the list key from a PUG-REST request can be converted into the three parameters (DB, Query Key, and WebEnv) that specifies an Entrez history, via the following URL:

https://pubchem.ncbi.nlm.nih.gov/list_gateway/list_gateway.cgi?action=pug_to_entrez&pug_listkey=LISTKEY

where LISTKEY is a PUG-REST list key.  The returned Entrez history (specified by DB, Query Key, WebEnv) can be used in an E-Utilities request (e.g., ESearch, ESummary, EFetch, or ELink).

Inter-conversion of Identifiers
PubChem has many (many) types of cross-links between databases, or between one records and other records in the same database. That is, you can move from “SID space” to “CID space” in a variety of ways, depending on just what relationship you’re interested in. The specification document has a complete table of these identifier inter-conversion options, depending on whether you’re starting from SIDs, CIDs, or AIDs. We’ll show a few examples here.

You’ve already seen one example just above of getting back SIDs associated with a given AID. That request returns all SIDs, but it’s also possible to get just the SIDs that are active in the assay, in this case a much smaller list than the full set of ~96,000 SIDs that were tested:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/640/sids/TXT?sids_type=active

Or to retrieve all the substances corresponding exactly to the structure of aspirin (CID 2244), which shows all the records of this chemical structure supplied to PubChem by multiple depositors – and there are many in this case. This sort of conversion operation can also be combined with ListKey storage in the same way discussed above, in case the results list is long.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/sids/XML?sids_type=standardized&list_return=listkey

There are operations to retrieve the various groups of related chemical structures that PubChem computes, such as this request to retrieve all compounds – salts, mixtures, etc. – whose parent compound is aspirin; that is, where aspirin is considered to be the “important” part of the structure:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/cids/TXT?cids_type=same_parent

Sometimes it’s possible to group lists of identifiers in the result according to identifiers in the input, and PUG REST includes options for that as well. Compare the output of the following two requests. The first simply returns one group of all standardized SIDs corresponding to any compound with the name ‘glucose’ (that is, deposited records that match one of the glucose CIDs exactly). The second groups them by CID, which is actually the default for this sort of request, unless you are storing the list on the server via ListKey, in which case it is necessarily flattened.

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glucose/sids/XML?sids_type=standardized&list_return=flat

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glucose/sids/XML?sids_type=standardized&list_return=grouped

How To Use HTTP POST
While being able to write most PUG REST requests as simple URLs is convenient, sometimes there are inputs that do not work well with this approach because of syntax conflicts or size restrictions. For example, a multi-line SDF file, any name or SMILES string or InChI that has ‘/’ (forward slash) or other special characters that are reserved in URL syntax, or long lists of identifiers that are too big to put directly in the URL of an HTTP GET request, can be put in the HTTP POST body instead. Many (though not necessarily all) of the PUG REST input types allow the argument to be specified by POST. While this isn’t something that one can type into a regular web client, most programmatic HTTP interface libraries will have the ability to use POST. Technically, there is no limit to the size of the POST body, but practically, a very large input may take a long time for PUG REST to process, leading to timeouts if it takes longer than 30 seconds.

There are existing standards for just how the information in the POST body is formatted, and you must include in the PUG REST call an HTTP header that indicates which content type you are supplying. The simpler format is “Content-Type: application/x-www-form-urlencoded” which is the same as the URL argument syntax after the ‘?’ separator, of the general form “arg1=value1&arg2=value2&…” (See here for more technical detail on these content types.) For example, use a URL like

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchi/cids/JSON

with “Content-Type: application/x-www-form-urlencoded” in the request header, and put the string

inchi=InChI=1S/C3H8/c1-3-2/h3H2,1-2H3

in the POST body. (With InChI this looks a little weird, because the first “inchi=” is the name of the PUG REST argument, and the second “InChI=” is part of the InChI string itself.) You should get back CID 6334 (propane). Note that some special characters may still need to be escaped, in particular the ‘+’ (plus sign) character which is a standard replacement for a space character in URL syntax. You must replace this with “%2B”, such as “smiles=CC(=O)OC(CC(=O)[O-])C[N%2B](C)(C)C” to use the SMILES string for CID 1 (acetylcarnitine). If PUG REST is giving you a “bad request” or “structure cannot be standardized” error message with your input, it’s possible there are other special characters that need to be escaped this way.

The first method just described above works well for single-line input strings, but is not applicable to inputs like SDF which are necessarily multi-lined. For this type, you’ll need to use the multipart/form-data type, and an appropriately formatted input. This method is a little more complex because of the existing protocol standard. To use the same example as above, first prepare a file (or string) that looks like this:

--AaB03x

Content-Disposition: form-data; name="inchi"

Content-Type: text/plain

InChI=1S/C3H8/c1-3-2/h3H2,1-2H3

--AaB03x--

Note that the POST body string/file in this case must have DOS-style “CR+LF” line endings, and there must be an empty line between the content headers and actual data line(s) (and no blank lines anywhere else). But in this format, no further escaping of special characters is needed. It looks a little strange, but your HTTP library may know how to construct this sort of thing automatically, check your documentation. This would be sent to the same URL as before, e.g.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchi/cids/JSON

but this time with “Content-Type: multipart/form-data; boundary=AaB03x” in the request header. It is essential that the arbitrary boundary string given in the header match what’s used in the POST body (“AaB03x” in this example).

Conclusion
If you’ve read this far, hopefully by now you have a good understanding of the sorts of things PUG REST can do to facilitate access to PubChem data, and how to write your own PUG REST requests. Please feel free to contact us at pubchem-help@ncbi.nlm.nih.gov for assistance, if there’s something you’d like to be able to do with this service but can’t quite figure out how to formulate the requests, or if the features you need simply aren’t present and you would like us to consider adding them.



PUG View
PUG View is a REST-style web service that provides information content that is not directly contained within the primary PubChem Substance, Compound, or BioAssay records. Its purpose is primarily to drive the PubChem database summary record web pages, but can also be used independently as a programmatic web service.

PUG View is mainly designed to provide complete summary reports on individual PubChem records. Users may also be interested in PUG REST, a different style of service that gives smaller bits of information about one or more PubChem records.

An overview of PUG View can be found in the following paper:

Kim S, Thiessen PA, Cheng T, Zhang J, Gindulyte A, Bolton EE. PUG-View: programmatic access to chemical annotations integrated in PubChem. J Cheminform. 2019 Aug 9; 11:56. doi:10.1186/s13321-019-0375-2.
[PubMed PMID: 31399858] [PubMed Central PMCID: PMC6688265] [Free Full Text]

USAGE POLICY: Please note that PUG View is not designed for very large volumes (millions) of requests. We ask that any script or application not make more than 5 requests per second, in order to avoid overloading the PubChem servers. To check additional request volume limitations, please read this document. If you have a large data set that you need to compute with, please contact us for help on optimizing your task, as there are likely more efficient ways to approach such bulk queries.

503 HTTP STATUS CODE: Please note that this status code may be returned when the server is temporarily unable to service your request due to maintenance downtime or capacity problems. (Please try again later.) Please also note that an HTML document may be returned.

Formats
PUG View provides structured information in a variety of formats, specified at the end of the URL path. Most results can be formatted as JSON(P), XML, or ASN.1 as text (ASNT) or base64-encoded binary (ASNB). For example, these all contain exactly the same information, just in different formats:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSONP?callback=func

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/XML

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/ASNT

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/ASNB

An XML schema is available here. Note that the JSON and ASN.1 formats follow the same content model.

https://pubchem.ncbi.nlm.nih.gov/pug_view/pug_view.xsd

Record Summaries
Full Records and Indexes
PUG View provides record summaries for the three primary PubChem databases - Compounds, Substances, and BioAssays - as well as patents and targets. Each of these can be accessed as an index, providing a listing of what information is present, but without the entire data content; essentially a table of contents for that record:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/index/compound/1234/JSON

Or the complete data can be retrieved:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON

This choice of index or full data is applicable to all the primary record types.

Specific Heading
If only a subcategory of information is desired, a heading can be used to restrict the data returned. Note that the index as above is a convenient way to see what headings are present for a given record, as not all records will have all possible headings present. For example, to get just the experimental property section:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/2244/JSON?heading=Experimental+Properties

Or even just a single value type, like melting point:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/2244/JSON?heading=Melting+Point

Section headings that can be used in PUG-View data retrieval can be found in the PubChem Compound TOC tree (using the PubChem Classification Browswers).

https://pubchem.ncbi.nlm.nih.gov/classification/#hid=72
 

Compounds
Compounds records are accessed by CID number. Note that PUG View provides textual and third-party information associated with the compound, but not the chemical structure, which is handled by other PubChem services.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1234/JSON

Substances
Substances records are accessed by SID number. Information on substances is fairly minimal; in particular, no third party annotation is associated with substances. Again, chemical structure is not part of PUG View’s results.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/substance/1/JSON

BioAssays
BioAssays are accessed by AID number.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/assay/1/JSON

Patents
Patents can be accessed by an identifier string.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/US-5837728-A/JSON

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/US-2015000048-A1/XML

Genes
Gene information can be retrieved by NCBI Gene ID:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/gene/1/JSON

Proteins
Protein information can be retrieved by NCBI Protein Accession:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/protein/P00533/JSON

Pathways
Pathway information can be retrieved by Source:ExternalID:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/pathway/Reactome:R-HSA-70171/JSON/

Taxonomies
Taxonomy information can be retrieved by NCBI Taxonomy ID:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/taxonomy/9606/JSON/

Cell Lines
Taxonomy information can be retrieved by Cell Line name (case-insensitive):

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/cell/HeLa/JSON/

Elements
Element information can be retrieved by atomic number:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/element/17/JSON/

Special Reports
The following are not primary PubChem records, but rather extra information of various sorts that is attached to PubChem records. These reports contain information not present in the main record data described above.

Annotations
PUG View can provide information of a specific type across all of PubChem’s primary databases. For example, if you are interested in all of the experimental viscosity measurements contained within PubChem and its associated third-party annotations, you can request this by heading:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/Viscosity/JSON

Or equivalently (useful if the heading contains special characters not compatible with URL syntax):

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/JSON?heading=Viscosity

This will include PubChem identifiers – CIDs in this example – for each data value, along with attribution detailing exactly where each bit of information was obtained.

Note that in the PubChem data model, a heading may refer to different types of PubChem records, making it necessary to specify which one is intended:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/Boiling%20Point/XML?heading_type=Compound

Also keep in mind that some headings have more data than others, and retrieval is limited. There will be "Page" and "TotalPages" values at the end of the request data, that will indicate the given page number and whether there is more data than shown in the given request (that is, whether TotalPages is greater than one). By default, page #1 is returned, but subsequent pages (up to the TotalPages limit) can be accessed by adding a page argument: 

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/CAS/JSON?page=10

Lastly, it is possible to get a complete list of all annotation headings (and their types) for which PubChem has any data, and that can be used in URLs such as the above:

https://pubchem.ncbi.nlm.nih.gov/rest/pug/annotations/headings/JSON

Source Categories
PUG View can list all PubChem depositors and their SIDs for a given compound, including a categorization of each source – such as chemical vendor, research and development, journal publishers, etc.:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/categories/compound/1234/JSON

Literature
This will give URLs into PubMed for literature associated with a compound, organized by subheading:

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/literature/compound/1234/JSON

Biologics
This is used do display biologic images associated with compounds. The integer here is an internal identifier, which will be present in the primary compound record.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/image/biologic/243577/SVG

QR
This is a specialized image generator for QR codes that link to the LCSS page for a compound, intended for safety and hazard labelling.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/qr/short/compound/1234/SVG

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/qr/long/compound/1234/SVG

Linkout
This gives a listing of all the NCBI LinkOut records present for a substance, compound, or assay.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/linkout/compound/1234/JSON

PDB/MMDB Structures
This gives a listing of 3D protein structures associated with a compound. 

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/structure/compound/2244/JSON

Annotation Attachments
This is another specialized retrieval for attachments associated with some records, such as spectral images, etc. This key value will be present in the main record.

https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/key/236678_1

Limitations
Some users are often confused with PUG-View and PUG-REST.  While PUG-REST retrieves property values computed by PubChem, PUG-View retrieves annotations collected from other data sources. 

Contrary to PUG-REST, PUG-View takes only CID (rather than chemical names, InChIKeys or other identifiers). Therefore, to get annotations corresponding to non-CID identifiers, they need to be converted to CIDs first and then those CIDs should be used in PUG-View requests.

Another important difference between PUG-REST and PUG-View is that PUG-View cannot take multiple CIDs in a single request, whereas PUG-REST can. That is, of the following two PUG-View requests, only the first one will work:

(Correct) https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1/JSON?heading=Substances+by+Category

(Incorrect) https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/1,2,3/JSON?heading=Substances+by+Category



PUG SOAP
PUG SOAP is a web services access layer to PubChem functionality, and is an interface to PubChem’s specialized search and analysis services – chemical structure searches, full record downloads, etc. It is based on a WSDL which can be found at the URL:

https://pubchem.ncbi.nlm.nih.gov/pug_soap/pug_soap.cgi?wsdl

PubChem’s PUG (Power User Gateway) is an XML-based interface suitable for low-level programmatic access to PubChem services, wherein data is exchanged through a relatively complex XML schema that is powerful but requires some expertise to use. PUG SOAP contains much of the same functionality, but broken down into simpler functions defined in a WSDL (http://www.w3.org/TR/wsdl), using the SOAP protocol (http://www.w3.org/TR/soap) for information exchange. This WSDL/SOAP layer is most suitable for SOAP-aware GUI workflow applications (Taverna, Pipeline Pilot) and programming languages (C#/.NET, Perl, Python, Java, etc.). See the "Tips & Tricks" section at the end of this document for more information on specific clients.

We welcome feedback and suggestions; please direct these to NCBI’s help desk at info@ncbi.nlm.nih.gov.

Additional information of PUG SOAP can also be found in the following papers:

Kim S, Thiessen PA, Bolton EE, Bryant SH. PUG-SOAP and PUG-REST: web services for programmatic access to chemical information in PubChem. Nucleic Acids Res. 2015 Jul 1; 43(W1):W605-W611. doi: 10.1093/nar/gkv396.
[PubMed PMID: 25934803] [PubMed Central PMCID: PMC4489244] [Free Full Text]
PUG SOAP Concepts
Keys
In this interface, complex data objects like chemical structures and lists of PubChem database identifiers are abstracted in what PUG SOAP calls “keys.” These are arbitrary strings that can easily be passed back and forth between the PUG SOAP server and client applications, reducing both the complexity and volume of data transferred over the network.

For example, when a SMILES or SDF structure is provided as initial input, PUG SOAP will return a “structure key” that can be used in subsequent functions that take a chemical structure as their starting point – like a substructure search or a standardization request. Similarly, functions that are used to specify a BioAssay table will return an “assay key.”

Sets of PubChem database identifiers (SIDs, CIDs, or AIDs) are contained in a “list key.” So for example, a similarity search (which takes a structure key as input) will return a list key as output. From there, one may use this list key to retrieve the actual identifiers, to download structures, to show the result set in Entrez, to limit the search space of subsequent queries, etc.

PubChem BioAssay, Substance, and Compound downloads produce a “download key” that may be used to obtain a URL from which the desired records may be obtained.

Queued (Asynchronous) Operations
Many functions in PUG SOAP are run on dedicated servers shared by the entire PubChem community, on which jobs run on a first come first serve queue and may take some time to complete. The key that such a function returns must be used with a status check function, to make sure that the request has been completed before proceeding to the next step. The user’s application is responsible for periodically polling the status function, moving on only when success is achieved, or halting if an error status is returned.

Examples of how to do this polling within many common SOAP clients are provided later in this document.

PUG SOAP Functions
This section describes the functions available through the PUG SOAP WSDL, their inputs and outputs, and whether they are synchronous or asynchronous. Synchronous here means that the function returns a result right away. Asynchronous means that the operation is queued, that the status check function (GetOperationStatus) must be used with the returned key, and further operations on that key must not be performed until the check indicates success.

This document provides a general description of what each function does. For details on the SOAP messages, XML schema types, enumerations, etc., see the automatically generated (and highly detailed!) documentation:

https://pubchem.ncbi.nlm.nih.gov/docs/pug-soap-reference

The functions below are listed alphabetically. One may also organize them by classifying into three categories: input, processing, and output. Input functions are the starting points, where the user provides structures and ID lists for further operations. Processing functions perform some complex calculation on PubChem’s computational infrastructure.  Output functions are used to retrieve the results of the processing. By design, the input functions all begin with “Input” and are synchronous.  Processing functions may have any name, and are asynchronous. Output functions begin with “Get” and are synchronous.

AssayDownload
Given an assay key, prepare for download a file containing an assay data table in the selected format. See the assay query section of the PUG service documentation for more detail on the supported formats. Compression is optional and defaults to gzip (.gz). Returns a download key. Asynchronous.

Download
Given a list key, prepare for download a file containing those records in the selected format. See the documentation on downloads for more details on the supported formats and file types. Returns a download key. Asynchronous.

GetAssayColumnDescription
Get the description of column (readout) in a BioAssay, which may be the outcome, score, or a TID from the given AID. Synchronous.

GetAssayColumnDescriptions
Get the description of all columns (readouts) in a BioAssay. Synchronous.

GetAssayDescription
Get the descriptive information for a BioAssay, including the number of user-specified readouts (TIDs) and whether a score readout is present. Optionally get version information. Synchronous.

GetDownloadUrl
Given a download key, return an FTP URL that may be used to download the requested file. Synchronous.

GetEntrezKey
Given a list key, return an Entrez history key (db, query key, and WebEnv) corresponding to that list. Synchronous.

GetEntrezUrl
Given an Entrez history key (db, query key, and WebEnv), return an HTTP URL that may be used to view the list in Entrez. Synchronous.

GetIDList
Given a list key, return the identifiers as an array of integers. Note that this method expects there to be at least one identifier in the list, and will fault if the list is empty; see GetListItemsCount, which can be used to check for an empty list prior to calling GetIDList. The optional Start (zero-based) and Count parameters can be used to return smaller portions of the list, useful especially for large lists. Synchronous.

GetListItemsCount
Return the number of IDs in the set represented by the given list key. Synchronous.

GetOperationStatus
Given a key for any asynchronous operation, return the status of that operation. Possible return values are: Success, the operation completed normally; HitLimit, TimeLimit: the operation finished normally, but one of the limits was reached (e.g. before the entire database was searched); ServerError, InputError, DataError, Stopped: there was a problem with the input or on the server, and the job has died; Queued: the operation is waiting its turn in the public queue; Running: the operation is in progress. Synchronous.

GetStandardizedCID
Given a structure key that has been processed by Standardize, return the corresponding PubChem Compound database CID, or an empty value if the structure is not present in PubChem. Synchronous.

GetStandardizedStructure
Given a structure key that has been processed by Standardize, return the chemical structure in as SMILES or InChI strings. Synchronous.

GetStandardizedStructureBase64
Given a structure key that has been processed by Standardize, return the chemical structure as ASN, XML, or SDF, returned as a Base64-encoded string. Synchronous.

GetStatusMessage
Given a key for any asynchronous operation, return any system messages (error messages, job info, etc.) associated with the operation, if any. Synchronous.

IdentitySearch
Search PubChem Compound for structures identical to the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

IDExchange
Convert IDs from one type to another, using any one of a variety of CID matching algorithms. Output can be a list or a downloaded file; download file compression is optional and defaults to gzip (.gz). Returns a list or download key. Asynchronous.

InputAssay
Specify an assay table from a BioAssay AID. The table may be complete, concise, or include a ListKey-specified set of readouts (TIDs). By default, all tested substances are included, but can be restricted to a ListKey-specified set of SIDs or CIDs. Returns an assay key. Synchronous.

InputEntrez
Input an Entrez history key (db, query key, and WebEnv). Returns a list key. Synchronous.

InputList
Input a set of identifiers for a PubChem database, as an array of integers. Returns a list key. Synchronous.

InputListText
Input a set of identifiers for a PubChem database, as a simple string of integer values separated by commas and/or whitespace. Returns a list key. Synchronous.

InputStructure
Input a chemical structure as a simple (one-line) string, either SMILES or InChI. Returns a structure key. Synchronous.

InputStructureBase64
Input a chemical structure in ASN.1 (text or binary), XML, or SDF format. The structure must be encoded as a Base64 string. Currently only single structures are supported. Returns a structure key. Synchronous.

MFSearch
Search PubChem Compound for structures of a given molecular formula, optionally allowing elements not specified to be present. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

ScoreMatrix
Compute a matrix of scores from one or two lists of IDs (if one, the IDs will be self-scored), of the selected type and in the selected format. Compression is optional and defaults to gzip (.gz). Returns a download key. Asynchronous.

SimilaritySearch2D
Search PubChem Compound for structures similar to the one given by the structure key input, based on the given Tanimoto-based similarity score. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

Standardize
Standardize the structure given by the structure key input, using the same algorithm PubChem uses to construct the Compound database. Returns a structure key. Asynchronous.

SubstructureSearch
Search PubChem Compound for structures containing the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

SuperstructureSearch
Search PubChem Compound for structures contained within the one given by the structure key input, based on a user-selected level of chemical identity: connectivity only, match isotopes and/or stereo, etc. The search may be limited by elapsed time or number of records found, or restricted to search only within a previous result set (given by a list key). Returns a list key. Asynchronous.

PUG SOAP Client Examples, Tips, and Tricks
The standard WSDL/SOAP interface to PUG SOAP makes these web services functions generic and compatible with any SOAP client - in theory. In practice, we have found that the support for WSDL/SOAP among various clients is highly variable, each with different quirks and workarounds necessary to make them work with PUG SOAP. On our PUG SOAP client help web page:

https://pubchem.ncbi.nlm.nih.gov/pug_soap/client_help.html

we share some of our experiences and tricks for working with some common clients, which hopefully will help first time users get started.

We have made every effort to design PUG SOAP to work as broadly and generically as possible. But since the SOAP clients are out of PubChem’s control, we cannot guarantee that every version of every client will work the same way, or that any given client will be compatible. Please contact NCBI’s help desk at info@ncbi.nlm.nih.gov with any comments, suggestions, or questions. Provided we have access to the same client software, we will try to help with specific issues.

