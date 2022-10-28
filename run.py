from kollekt import create_app
from dev_script import fill_db, delete_db
from kollekt.Components.Collection import CollectionItem

delete_db()
app = create_app()

if __name__ == '__main__':
    app.run(debug=1)

    @app.route('/')
    def test1():
        item1 = CollectionItem('jim', 'shoes', 'none', 'images/bantest.png', 'this is my shoe', 'public')
        return item1.get_text()
