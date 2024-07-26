// vue.config.js
const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
	transpileDependencies: true,
	lintOnSave: false,
	devServer: {
		proxy: {
			"^/private/files": {
				target: "http://localhost:80",
				changeOrigin: true,
				pathRewrite: { "^/private/files": "/private/files" },
			},
		},
	},
});
