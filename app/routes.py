from app import app

@app.route('/')
@app.route('/index')
def index():
	from datetime import datetime
	the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

	return """
	<h1>Oh hai world</h1>
	<p>It is currently {time}.</p>

	<img src="http://loremflickr.com/600/400">
	""".format(time=the_time)

    #return "Oh hai world"