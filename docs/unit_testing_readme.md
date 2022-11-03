# Unit testing readme file.

Before you run the script consider using this command:

```bash
$ sudo -E su
```
It will save your local environment variables when accessing as root user, to prevent loosing of bot token, which should be exported as an environment variable. In case bot token is already in your local environment variables just type: 
```bash
$ sudo su
```
After you get the root priviliges activate the virtual environment using such command:
```bash
$ source testing_venv/bin/activate
```
After that optionally you can change mod of the ```run_tests.sh``` script:
```bash
$ chmod +x run_tests.sh
$ ./run_tests.sh
```

Or if you dont want to:
```bash
$ sh ./run_tests.sh
```
Running script under the root priviliges is neccesary because the ping-bot using pmutils library, which raises the ExceptionError on
process_iter() function when checking the connection to the database if it does not run under the sudo.
