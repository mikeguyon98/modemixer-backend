from io import BytesIO
import markdown
import pdfkit
import boto3
import os

def markdown_dict_to_pdf(markdown_dict, sections):
    html_content = "<h1>TECHPACK</h1>"
    for section in sections:
        md_text = markdown_dict.get(section, "")
        html_section = markdown.markdown(md_text)
        html_content += f"<h1>{section}</h1>{html_section}<hr/>"
    
    # Create a BytesIO object to write the PDF to memory
    pdf_output = BytesIO()

    # Generate PDF and write directly to BytesIO object
    pdf_data = pdfkit.from_string(html_content, output_path=False)  # This will return PDF data as bytes
    pdf_output.write(pdf_data)  # Write the PDF data to BytesIO object
    pdf_output.seek(0)  # Rewind the buffer to the beginning for future read

    return pdf_output


def upload_pdf_to_s3(pdf_byte_stream, bucket_name, file_name):
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    s3 = session.client("s3")
    
    try:
        # Ensure the stream is at the beginning
        pdf_byte_stream.seek(0)
        s3.upload_fileobj(pdf_byte_stream, bucket_name, file_name)
        print(f"Successfully uploaded {file_name} to S3 bucket {bucket_name}")
        # Generate the public URL for the uploaded PDF
        public_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return public_url
    except Exception as e:
        print(f"Failed to upload {file_name}: {e}")
        return None
