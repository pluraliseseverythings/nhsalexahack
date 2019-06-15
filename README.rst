Hello World with Flask
======================

In this tutorial, you will create a web app and deploy it to Heroku. You will use a Flask create the app. You'll first run the app locally, and then deploy it to Heroku using git.

Prerequisites
-------------

* Create an account on [heroku.com](https://api.heroku.com/signup)
* Install the `heroku` command-line client (Appendix A)
* Installing git and Setting up an SSH Key (Appendix B)
* Ensure your Python environment is setup

  * `Getting Setup with Python <http://www.craigkerstiens.com/2011/10/27/gettingsetupwithpython/>`_
  * `Installing Python Packages <http://www.craigkerstiens.com/2011/11/01/installingpythonpackages/>`_


Step 1: Create a Web App
------------------------

1. Create and load your virtualenv::

	virtualenv --no-site-packages venv 
	source venv/bin/activate


2. Create your application in app.py::

	import os
	from flask import Flask
	app = Flask(__name__)

	@app.route("/")
	def hello():
		return "Hello from Python!"

	if __name__ == "__main__":
		port = int(os.environ.get("PORT", 5000))
		app.run(host='0.0.0.0', port=port)


Step 2: Test the App Locally
----------------------------
	
1. Run your application locally::

	python app.py
	

2. You should be able to navigate in your browser to `http://localhost:5000' <http://localhost:5000/>`_ to view your hello world application. You'll notice for Flask the one unique portion is to attempt to read the port variable if it exists, this is to enable Heroku to know which port to listen to. 

3. Press `CTRL-C` to stop the process.

You are now ready to deploy this simple Python/Flask web app to Heroku.

Step 3: Deploy the Web App to Heroku
------------------------------------

1. In the project directory, create a new file named Procfile containing::

	web: python app.py


Note: The file names, directories, and code are case sensitive. The Procfile file name must begin with an uppercase "P" character.

Caution: Some text editors on Windows, such as Notepad, automatically append a .txt file extension to saved files. If that happens, you must remove the file extension.

`Procfile` is a mechanism for declaring what commands are started when your dynos are run on the Heroku platform.  In this case, we want Heroku to run the webapp startup script for web dynos.

2. Initialize a local git repository, add the files to it, and commit them::

	git init
	git add .
	git commit -m "initial commit for helloheroku"

Note: On Windows, you can ignore the following message when running the “git add .” command::

	warning : LF will be replaced by CRLF in .gitignore

The commit operation has output similar to the following::

	[master (root-commit) b914eee] initial commit
	7 files changed, 165 insertions(+), 0 deletions(-)
	create mode 100644 .gitignore
	create mode 100644 Procfile
	create mode 100644 app.py


3. Create a new app provisioning stack on Heroku by using the `heroku` command-line client:

    heroku create --stack cedar

Note: You must use the "cedar" stack when creating this new app because it’s the only Heroku stack that supports Python.

The output looks similar to the following:

    Creating empty-winter-343... done, stack is cedar
    http://empty-winter-343.herokuapp.com/ | git@heroku.com:empty-winter-343.git
    Git remote heroku added

Note: `empty-winter-343` is a randomly generated temporary name for the app. You can rename the app with any unique and valid name using the `heroku apps:rename` command.

    The create command outputs the web URL and git URL for this app. Since you had already created a git repository for this app, the heroku client automatically added the heroku remote repository information to the git configuration.

4. Deploy the app to Heroku:

	git push heroku master

This command instructs `git` to push the app to the master branch on the heroku remote repository. This automatically triggers a Maven build on Heroku. When the build finishes, the output ends with something like the following:

	----->Discovering process types
    Procfile declares types -> web
    -----> Compiled slug size is 17.0MB
    -----> Launching... done, v6
    http://empty-winter-343.herokuapp.com deployed to Heroku
    To git@heroku.com:empty-winter-343.git
    + 3bcf805...a72152c master -> master (forced update)

5. Verify that the output contains the message::

	Procfile declares types -> web

If it doesn't, confirm that the `Procfile` is named correctly with no file extension and that it contains::

	web: sh target/bin/webapp

If you fix `Procfile`, deploy the changes to Heroku::

	git add Procfile
    git commit -m "fixed Procfile"
    git push heroku master
    heroku scale web=1

6. Open the app in your browser using the generated app URL or by running::

	heroku open

You should see `hello, world` on the web page.


Step 4: Scale the App on Heroku
-------------------------------

By default, the app runs on one dyno. To add more dynos, use the `heroku scale` command.

1. Scale the app to two dynos::

    heroku scale web=2

2. See a list of your processes::

    heroku ps

Tip: This command is very useful as a troubleshooting tool. For example, if your web app is not accessible, use `heroku ps` to ensure that a web process is running. If it’s not running, use `heroku scale web=1` to start the web app and use the heroku logs command to determine why there was a problem.

3. Scale back to one web dyno::

    heroku scale web=1

Step 5: View App Logs on Heroku
-------------------------------

You can see everything that your app outputs to the console (STDOUT and STDERR) by running the heroku logs command.

1. To see the logs, run::

    heroku logs

2. To see log messages as they happen, use the "tail" mode::

    heroku logs -t

3. Press `CTRL-C` to stop seeing a tail of the logs.

Step 5: Roll Back a Release on Heroku
-------------------------------------

Whenever you deploy code, change a config variable, or add or remove an add-on resource, Heroku creates a new release and restarts your app. You will learn more about add-ons in Tutorial #4: Using a Heroku Add-on.

You can list the history of releases, and use rollbacks to revert to prior releases to back out of bad deployments or config changes.  This enables you to quickly revert to a known working state instead of creating a quick fix that might have other unforeseen effects.

1. To use the releases feature, install the `releases:basic` add-on.

    heroku addons:add releases:basic

Note: If the output indicates that your app already has the add-on, you can ignore the message.

2. To try it out, change an environment variable for your app on Heroku::

    heroku config:add MYVAR=42

3. Now review your list of releases on Heroku::

    heroku releases

You'll see a list of recent releases, including version number and the date of the release.

4. Roll back to the release before the MYVAR environment variable was set::

    heroku rollback

5. Verify that the MYVAR environment variable is no longer set::

    heroku config

Summary
-------

In this tutorial, you created a web app and deployed it to Heroku. You learned how to push apps to Heroku using `git` and how the `Procfile` declares what commands are started when dynos are run. You also learned how to list and scale the number of dynos, view logs, and roll back releases.


