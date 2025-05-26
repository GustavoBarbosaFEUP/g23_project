from werkzeug.utils import secure_filename
import os

prev_option = ""
img = ""

def designerFotoform(app, cname=''):
    global img
    global prev_option

    cl = app.get_class(cname or "Designer")

    if prev_option == 'insert' and app.request.form['option'] == 'save':
        if cl.auto_number == 1:
            strobj = "None"
        else:
            file = app.request.files['img']
            filename = secure_filename(file.filename)
            foto = filename
            if foto != "":
                file.save(os.path.join(app.config['UPLOAD'], filename))
            else:
                foto = ""
            
            strobj = app.request.form[cl.att[0]]
            for i in range(1, len(cl.att)):
                if cl.att[i] == 'foto':
                    strobj += "#" + foto
                else:
                    strobj += "#" + app.request.form[cl.att[i]]

            obj = cl.from_string(strobj)
            cl.insert(getattr(obj, cl.att[0]))
            cl.last()
    elif app.request.form['option'] == 'edit':
        file = app.request.files['img']
        filename = secure_filename(file.filename)
        foto = filename
        if foto != "":
            file.save(os.path.join(app.config['UPLOAD'], filename))
            app.current_obj.foto = foto

    prev_option = app.request.form['option']
    return app.render_template(f"{cname.lower()}_foto.html", cl=cl)
