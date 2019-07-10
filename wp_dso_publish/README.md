# WP-DSO-Publish

## Operation

[Pyforms-based](https://pyforms-gui.readthedocs.io/en/v4/index.html) GUI that publishes to safe two workflow policies 
(one for Research and Infrastructure Approval, respectively) and a dataset policy that requires
that both are satisfied prior to granting access (via [Presidio](https://github.com/RENCI-NRIG/impact-presidio)).
This is consistent with SAFE ImPACT 
[MVP example](https://github.com/RENCI-NRIG/impact-docker-images/tree/master/safe-server/1.0.1).

Requires Python3 and pip3. Be sure to load the required dependencies:
```bash
$ pip install -r requirements.txt
```

Running it as as simple as, starting from the directory the contains `wp_dso_publish/`
```bash
$ export PYTHONPATH=wp_dso_publish/:$PYTHONPATH
$ python -m wp_dso_publish
```

The GUI presents two tabs - one with identifiers for the two workflows and the dataset, one with SAFE parameters.
Identifiers can either be filled in or auto-generated (GUIDs) using the 'Generate button'. SAFE server base
URL is automatically filled in. SAFE *public* key for the dataset owner principal must also be specified
(typically has the .pub extension) via file browser. 

Once all parameters are filled in, press the 'Push Combined Policy to SAFE' button and inspect the outcome. 

If everything went according to plan, cut-and-paste the workflow identifiers when registering the workflows
with the Notary Service. Similarly cut-and-paste the dataset identifier when registering the dataset. 

## Saving settings

The app relies on confapp module to restore settings in the form of Python code from a file named 
'saved-settings.py', if it exists. Any filled in settings are saved when 'Saved Settings' button is
pressed and then automatically restored when the program is restarted next time. The file can be edited
by hand if needed. The following parameters (as strings) need to be defined (example):
```
RESEARCH_APPROVAL_ID = '53f8e808-5d91-4eff-8ecf-ab7d2dcda4d3'
INFRASTRUCTURE_APPROVAL_ID = 'cf6d4ef7-d07a-4a7f-8ff5-1ec925f8df9b'
DATASET_ID = '05b88841-d14b-471d-8e0f-5da29bf8da68'
PUBLIC_KEY_PATH = '/path/to/public/key/key.pub
SAFE_URL = 'http://localhost:7777/'
```

## Tweaking

The layout is partially hard-wired in the code (see the last line of `__main__.py`):
```
if __name__ == "__main__":   pyforms.start_app(AppGUI, geometry=[100, 100, 500, 700])
```
which specifies the geometry of the main window. Couldn't find a more elegant way to do it.

The rest of the layout is contained in [style.css](style.css) file in the same directory. 