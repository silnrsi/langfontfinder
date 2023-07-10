
# Results Structure

The returned result is a JSON object. The primary component of the result is a font family record. But the basic structure allows for multiple records to be returned. At its top level it has the fields:

| Field     | Value                                                             |
| :-------- | :---------------------------------------------------------------- |
| defaultfamily | An array of familyid values for the default result |
| roles     | \[opt\] An object whose keys are roles. The value for each role is a list of familyid values in preference order. |
| families  | An object in which each key is a familyid. The value for each key is the corresponding font record |
| apiversion | A semantic version number string for the file format. Currently “0.3” |

## Font family records

The metadata for a font family is in a *font family record* JSON object identified by *familyid*. The object contains the following fields, most of which are optional. Required fields are in bold:

| Field | Description |
| ----- | ----------- |
| altfamily | [opt] An alternative family name that may be used by Windows apps to refer to the font family in certain situations. If defined in the root of the record the family name applies to all fonts in the family. If a *files* field exists, then this field is ignored. This field is not used in current records but is here for completeness. *altfamily* information is normally found in individual *files* records. |
| defaults | [opt] A subobject indicating which *files* entries represent default fonts for the family. See *defaults* section below. |
| **distributable** | Boolean to indicate whether the font is likely to be freely distributable. |
| fallback | [opt] A *familyid* for an alternative font family to use instead. Two common cases of this are 1) when the font family is not distributable (e.g. Microsoft system fonts) or 2) if the font family is deprecated. |
| **family** | Common family name as seen by users, which may contain spaces (e.g. "Lisu Bosa"). Some Windows apps may display a different family name for individual members of a family in certain situations - see *altfamily*. |
| **familyid** | The unique identifier for the font family. |
| features | [opt] A CSS-style features string describing how the font features should be set to appropriately style text in this font for this language. This field is only returned by the [Language Font Finder (LFF)](https://github.com/silnrsi/langfontfinder) service, if at all, and is never present in the `families.json` file.
| files | [opt] A subobject containing information about individual font files in the package. The object is keyed by filename with its own object of information.  See *files* section below. |
| googlefonts | [opt] This subobject contains information on how to access the font family via the Google Fonts service. See *defaults* section below. *This field is not used in current records pending further discussion.* |
| license | [opt] The name of the font license, if known (MIT, OFL, GPL-FE, etc.). This may instead indicate a type of license, such as "shareware" or "proprietary". |
| packageurl | [opt] URL for direct download of the complete font package, typically a .zip file. |
| siteurl | [opt] URL to a website where users can find out about the font package and download it. |
| source | [opt] The source of this font, if known, such as "SIL", "Google", "NLCI", "Microsoft", etc. |
| status | [opt] The current status of this font package: *current* (active), *archived* (no longer active), *deprecated* (another *familyid* is preferred). Defined for all SIL fonts, and others whose status is known. |
| version | [opt] The version of the font package being described. This is always current for SIL fonts. For non-SIL fonts the version number reflects the latest known version, although there may be updated versions available. |
| ziproot | [opt] The name of the folder created when a .zip package is decompressed. Used to form *zippath* fields in *files* records. |

### *default* subobjects

The *default* field is an object whose keys are font file types.

| Field | Description |
| ----- | ----------- |
| ttf | [opt] Key in *files* subobjects to the default TTF font file. |
| woff | [opt] Key in *files* subobjects to the default WOFF font file. |
| woff2 | [opt] Key in *files* subobjects to the default WOFF2 font file. |

### *files* subobjects

The *files* field is an object whose keys are filenames without any path. For each filename, there is an object of information with the following fields:

| Field | Description |
| ----- | ----------- |
| altfamily | [opt] An alternative family name if different from the *family* field in the main font family description. This is typically used by legacy RIBBI-only applications to provide access to multi-weight font families, particularly on Windows. |
| axes | [opt] A subobject keyed by font axis and a float value.  See *axes* section below. | 
| flourl | [opt] If the font file exists on FLO, this field gives the URL. |
| packagepath | [opt] The path to the font file inside the main *packageurl*, if defined. |
| url | [opt] A direct download URL to this font file, if available. |
| zippath | [opt] Most packages are distributed as a zip file with a top level directory within the zip. This field gives the complete path within the zip file to the font file (including that top level directory). |

### *axes* subobjects

The *axes* field within *files* records is a subobject whose keys are four-letter axis identifiers. There are [five standard registered axes](https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg) although custom axes can be defined. The keys and their values identify a single style contained in a font family (e.g. Bold Italic). SIL fonts typically define styles using only these two axes:

| Field | Description |
| ----- | ----------- |
| ital | [opt] 0 for upright, 1 for italic. |
| wght | [opt] Font weight. This is a number between 0 and 999. Each multiple of 100 signifies an industry-standard weight name from 100 to 900: Thin, ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold, Black. |

For example, the normal Regular weight of a font family will always be indicated by `{ "ital": 0 "wght": 400.0 }` and the Bold Italic by `{ "ital": 1, "wght": 700.0 }`.

### *googlefonts* subobjects

The *googlefonts* field will contain information on how to access the fonts via the Google Fonts service. *Currently undefined pending further discussion.*
