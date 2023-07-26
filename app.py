import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import psycopg2

# Replace the following with your actual database credentials
DB_HOST = '127.0.0.1'
DB_NAME = 'blog'
DB_USER = 'postgres'
DB_PASSWORD = 'Y@229471'

connection = psycopg2.connect(
    host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
)

class BlogPostHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html") 

    def get(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM blog_posts ORDER BY id DESC")
        blog_posts = cursor.fetchall()
        cursor.close()

        self.render("index.html", blog_posts=blog_posts)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        try:
            data = tornado.escape.json_decode(message)
            title = data["title"]
            author = data["author"]
            content = data["content"]

            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO blog_posts (title, author, content) VALUES (%s, %s, %s)",
                (title, author, content),
            )
            connection.commit()
            cursor.close()

        except Exception as e:
            print("Error:", e)
    

def make_app():
    return tornado.web.Application(
        [
            (r"/", BlogPostHandler),
            (r"/websocket", WebSocketHandler),
        ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
