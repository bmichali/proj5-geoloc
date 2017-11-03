
import flask
import config
import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
app.token = CONFIG.TOKEN
markers = CONFIG.MARKERS

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    flask.g.api_token = app.token
    app.logger.debug("Main page entry")
    return flask.render_template('geoloc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

# process markers, send to HTML
@app.route("/_marker_list")
def _marker_list():
    """
    grab locations from text file,
    including name, lat and lng
    """
    app.logger.debug("Marker List")
    locations = open(markers)
    result = []
    for line in locations:
        if line[0] is not "#":
            app.logger.debug("added: " + line)
            result.append(line.split("|"))

    locations.close()
    app.logger.debug("sent locations")
    return flask.jsonify(result=result)

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
