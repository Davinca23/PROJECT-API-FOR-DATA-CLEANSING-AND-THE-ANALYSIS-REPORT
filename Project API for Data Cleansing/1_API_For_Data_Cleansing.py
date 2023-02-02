import re
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


app = Flask(__name__)
app.config["DEBUG"]=True

app.json_encoder = LazyJSONEncoder
swag_template = dict(
info = {
    'title':LazyString(lambda: 'API Documentation for Data Processing and Modelling'),
    'version':LazyString(lambda:'1.0.0'),
    'description':LazyString(lambda: 'Dokumentasi API untuk Data dan Modelling'),
},
host = LazyString(lambda: request.host)

)

swagger_config = {
    "headers":[],
    "specs":[
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swag_template, config=swagger_config)



def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'docs', 'xlsx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanse_file(contents):
    contents = contents.decode('utf-8')
    contents = re.sub(r'[0-9]+', '', contents)
    contents = re.sub(r'[\,]+', "", contents)
    contents = re.sub(r'[\-]{1,}', "", contents)
    contents = re.sub(r'(\.)(.*)', "", contents)
    contents = re.sub(r'(\\x)(.*)', "", contents)
    contents = re.sub(r'(\:)(.*)', "", contents)
    contents = re.sub(r'(\; )(.*)', "", contents)
    contents = re.sub(r'(â)(.*)', "", contents)
    contents = re.sub(r'(ð)(.*)', "", contents)
    contents = re.sub(r'(user)', "", contents)
    contents = re.sub(r'(\")+', "", contents)
    contents = re.sub(r'(\')+', "", contents)
    contents = re.sub(r'(\|)+', "", contents)
    contents = re.sub(r'(\\n)+', "", contents) 
    contents = re.sub(r'[\=]+', "", contents)
    contents = re.sub(r'(bego|tolol|idiot|anjing|monyet|bangsat|bodoh|tai|homo|jancuk|lonte|gembrot|kntl|mampus|dungu|biadab|babi|pengecut|setan!|memek|kontol|mnyt|ngewe|kampret|ngentot|bloon|bangke|bacot)',r'XXX',contents)
    contents = re.sub(r'(gendut|gembrot|kurus|ceking|babon|cungkring|autis|bencong)',r'YYY',contents)
    contents = contents.lower()
    contents = contents.split('\n')
    contents = [line for line in contents if line.strip() != '']
    df = pd.DataFrame(contents)
    df = df.applymap(lambda x: x.strip())
    df = df.dropna()
    df.to_csv('cleaned_file.csv')
    return df

@swag_from("docs/user.yml", methods=['GET','POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            contents = file.read()
            df = cleanse_file(contents)
            return render_template('cleansed_file.html', data=df.to_html())
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def cleanse_text(text):
    #text = text.decode('utf-8')
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub(r'[\,]+', "", text)
    text = re.sub(r'[\-]{1,}', "", text)
    text = re.sub(r'(\[|\])', "", text)
    text = re.sub(r'(\")+', "", text)
    text = re.sub(r'(\')+', "", text)
    text = re.sub(r'(\\n)+', "", text) 
    text = re.sub(r'[\=]+', "", text)
    text = text.capitalize()
    text = text.split('\n')
    text = [line for line in text if line.strip() != '']
    return text

@swag_from("docs/user.yml", methods=['GET','POST'])
@app.route('/text', methods=['GET', 'POST'])
@app.route('/text', methods=['GET', 'POST'])
def upload_text():
    if request.method == 'POST':
        try:
            text = request.form['text']
        except KeyError:
            return 'Error: No text field in form data.'
        cleansed_text = cleanse_text(text)
        return render_template('cleansed_text.html', data=cleansed_text)
    
    return '''
    <!doctype html>
    <title>Submit Text</title>
    <h1>Submit Text</h1>
    <form method="POST">
        <label for="text">Enter text to cleanse:</label><br>
        <textarea id="text" name="text"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    '''

    
if __name__ == '__main__':
    app.run(debug= True,port=9876)

app.run()
