
(function() {
	// Load plugin specific language pack
	tinymce.PluginManager.requireLangPack('plantuml');

	tinymce.create('tinymce.plugins.Plantuml', {

		init : function(ed, url) {
			ed.addCommand('mcePlantuml', function() {
				ed.windowManager.open({
					file : url + '/dialog.htm',
					width : 480 + parseInt(ed.getLang('plantuml.delta_width', 0)),
					height : 360 + parseInt(ed.getLang('plantuml.delta_height', 0)),
					inline : 1
				}, {
					plugin_url : url, // Plugin absolute URL
					some_custom_arg : 'custom arg' // Custom argument
				});
			});

			// Register example button
			ed.addButton('plantuml', {
			    title: 'plantuml.desc',
				cmd : 'mcePlantuml',
				image : url + '/img/uml.png'
			});

			// Add a node change handler, selects the button in the UI when a image is selected
			ed.onNodeChange.add(function(ed, cm, n) {
			    cm.setActive('plantuml', n.nodeName == 'IMG');
			});
		},

		createControl : function(n, cm) {
			return null;
		},

		getInfo : function() {
			return {
				longname : 'Insert Code plugin',
				author : 'Plantuml.com',
				authorurl : 'http://plantuml.sourceforge.net/',
				infourl: 'http://plantuml.sourceforge.net/tinymce.html',
				version : "1.0"
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('plantuml', tinymce.plugins.Plantuml);
})();