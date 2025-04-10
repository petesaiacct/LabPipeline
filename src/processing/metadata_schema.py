# This dictionary defines the extensible metadata schema for our lab's knowledge base.
# Each key in the dictionary represents a top-level category of information (e.g., 'general', 'data_status').
# The value associated with each key is another dictionary containing the specific metadata fields
# relevant to that category. Each metadata field is further described with a 'description'
# and optionally, 'data_type' and 'allowed_values' to provide more context and constraints.

metadata_schema = {
    'general': {
        'InLab': {
            'description': 'Indicates if the item originated within our lab.',
            'data_type': 'boolean',
            'allowed_values': [True, False]
        },
        'Submitter/Logger': {
            'description': 'Name or unique identifier of the person who initially added the item.',
            'data_type': 'string'
        },
        'Submission Date': {
            'description': 'Date and time when the item was initially added (YYYY-MM-DD HH:MM:SS).',
            'data_type': 'datetime'
        },
        'Last Updated By': {
            'description': 'Name or unique identifier of the person who last modified the item.',
            'data_type': 'string'
        },
        'Last Updated Date': {
            'description': 'Date and time when the item was last modified (YYYY-MM-DD HH:MM:SS).',
            'data_type': 'datetime'
        },
        'Keywords': {
            'description': 'Relevant keywords or tags associated with the item.',
            'data_type': 'list of strings'
        },
        # You can add more general fields here as needed
        'Notes': {
            'description': 'General notes or comments about the item.',
            'data_type': 'string'
        }
    },
    'data_status': {
        'Data Status': {
            'description': 'The current processing status of the data.',
            'data_type': 'string',
            'allowed_values': ['Raw Data', 'Cleaned Data', 'Analyzed Data', 'Processed Data', 'Validated Data', 'Archived Data', 'Obsolete Data']
        },
        # Add more data-specific status fields if necessary
        'Data Format': {
            'description': 'The format of the data file (e.g., CSV, TXT, HDF5).',
            'data_type': 'string'
        },
        'File Size (MB)': {
            'description': 'The size of the data file in megabytes.',
            'data_type': 'float'
        }
    },
    'publication_status': {
        'Type': {
            'description': 'The type of publication or paper.',
            'data_type': 'string',
            'allowed_values': ['Unpublished Paper', 'Paper Under Review', 'Published Paper', 'Pre-print', 'Paper in Revision', 'Rejected Paper']
        },
        'Author(s)': {
            'description': 'List of authors of the publication.',
            'data_type': 'list of strings'
        },
        'Draft #': {
            'description': 'The draft number for unpublished papers.',
            'data_type': 'integer',
            'condition': 'Only applicable if Type is "Unpublished Paper"'
        },
        'Journal/Conference': {
            'description': 'Name of the journal or conference for submitted/published papers.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Paper Under Review" or "Published Paper"'
        },
        'Submission Date': {
            'description': 'Date of submission to the journal/conference (YYYY-MM-DD).',
            'data_type': 'date',
            'condition': 'Only applicable if Type is "Paper Under Review"'
        },
        'Review Status': {
            'description': 'Current status in the review process.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Paper Under Review"',
            'allowed_values': ['Awaiting Decision', 'Revision Requested', 'Under Review', 'Minor Revision', 'Major Revision']
        },
        'Publication Date': {
            'description': 'Date of publication (YYYY-MM-DD).',
            'data_type': 'date',
            'condition': 'Only applicable if Type is "Published Paper"'
        },
        'DOI': {
            'description': 'Digital Object Identifier of the published paper.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Published Paper"'
        },
        'Volume': {
            'description': 'Volume number of the publication.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Published Paper"'
        },
        'Issue': {
            'description': 'Issue number of the publication.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Published Paper"'
        },
        'Pages': {
            'description': 'Page numbers of the publication.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Published Paper"'
        },
        'Pre-print Server': {
            'description': 'Platform hosting the pre-print.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Pre-print"'
        },
        'Pre-print DOI/Identifier': {
            'description': 'Identifier of the pre-print.',
            'data_type': 'string',
            'condition': 'Only applicable if Type is "Pre-print"'
        },
        'Revision Round': {
            'description': 'The current revision round number.',
            'data_type': 'integer',
            'condition': 'Only applicable if Type is "Paper in Revision"'
        }
    },
    'research_status': {
        'Research Type': {
            'description': 'The type of research activity.',
            'data_type': 'string',
            'allowed_values': ['Experiment Proposal', 'Active Experiment', 'Completed Experiment', 'On Hold', 'Terminated', 'Pilot Study', 'Main Study', 'Follow-up Study']
        },
        'Approval Status': {
            'description': 'The approval status of the experiment proposal.',
            'data_type': 'string',
            'allowed_values': ['Approved', 'Pending', 'Rejected'],
            'condition': 'Only applicable if Research Type is "Experiment Proposal"'
        },
        'Start Date': {
            'description': 'The start date of the experiment (YYYY-MM-DD).',
            'data_type': 'date',
            'condition': 'Only applicable if Research Type is "Active Experiment" or "Completed Experiment"'
        },
        'End Date': {
            'description': 'The end date of the experiment (YYYY-MM-DD).',
            'data_type': 'date',
            'condition': 'Only applicable if Research Type is "Completed Experiment"'
        },
        # Add more research-specific fields
        'Experimental Goal': {
            'description': 'A brief description of the experiment\'s objective.',
            'data_type': 'string',
            'condition': 'Only applicable if Research Type is "Active Experiment" or "Completed Experiment"'
        }
    },
    'note_type': {
        'Note Category': {
            'description': 'The category of the note or record.',
            'data_type': 'string',
            'allowed_values': ['Raw Notes', 'Experiment Notes', 'Lab Meeting Notes', 'Protocol Document', 'Analysis Log', 'Software/Tool Documentation', 'Grant Proposal', 'Ethics Approval']
        },
        # Add fields specific to note types if needed
        'Meeting Date': {
            'description': 'Date of the lab meeting.',
            'data_type': 'date',
            'condition': 'Only applicable if Note Category is "Lab Meeting Notes"'
        },
        'Protocol Version': {
            'description': 'Version number of the protocol.',
            'data_type': 'string',
            'condition': 'Only applicable if Note Category is "Protocol Document"'
        }
    },
    # You can add more top-level categories as your needs evolve (e.g., 'software', 'equipment')
}

