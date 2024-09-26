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
![image](https://github.com/user-attachments/assets/4a74a69a-02a2-4026-ac59-81e8e9683570)


Now, uninstall and re-install the app again:
```bash
bench --site sitename uninstall-app wiki --no-backup
```
```bash
bench --site sitename install-app wiki
```
Now things should be working fine.
If you are still encoutnering different errors, we recommend you to use the first method.


### First steps

#### Migrate

After installing the Wiki app successfully, start by migrating the data to your site.
```bash
bench --site sitename migrate
```
You should also do this everytime you pull changes from the main github repository.

#### Delete default Wiki data

Go to the *Wiki Pages* doctype and look for the two default wiki pages named *"New Wiki Page"* and *"Home"* and delete them.
![image](https://github.com/user-attachments/assets/7532eebf-940e-49f2-8007-10a1c3b340ad)

You should also go the the *Wiki Space* doctype and look for the default wiki route that has *"Wiki"* in the route column and delete it.
![image](https://github.com/user-attachments/assets/c221a0aa-5544-4955-82d5-007a2d541b11)


### Start making your Wiki

In the *Wiki Space* doctype, add a new row and in the *Route* field type the name of your project - preferably using underscore (_) instead of spaces - and then press save.
![image](https://github.com/user-attachments/assets/54eef194-ff16-4485-a355-5c0f1397332b)

After you do that, type the route name (in this case, your project name) after the domain of your site and start making your wiki :)
![image](https://github.com/user-attachments/assets/040e166f-6bea-452e-91b9-8434785d1167)


### Upload your changes

Once you are done making your Wiki and you want to push your changes, you need to do the following command:
```bash
bench --site sitename export-fixtures
```
After that you can push your changes to github and the data will be pushed with it.


### Contributing
1. [Code of Conduct]()
2. [Contribution Guidelines](https://github.com/SanU-Development-Team/Academia/wiki/Contribution-Guidelines)

#### License

mit
