from kollekt import create_app
from dev_script import fill_db, delete_db
from kollekt.Components.Collection import CollectionItem

delete_db()
app = create_app()

if __name__ == '__main__':
    app.run(debug=1)

