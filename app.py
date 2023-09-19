import dash
# from jupyter_dash import JupyterDash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import base64
import os
import datetime

app = dash.Dash(
    __name__, 
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap",
    ],
    title="ChartGPT",
    update_title="ChartGPT | Loading...",
    assets_folder="assets",
    include_assets_files=True,
)

app.layout = html.Div([
    dcc.Upload(
        id='upload-pdf',
        children=html.Button('Upload PDF File'),
        multiple=False  # Allow only one file to be uploaded at a time
    ),
    html.Div(id='output-message')
])

# Define the directory where you want to save the uploaded PDF files
upload_dir = 'uploaded_pdfs/'

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

@app.callback(
    Output('output-message', 'children'),
    Input('upload-pdf', 'contents'),
    State('upload-pdf', 'filename'),
)
def save_uploaded_pdf(contents, file_name):
    if contents is None:
        return html.Div('No file uploaded.')

    try:
        # Extract the file name from the content string
        _, content_string = contents.split(',')
#         file_name = 'uploaded_file.pdf'  # You can customize the file name if needed
        file_path = os.path.join(upload_dir, file_name)

        # Decode and save the uploaded PDF as binary data
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(content_string))

        # Check if the saved file exists
        if os.path.exists(file_path):
            return html.Div(f'Successfully saved the file as {file_path}')
        else:
            return html.Div(f'Error: Failed to save the file.')

    except Exception as e:
        return html.Div(f'Error: {str(e)}')
if __name__ == '__main__':
    app.run_server(debug=True)
