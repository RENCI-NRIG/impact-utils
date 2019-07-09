# WP-DSO-Publish

## Operation

[Pyforms-based](https://pyforms-gui.readthedocs.io/en/v4/index.html) GUI that publishes to safe two workflow policies 
(one for Research and Infrastructure Approval, respectively) and a dataset policy that requires
that both are satisfied prior to granting access (via [Presidio](https://github.com/RENCI-NRIG/impact-presidio)).
This is consistent with SAFE ImPACT 
[MVP example](https://github.com/RENCI-NRIG/impact-docker-images/tree/master/safe-server/1.0.1).

Requires Python3 and pip3. Be sure to load the required dependencies:
```
$ pip install -r requirements.txt
```

GUI presents two tabs - one with identifiers for the workflows and the dataset, one with SAFE parameters.
Identifiers can either be filled in or auto-generated (GUIDs) using the 'Generate button'. SAFE server base
URL is automatically filled in. SAFE *public* key for the dataset owner principal must also be specified
(typically has the .pub extension) via file browser. 

Once all parameters are filled in, press the 'Push Combined Policy to SAFE' button and inspect the outcome. 

If everything went according to plan, cut-and-paste the workflow identifiers when registering the workflows
with the Notary Service. Similarly cut-and-paste the dataset identifier when registering the dataset. 

## Tweaking

The layout is partially hard-wired in the code (see the last line of app_main.py):
```
if __name__ == "__main__":   pyforms.start_app(AppGUI, geometry=[100, 100, 500, 700])
```
which specifies the geometry of the main window. Couldn't find a more elegant way to do it.

The rest of the layout is contained in [style.css](style.css) file in the same directory. 