# Explanation for Reviewers:
#
# This 'metadata_schema' dictionary provides a structured way to define and organize
# the metadata associated with various items in our lab's knowledge base (data, papers, notes, etc.).
#
# Top-Level Keys:
#   - Each top-level key (e.g., 'general', 'data_status', 'publication_status') represents a broad
#     category of metadata. This helps in logically grouping related fields. You can extend this
#     by adding new top-level categories as needed (e.g., for software, equipment, etc.).
#
# Second-Level Keys (Metadata Fields):
#   - Within each top-level category, the keys represent specific metadata fields (e.g., 'InLab',
#     'Data Status', 'Journal/Conference'). These are the actual attributes we want to record
#     for each item.
#
# Third-Level Dictionary (Field Properties):
#   - Each metadata field is described by a dictionary containing the following keys:
#     - 'description': A human-readable explanation of what this field represents. This is crucial
#       for users to understand the purpose of each metadata element.
#     - 'data_type' (optional): Specifies the expected data type for this field (e.g., 'string',
#       'integer', 'boolean', 'date', 'datetime', 'list of strings', 'float'). This helps in
#       data validation and ensures consistency.
#     - 'allowed_values' (optional): For fields with a limited set of valid entries, this list
#       specifies the permissible values. This enforces standardization and reduces errors.
#     - 'condition' (optional): Explains when a particular metadata field is applicable. This helps
#       in understanding the context of the field and avoids confusion when it's not relevant
#       for certain types of items.
#
# Extensibility:
#   - To add new metadata fields, simply add a new key-value pair within the appropriate
#     top-level category. The key will be the name of the new field, and the value will be
#     a dictionary describing the field (description, data_type, allowed_values, condition).
#   - You can also add entirely new top-level categories if your knowledge base needs to track
#     different types of information.
#
# How to Use in Python Code:
#   - You can import this 'metadata_schema' dictionary into your Python scripts.
#   - When processing or creating metadata for an item, you can refer to this schema to understand
#     the available fields, their descriptions, and expected data types.
#   - You can use this schema to guide the creation of your data structures in the vector database.
#   - For querying, users can refer to this schema to understand the available metadata fields they
#     can filter or search by.
#
# Analogy to MAN Pages:
#   - This 'metadata_schema' serves a similar purpose to MAN pages in Unix/Linux. It provides
#     documentation about the structure and meaning of the metadata fields you will be using.
#   - Your Python code can potentially be extended to read this schema and present it to users
#     in a more user-friendly format if they need to understand the available metadata.

# Example of how you might use this schema in your Python code:
#
# def create_metadata_entry(item_type, data):
#     metadata = {}
#     schema_section = {}
#     if item_type == 'data':
#         schema_section = metadata_schema['general'].copy()
#         schema_section.update(metadata_schema['data_status'])
#     elif item_type == 'paper':
#         schema_section = metadata_schema['general'].copy()
#         schema_section.update(metadata_schema['publication_status'])
#     # ... add other item type mappings
#
#     for field, details in schema_section.items():
#         if field in data:
#             metadata[field] = data[field]
#         # You might add error checking here to ensure required fields are present
#     return metadata
#
# example_data = {
#     'InLab': True,
#     'Submitter/Logger': 'John Doe',
#     'Submission Date': '2025-04-10 16:15:00',
#     'Data Status': 'Raw Data',
#     'Data Format': 'CSV'
# }
#
# data_metadata = create_metadata_entry('data', example_data)
# print(data_metadata)