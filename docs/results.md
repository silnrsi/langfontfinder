
# Results Structure

The returned result is a JSON object. The primary component of the result is a font record. But the basic structure allows for multiple records to be returned. At its top level it has the fields:

| Field     | Value                                                             |
| --------- | ----------------------------------------------------------------- |
| defaultfamily | An array of familyid values for the default result |
| roles     | \[opt\] An object whose keys are roles. The value for each role is a list of familyid values in preference order. |
| families  | An object in which each key is a familyid. The value for each key is the corresponding font record |
| apiversion | A semantic version number string for the file format. Currently “0.3” |

## Family Record

A family record has the following JSON object structure:

| Field     | Description                                                     |
| --------- | --------------------------------------------------------------- |
| familyid  | A unique identifier for the font family described in this object. This may be used by a font service to access information on the font. |
| fallback  | \[opt\] A font family id for an alternative font family to use. This is often used if there is no defaultttf, etc. due to, say, copyright reasons. Also used when a family is deprecated to indicate which family to use instead. |
| family    | Common family name, however Windows ID1 may differ for non-RIBBI weights (see Files structure later) |
| altfamily | \[opt\] This alternative family name applies to all fonts in the family in some situations. If a files field exists, then this field is ignored. See the corresponding field in the files structure below. |
| siteurl   | \[opt\] URL to product site where users can find out about the font package and download it. |
| packageurl | \[opt\] URL for direct download of the font package. |
| files     | \[opt\] A sub object containing information about font files in the package. The object is keyed by filename with its own object of information. The object structure is described later. |
| defaults  | \[opt\] A sub object containing files entries to use by default |
| version   | \[opt\] The version of the font package being described. |
| status    | \[opt\] The current status of this font package: current (active), archived (no longer active), deprecated (another fontFamilyID is preferred). Will be defined for all SIL fonts, and others whose status is known. |
| license   | \[opt\] The name of the font license, if known (MIT, OFL, GPL-FE, etc.). If the font license is proprietary this will be ‘proprietary’. |
| distributable | Boolean to indicate whether the font is likely to be freely distributable. |
| source    | \[opt\] The source of this font, if known: SIL, Google, NLCI, Microsoft, etc. The list of values is an open set and so may take any value beyond those listed later. (see below) |
| googlefonts | \[opt\] This sub object contains information on how to access the font family via Google Fonts. The structure of the object is described below. |
| features  | \[opt\] \[FAF\] A CSS-style features string describing how the font features should be set to appropriately style text in this font for this language. This field is not found in families.json as it is language-specific and only available through the API. |

### Files Structure

The files field is an object whose keys are filenames without any path. For each filename, there is an object of information with the following fields:

| Field     | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| altfamily | \[opt\] An alternative family name if different from the family field in the main font family description. This is typically used by legacy RIBBI-only applications to provide access to multi-weight font families, particularly on Windows. |
| url       | \[opt\] A direct download URL to this font file |
| flourl    | \[opt\] If the font file exists on FLO, this field gives the URL. |
| packagepath | \[opt\] Gives the path to the font file inside the font package (see main package field) |
| zippath   | \[opt\] Most packages are distributed as a zip file with a top level directory within the zip. This field gives the complete path within the zip file to the font file (including that top level directory) |
| axes      | \[opt\] An object keyed by font axis and a float value. |

The rest of the fields in a font file axes object have exactly 4 letter keys and are considered axes for accessing a particular font instance in a multidimensional font family. The value is a number, often a float. For example, a font family may have a weight dimension, an italic dimension and even a width dimension. Some common axis identifiers are listed here. They all follow CSS conventions.

The axes object may take any 4 letter key. Common ones are:

| Dimension | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| wght      | \[opt\] Font weight. This is a number between 0 and 999. Each multiple of 100 signifies an industry-standard weight name from 100 to 900: Thin, ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold, Black. |
| ital      | \[opt\] 0 for upright, 1 for italic. |

### Defaults

There are various default files entries:

| Field     | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| ttf       | \[opt\] Key in files to the default TTF font file. |
| woff      | \[opt\] Key in files to the default WOFF font file. |
| woff2     | \[opt\] Key in files to the default WOFF2 font file. |

### Source

The source field is used by the font production team for the management of families.json.

While the source field may take any value, the following values are recognised as having potentially useful meaning:

| Value     | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| Google    | Font is free/open and is available through the Google Fonts service |
| Microsoft | Font is not freely available and cannot be redistributed. It may be available on Microsoft OSes or through MS Office distributions. |
| NLCI      | Font is free/open and maintained on behalf of New Life Computer Institute |
| SIL       | Font is free/open and maintained by SIL |

### Googlefonts Structure

The googlefonts field is a sub object containing these fields: (note that this is extremely preliminary and may change considerably)

| Field     | Parameter                                                         |
| --------- | ----------------------------------------------------------------- |
| defaulthref | href for the single default face |
| fullhref  | href for the full set of fonts |
| version   | The version that is currently in Google Fonts |
| notes     | Special information on usage, limitations, known issues |







