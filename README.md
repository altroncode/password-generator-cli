# Password Generator

![](assets/logo.png)


**password-generator** - application with which 
you can create passwords and keep them in storages.
This version does not require any dependency.

## Installation
```shell
git clone https://github.com/altroncode/password-generator-cli.git
```
```shell
cd password-generator-cli && bash ./install.sh
```

## Update
```shell
cd password-generator-cli && ./update.sh```
```

## Usage
```commandline
password_gen --length 20 --login username
--platform platform --storages telegram others --is_note
```
It is also possible to save an already existing password
```bash
password_gen --password "123abcABC@#$%^&"
```

To archive password the following syntax are used: &lt;storage&gt;+archive

For more information use password-gen -h

## Configuration
To set up the project, you need to rename `.env.dist` to
.env and also edit the `config/settings.ini` file.

For additional configuration used command line arguments.
