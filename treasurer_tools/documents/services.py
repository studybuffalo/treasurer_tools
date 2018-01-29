"""Functions to handle upload of attachment files"""
import magic

"""Process Planning

- User uploads all their files (various file types)
- If any items fail to upload or are invalid format, inform user

- The treasurer will review the claim
  - Convert all the uploaded files into a single PDF for review
  - Notify treasurer of any files causing issue (can try to manually fix or contact user)
  - Allow treasurer to edit PDF (separate functionality)
    - Treasurer to upload new pages as needed
    - Treasuer can move any pages around or delete pages
    - Saves entire document as a new PDF
  - Treasurer can save a final version of the PDF
"""
def invalid_file_type_message(file):
    """Generates an error message for an invalid file type"""
    return (
        "The provided attachment is a {} file. Please provide a supported "
        "attachment".format(file)
    )

def check_pypdf2_pdf(file):
    """Checks if this is a workable pdf"""
    return file

def convert_gif(file):
    """Converts gif to workable PDF"""
    return file

def convert_jpeg(file):
    """Converts jpeg to workable PDF"""
    return file

def convert_png(file):
    """Converts png to workable PDF"""
    return file

def convert_tiff(file):
    """Converts tiff to workable PDF"""
    return file

def convert_doc(file):
    """Converts word document to workable PDF"""
    return file

def convert_odt(file):
    """Converts speadsheet to workable PDF"""
    return file

def organize_file_conversion(files):
    """Method to sort file uploads into proper conversion functions"""
    converted_files = []
    user_messages = []

    for file in files:
        # Get filetype MIME
        file_type = magic.from_file(file, mime=True)

        # Send file to proper conversion function
        if file_type == "application/pdf":
            converted_file = check_pypdf2_pdf(file)
        elif file_type == "image/gif":
            converted_file = convert_gif(file)
        elif file_type == "image/jpeg":
            converted_file = convert_jpeg(file)
        elif file_type == "image/png":
            converted_file = convert_png(file)
        elif file_type == "image/tiff":
            converted_file = convert_tiff(file)
        elif file_type == "application/msword":
            converted_file = convert_doc(file)
        elif file_type == "application/vnd.oasis.opendocument.text":
            converted_file = convert_odt(file)
        else:
            user_messages.append(invalid_file_type_message(file))

        if converted_file.success:
            converted_files.append(converted_file.file)
        else:
            user_messages.append(converted_file.message)
