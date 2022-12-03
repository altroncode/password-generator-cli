# Password Generator

![](assets/logo.png)


**password-generator** is an application with which 
you can create passwords and keep them in storages.
This version does not require any dependency.

## Usage
In the same directory as the password-generator:

```commandline
python password_generator --length 20 --username username
--platform platform --send telegram --note
```

## Configuration
To set up the project, you need to rename `.env.dist` to
.env and also edit the `config/settings.ini` file.

For additional configuration used command line arguments.
Their settings are in `cli.py`.
