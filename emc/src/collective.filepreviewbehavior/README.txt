Introduction
============

collective.filepreviewbehavior contains a behavior for using
Products.ARFilePreview with dexterity content types. The views and some adapters
are overwritten ARFilePreview uses some Archetypes specific stuff.

BE WARNED: If you have a dexterity setup, you may not want to install
Archetypes. But Products.ARFilePreview was developed for Archetypes and may
still depend on it.


Usage
-----

Add the behavior ``collective.filepreviewbehavior.interfaces.IPreviewable`` to
the behaviors list of your dexterity conten type, then the uploaded file will be
converted to a HTML preview.

Use as name for the file-field "file" and mark it as primary field. The file
field should be in your primary schema interfaces, a behavior schema interface
may not work.

For more information about marking as primary field check out the dexterity
documentation (the chapter on webdav):
http://plone.org/products/dexterity/documentation/manual/developer-manual/advanced/webdav-and-other-file-representations


The Views
---------

Products.ARFilePreview provides three views:
* *file_preview* : A view containg the download link and a the preview of the
document embedded in the plone theme.
* *preview_provider* : A view only containing the preview of the document. This
view can be used as fullscreen / popup preview.
* *file_asdoc* : A view only containing the preview of the document, but embedded
in the plone theme.

You may the make some actions for your content, collective.filepreviewbehavior
will not create any actions.

