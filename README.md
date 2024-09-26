## Academia

Academic institution management system

### Installation

If the Wiki app is already installed and running for you, you can skip this part.

#### Method 1 (recommended)

We recommend you to uninstall the Academia app before installing the Wiki app.
Make sure that you have commited all changes before uninstalling.
To uninstall, write the following command:
```bash
bench --site sitename uninstall-app academia
```

After you finish uninstalling, get and install the Wiki app through the following commands
```bash
bench get-app https://github.com/frappe/wiki.git
```
```bash
bench --site sitename install-app wiki
```

Once you are done installing wiki, you can now install the Academia app:
```bash
bench --site sitename install-app academia
```

#### Method 2

If you don't want to uninstall the Academia app, you can get and install the Wiki app:
```bash
bench get-app https://github.com/frappe/wiki.git
```
```bash
bench --site sitename install-app wiki
```

After the first install, you might encounter an error similar to
```bash
An error occurred while installing wiki: Module import failed for Wiki Page, the DocType you're trying to open might be deleted.<br> Error: No module named 'frappe.core.doctype.wiki_page'
```

Now, uninstall and re-install the app again:
```bash
bench --site sitename uninstall-app wiki --no-backup
```
```bash
bench --site sitename install-app wiki
```
Now things should be working fine.
If you are still encoutnering different errors, we recommend you to use the first method.


### Contributing
1. [Code of Conduct]()
2. [Contribution Guidelines](https://github.com/SanU-Development-Team/Academia/wiki/Contribution-Guidelines)

#### License

mit
